# core/views.py

import os, logging
from django.shortcuts import render, get_object_or_404
from .forms import ScenarioForm
from .models import ConstitutionArticle, CaseLaw
from .helpers.retrieval import find_relevant_articles_and_cases
from .helpers.placeholder import generate_placeholders
from .utils.llm import call_local_llm
from .models import SavedScenario  # assume you have a model to store
logger = logging.getLogger(__name__)
PROMPT_PATH = os.path.join(os.path.dirname(__file__), "prompts", "argument_template.txt")





def label_irac_blocks(raw: str):
    """
    Split a raw IRAC string on double newlines and map each
    chunk to a label + text dict for the template.
    """
    mapping = [
        ("C) **Conclusion:**",         "Conclusion"),
        ("R) **Rule & Precedent:**",   "Rule & Precedent"),
        ("E) **Explanation & Commentary:**", "Explanation & Commentary"),
        ("A) **Application:**",        "Application"),
        ("R) **Rebuttal:**",           "Rebuttal"),
        ("C) **Conclusion & Remedy:**","Conclusion & Remedy"),
    ]

    blocks = []
    for chunk in raw.split("\n\n"):
        chunk = chunk.strip()
        if not chunk:
            continue
        for prefix, label in mapping:
            if chunk.startswith(prefix):
                text = chunk[len(prefix):].strip()
                blocks.append({"label": label, "text": text})
                break
        else:
            blocks.append({"label": None, "text": chunk})
    return blocks

def input_view(request):
    # Fetch the 20 most recent saved scenarios
    memories = SavedScenario.objects.order_by('-created_at')[:20]

    if request.method == 'POST':
        form = ScenarioForm(request.POST)
        if form.is_valid():
            scenario_text = form.cleaned_data['scenario']

            # Save this scenario
            SavedScenario.objects.create(
                title=scenario_text[:150],
                scenario=scenario_text
            )

            # Generate raw IRAC outputs
            for_raw, against_raw = generate_arguments(scenario_text)

            # Split & label them
            for_blocks    = label_irac_blocks(for_raw)
            against_blocks = label_irac_blocks(against_raw)

            return render(request, 'chat.html', {
                'for_blocks':    for_blocks,
                'against_blocks': against_blocks,
                'for_feedback':   None,
                'against_feedback': None,
                'memories':       memories,
            })
    else:
        form = ScenarioForm()

    # On GET (or invalid POST), just show the form + sidebar
    return render(request, 'chat.html', {
        'form':      form,
        'memories':  memories,
    })

def generate_arguments(scenario: str):
    # 1) Retrieve relevant law
    articles, cases = find_relevant_articles_and_cases(scenario, top_k=3)

    # Build full-text blocks
    articles_full = ""
    for art in articles:
        articles_full += (
            f"Article {art.article_id} (Chapter {art.chapter} – {art.section}):\n"
            f"{art.text}\n\n"
        )

    cases_full = ""
    for c in cases:
        cases_full += (
            f"{c.name} [{c.case_id}] ({c.court_name}):\n"
            f"{c.summary}\n\n"
        )

    # 2) Extract placeholders
    ph = generate_placeholders(scenario)

    # 3) Load & fill prompt with full-text and placeholders
    template = open(PROMPT_PATH, encoding='utf-8').read()
    prompt = template.format(
        scenario=scenario,
        articles_full=articles_full,
        cases_full=cases_full,
        who=ph['who'],
        what=ph['what'],
        when=ph['when'],
        where=ph['where'],
        how=ph['how'],
        issues=ph['issues'],
        jurisdiction=ph['jurisdiction'],
        treaties=ph['treaties'],
        policy_arg=ph['policy_arg'],
        counterarguments=ph['counterarguments'],
    )
    logger.debug("Prompt:\n%s", prompt)

    # 4) Call LLM
    output = call_local_llm(prompt)
    logger.debug("Output:\n%s", output)

    # 5) Split FOR/AGAINST
    if "--- FOR ---" in output and "--- AGAINST ---" in output:
        for_part = output.split("--- FOR ---", 1)[1].split("--- AGAINST ---", 1)[0].strip()
        against_part = output.split("--- AGAINST ---", 1)[1].strip()
        return for_part, against_part

    # Fallback
    return output, ""

def article_detail(request, article_id):
    art = get_object_or_404(ConstitutionArticle, article_id=article_id)
    return render(request, 'core/article_detail.html', {'article': art})

def case_detail(request, case_id):
    case = get_object_or_404(CaseLaw, case_id=case_id)
    return render(request, 'core/case_detail.html', {'case': case})

import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt  # or use the AJAX-CSRFTOKEN pattern
def refine_argument(request):
    """
    AJAX endpoint: refine the 'for' or 'against' argument.
    Expects JSON: { side, original, instruction }
    """
    data = json.loads(request.body.decode())
    side        = data.get('side')        # "for" or "against"
    original    = data.get('original')    # the full CREAC block
    instruction = data.get('instruction') # e.g. "Drill down on that policy point"

    # Build a small refinement prompt
    prompt = f"""
You are a Supreme Court advocate. Below is the original {side.upper()} submission:

{original}

REFINEMENT INSTRUCTION:
"{instruction}"

Please produce an improved version of only the {side.upper()} submission,
keeping the CREAC structure and citations, and integrating the refinement.
"""

    refined = call_local_llm(prompt)  # uses mistral:latest
    return JsonResponse({'refined': refined})

