# core/helpers/retrieval.py

from sentence_transformers import SentenceTransformer, util
from core.models import ConstitutionArticle, CaseLaw

model = SentenceTransformer('all-MiniLM-L6-v2')

def find_relevant_articles_and_cases(scenario: str, top_k: int = 3):
    """
    1) Embed scenario, articles, and cases.
    2) Boost by tag relevance.
    3) Return top_k of each.
    """
    emb = model.encode(scenario, convert_to_tensor=True)

    # Score articles
    scores = []
    for art in ConstitutionArticle.objects.all():
        sim = util.cos_sim(emb,
            model.encode(art.text, convert_to_tensor=True)
        ).item()
        boost = 0.2 if any(tag in scenario.lower() for tag in art.tags.lower().split(',')) else 0
        scores.append((sim + boost, art))
    scores.sort(key=lambda x: x[0], reverse=True)
    top_articles = [art for _, art in scores[:top_k]]

    # Score cases
    scores = []
    for case in CaseLaw.objects.all():
        sim = util.cos_sim(emb,
            model.encode(case.summary, convert_to_tensor=True)
        ).item()
        boost = 0.2 if any(tag in scenario.lower() for tag in case.tags.lower().split(',')) else 0
        scores.append((sim + boost, case))
    scores.sort(key=lambda x: x[0], reverse=True)
    top_cases = [case for _, case in scores[:top_k]]

    return top_articles, top_cases
