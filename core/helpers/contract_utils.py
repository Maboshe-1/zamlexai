# core/helpers/contract_utils.py

import os
from pathlib import Path
from django.conf import settings
from django.template import Template, Context
from django.utils import timezone

from .retrieval import find_relevant_articles_and_cases

def build_contract_prompt(template_name: str, data: dict) -> str:
    """
    1) Semantic retrieval of top‑3 articles & cases for `template_name`.
    2) Loads `core/prompts/contracts/{template_name}.txt`.
    3) Renders with form `data`, plus law & date.
    """
    # ── semantic retrieval ────────────────────────────────
    articles, cases = find_relevant_articles_and_cases(template_name, top_k=3)
    articles_full = "\n".join(f"Article {a.article_id}: {a.text[:200]}…" for a in articles) or "None"
    cases_full    = "\n".join(f"*{c.name}* [{c.case_id}]: {c.summary[:200]}…" for c in cases) or "None"

    # ── build the .txt file path ──────────────────────────
    prompts_dir = Path(settings.BASE_DIR) / 'core' / 'prompts' / 'contracts'
    tpl_path    = prompts_dir / f"{template_name}.txt"

    if not tpl_path.exists():
        raise FileNotFoundError(f"Contract template not found: {tpl_path}")

    raw = tpl_path.read_text(encoding='utf-8')

    # ── render with Django Template ───────────────────────
    tpl = Template(raw)
    ctx = Context({
        **data,
        'articles_full': articles_full,
        'cases_full':    cases_full,
        'now':           timezone.now().strftime('%d %B %Y'),
    })
    return tpl.render(ctx)