@csrf_exempt
def augment_argument(request):
    """
    AJAX endpoint to augment (append to) the 'for' or 'against' argument,
    based on a user question or instruction.
    Expects JSON: { side, original, instruction }
    Returns JSON: { augmented: "<original>\n\n<APPENDIX>" }
    """
    data = json.loads(request.body)
    side        = data['side']
    original    = data['original']
    instruction = data['instruction']

    prompt = f"""
You are a top‑tier Zambian advocate. Below is the existing {side.upper()} submission:

{original}

INSTRUCTION:
“{instruction}”

Your job: **Do not rewrite or remove a single word** from the original.  
Instead, **append** a clearly marked “Addendum” that:
 - Directly answers the instruction,
 - Uses CREAC if needed,
 - Preserves tone, citations, emotion, and structure.

Format your response as:

<<< ORIGINAL >>>
{original}

<<< ADDENDUM >>>
[Your appended content]
"""

    response = call_local_llm(prompt)
    # Split at markers
    if "<<< ADDENDUM >>>" in response:
        parts = response.split("<<< ADDENDUM >>>", 1)
        appendix = parts[1].strip()
        augmented = parts[0].replace("<<< ORIGINAL >>>", "").strip() \
                    + "\n\n" + appendix
    else:
        # Fallback: just append raw response
        augmented = original + "\n\n" + response

    return JsonResponse({'augmented': augmented})


from django.shortcuts import render

from .helpers.contract_utils import build_contract_prompt
from .utils.llm import call_local_llm

from django.shortcuts import render
from django.template import Template, Context
from .forms import NDAForm, SaleForm, LeaseForm, EmploymentForm
from django.template import Template, Context

def build_contract_prompt(template_name, data):
    prompt_path = f'core/prompts/contracts/{template_name}'
    with open(prompt_path, encoding='utf-8') as f:
        content = f.read()
    return Template(content).render(Context(data))



def contract_list(request):
    return render(request, 'contracts/contract_list.html')


def nda_view(request):
    form = NDAForm(request.POST or None)
    draft = risk_report = None
    if form.is_valid():
        data   = form.cleaned_data
        prompt = build_contract_prompt('nda', data)
        draft  = call_local_llm(prompt)
        risk_report = call_local_llm(f"Identify risks in each numbered clause:\n\n{draft}")
    return render(request, 'contracts/nda.html', {
        'form': form, 'draft': draft, 'risk_report': risk_report
    })

def sale_view(request):
    form = SaleForm(request.POST or None)
    draft = risk_report = None
    if form.is_valid():
        data   = form.cleaned_data
        prompt = build_contract_prompt('sale', data)
        draft  = call_local_llm(prompt)
        risk_report = call_local_llm(f"Identify risks in each numbered clause:\n\n{draft}")
    return render(request, 'contracts/sale.html', {
        'form': form, 'draft': draft, 'risk_report': risk_report
    })

def lease_view(request):
    form = LeaseForm(request.POST or None)
    draft = risk_report = None
    if form.is_valid():
        data   = form.cleaned_data
        prompt = build_contract_prompt('lease', data)
        draft  = call_local_llm(prompt)
        risk_report = call_local_llm(f"Identify risks in each numbered clause:\n\n{draft}")
    return render(request, 'contracts/lease.html', {
        'form': form, 'draft': draft, 'risk_report': risk_report
    })

from .helpers.contract_utils import build_contract_prompt

def employment_view(request):
    form = EmploymentForm(request.POST or None)
    draft = risk_report = None

    if form.is_valid():
        data   = form.cleaned_data
        prompt = build_contract_prompt('employment', data)
        draft  = call_local_llm(prompt)
        risk_report = call_local_llm(
            "Identify any legal or practical risk in each numbered clause:\n\n" + draft
        )

    return render(request, 'contracts/employment.html', {
        'form': form,
        'draft': draft,
        'risk_report': risk_report,
    })



from django.shortcuts import redirect
from .models import SavedScenario

def load_scenario(request, pk):
    """
    Load a previously saved scenario and redirect back to input_view,
    pre‑populating the textarea.
    """
    scenario = get_object_or_404(SavedScenario, pk=pk).scenario
    # We’ll pass it via GET so the form can pick it up
    return redirect(f"/?scenario={scenario!s}")


from .forms import WillForm, PetitionForm
from .helpers.will_utils import build_will_prompt
from .helpers.petition_utils import build_petition_prompt

from django.shortcuts import render
from .forms import WillForm

def will_view(request):
    will_text = None
    if request.method == "POST":
        form = WillForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            # Build a prompt and call your LLM here.
            prompt = f"""
Last Will & Testament:

Testator: {data['testator_name']}
Executor: {data['executor_name']}

Residuary Clause:
{data['residuary']}

Special Requests:
{data['special_requests']}

Beneficiaries:
""" 
            # Append beneficiaries from POST arrays:
            names = request.POST.getlist('beneficiary_name[]')
            rels  = request.POST.getlist('beneficiary_relationship[]')
            gifts = request.POST.getlist('beneficiary_gift[]')
            for n, r, g in zip(names, rels, gifts):
                prompt += f"- {n} ({r}): {g}\n"
            # Here you would call call_local_llm(prompt)
            will_text = call_local_llm(prompt)  # or however you integrate

    else:
        form = WillForm()

    return render(request, "will_draft.html", {
        "form": form,
        "will_text": will_text,
    })


def petition_view(request):
    petition_text = None
    if request.method == 'POST':
        form = PetitionForm(request.POST)
        if form.is_valid():
            prompt = build_petition_prompt(form.cleaned_data)
            petition_text = call_local_llm(prompt)
    else:
        form = PetitionForm()

    return render(request, 'petition_draft.html', {
        'form': form,
        'petition_text': petition_text
    })
