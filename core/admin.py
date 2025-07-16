# core/admin.py
from django.contrib import admin
from .models import ConstitutionArticle, CaseLaw, SavedScenario

class ConstitutionArticleAdmin(admin.ModelAdmin):
    list_display = ('article_id', 'chapter', 'section')
    search_fields = ('article_id', 'text', 'tags')

class CaseLawAdmin(admin.ModelAdmin):
    list_display = ('case_id', 'name', 'court_name', 'authority_level')  # Added court_name and authority_level
    search_fields = ('name', 'summary', 'tags', 'court_name')
    filter_horizontal = ('related_articles',)




admin.site.register(ConstitutionArticle, ConstitutionArticleAdmin)
admin.site.register(CaseLaw, CaseLawAdmin)
admin.site.register(SavedScenario)