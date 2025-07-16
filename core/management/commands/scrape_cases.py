from django.core.management.base import BaseCommand
from core.models import CaseLaw, ConstitutionArticle
import requests
from bs4 import BeautifulSoup
from pdfplumber import open as pdf_open

class Command(BaseCommand):
    help = 'Scrape case laws and store them in the database'

    def handle(self, *args, **kwargs):
        url = "https://zambialii.org/judgments/"  # Replace with the actual URL you are scraping
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        # Scrape the case data
        cases = soup.find_all('div', class_='case')  # Update based on the actual HTML structure

        for case in cases:
            case_name = case.find('h2').text
            case_summary = case.find('p').text
            case_tags = ', '.join([tag.text for tag in case.find_all('span', class_='tag')])  # Adjust tag extraction based on website structure

            # Create a new CaseLaw instance
            case_law = CaseLaw(
                case_id=self.generate_case_id(),  # Add logic to generate unique case ID
                name=case_name,
                summary=case_summary,
                tags=case_tags,
            )

            # Check if there are any related Constitution Articles
            related_articles = self.extract_related_articles(case)  # Function to extract related articles
            case_law.save()

            # Add related articles to the case
            case_law.related_articles.add(*related_articles)

            # Check if there's a PDF, and if so, extract text
            pdf_link = case.find('a', text='PDF')  # Adjust based on actual link text
            if pdf_link:
                pdf_url = pdf_link['href']
                pdf_text = self.extract_pdf_text(pdf_url)
                case_law.summary += "\n" + pdf_text  # Append the PDF text to the case summary

            case_law.save()

    def generate_case_id(self):
        # Logic to generate unique case ID (could be based on a timestamp or other identifiers)
        return "CASE123"  # Placeholder logic

    def extract_related_articles(self, case):
        # Extract related Constitution Articles (this can be customized based on your scraping needs)
        related_articles = []
        article_ids = case.find_all('span', class_='article-id')  # Adjust based on HTML
        for article_id in article_ids:
            article = ConstitutionArticle.objects.filter(article_id=article_id.text).first()  # Fetch related article
            if article:
                related_articles.append(article)
        return related_articles

    def extract_pdf_text(self, pdf_url):
        # Download and extract text from a PDF
        response = requests.get(pdf_url)
        with open('temp.pdf', 'wb') as f:
            f.write(response.content)

        with pdf_open('temp.pdf') as pdf:
            text = ''
            for page in pdf.pages:
                text += page.extract_text()

        return text
