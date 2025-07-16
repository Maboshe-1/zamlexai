# core/models.py
from django.db import models

class ConstitutionArticle(models.Model):
    article_id = models.CharField(max_length=20, unique=True)
    chapter = models.CharField(max_length=50)
    section = models.CharField(max_length=250)
    text = models.TextField()
    tags = models.CharField(max_length=255)  # Comma-separated keywords, e.g., "eligibility, president, term limits"
    implication = models.TextField(default="the principle supports the client", help_text="What this article establishes or implies.")
    potential_counterargument = models.TextField(default="an alternative interpretation limits this right", help_text="Possible opposing view or limitation.")

    def __str__(self):
        return f"Article {self.article_id}"

class CaseLaw(models.Model):
    case_id = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    summary = models.TextField()
    related_articles = models.ManyToManyField(ConstitutionArticle)
    tags = models.CharField(max_length=255)  # Comma-separated keywords, e.g., "eligibility, partial term"
    authority_level = models.IntegerField(default=1)  # e.g., 1 = Supreme Court, 2 = High Court, etc.
    court_name = models.CharField(max_length=100, default=True)  # New field for the court that handled the cases

    def __str__(self):
        return self.name
    

class SavedScenario(models.Model):
    title = models.CharField(max_length=150)
    scenario = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # show first 50 chars as title if no title provided
        return self.title or self.scenario[:50]

