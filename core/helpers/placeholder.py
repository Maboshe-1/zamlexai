# core/helpers/placeholder.py

from core.utils.llm import call_local_llm

def generate_placeholders(scenario: str) -> dict:
    """
    Single LLM call that returns a Python dict with:
      who, what, when, where, how,
      issues, jurisdiction,
      treaties, policy_arg, counterarguments
    """
    prompt = f"""
You are a Zambian legal analyst. Given the scenario below, respond with a Python dict
having keys: who, what, when, where, how, issues, jurisdiction, treaties, policy_arg, counterarguments.

Scenario:
\"\"\"{scenario}\"\"\"

Only output the dict.
"""
    resp = call_local_llm(prompt)  # uses mistral:latest
    try:
        data = eval(resp, {"__builtins__": {}})
        if isinstance(data, dict):
            return data
    except Exception:
        pass

    # fallback defaults
    return {
        "who": "Unknown",
        "what": scenario[:100],
        "when": "recently",
        "where": "Zambia",
        "how": "Not specified",
        "issues": "Main legal issue unclear",
        "jurisdiction": "High Court of Zambia",
        "treaties": "None",
        "policy_arg": "No policy argument provided",
        "counterarguments": "No counterarguments identified"
    }
