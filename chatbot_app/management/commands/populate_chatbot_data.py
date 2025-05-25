import os
import re
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand
from chatbot_app.models import PageContent, FAQ
from django.conf import settings

class Command(BaseCommand):
    help = 'Populates the PageContent model with data from HTML files'

    def handle(self, *args, **options):
        self.stdout.write('Starting to populate chatbot data...')
        
        # Process different page categories
        self.process_pages('appattack')
        self.process_pages('challenges')
        self.process_pages('DeakinThreatmirror')
        self.process_pages('malware_visualization')
        self.process_pages('pt_gui')
        self.process_pages('smishing_detection')
        self.process_pages('upskilling')
        self.process_pages('Vr')
        
        self.stdout.write(self.style.SUCCESS('Successfully populated chatbot data!'))

    def process_pages(self, category):
        """Process HTML files in a specific category directory"""
        self.stdout.write(f'Processing {category} pages...')
        
        # Path to the category's HTML files
        base_path = os.path.join(settings.BASE_DIR, 'home', 'templates', 'pages', category)
        
        # Check if the directory exists
        if not os.path.exists(base_path):
            self.stdout.write(self.style.WARNING(f'Directory not found: {base_path}'))
            return
        
        # Process each HTML file in the directory
        for filename in os.listdir(base_path):
            if filename.endswith('.html'):
                file_path = os.path.join(base_path, filename)
                self.process_html_file(file_path, category, filename.replace('.html', ''))

    def process_html_file(self, file_path, category, page_name):
        """Extract content from an HTML file and store it in the database"""
        self.stdout.write(f'Processing file: {file_path}')
        
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                
                # Parse the HTML content
                soup = BeautifulSoup(content, 'html.parser')
                
                # Extract page title
                title_tag = soup.find('title')
                title = title_tag.text.strip() if title_tag else page_name.capitalize()
                
                # Extract main content sections
                self.extract_sections(soup, category, page_name, title)
                
                # Extract FAQs if they exist
                self.extract_faqs(soup, category, page_name)
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error processing {file_path}: {str(e)}'))

    def extract_sections(self, soup, category, page_name, title):
        """Extract different sections from the HTML content"""
        # Create a base record for the page
        page_path = f'/{category}/{page_name}'
        
        # Create keywords from title and category
        keywords = f"{title}, {category}, {page_name}".lower()
        
        # Try to extract a description from meta tags or first paragraph
        description = ""
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        if meta_desc and 'content' in meta_desc.attrs:
            description = meta_desc['content']
        else:
            first_p = soup.find('p')
            if first_p:
                description = first_p.text.strip()
        
        # Save the base page information
        PageContent.objects.update_or_create(
            page_path=page_path,
            section='overview',
            defaults={
                'title': title,
                'content': description,
                'keywords': keywords,
                'page_category': category
            }
        )
        
        # Extract sections from headings and their content
        headings = soup.find_all(['h1', 'h2', 'h3'])
        for heading in headings:
            section_title = heading.text.strip()
            if not section_title:
                continue
                
            # Get content following this heading
            section_content = ""
            current = heading.next_sibling
            
            # Collect content until the next heading or significant element
            while current and not current.name in ['h1', 'h2', 'h3', 'section']:
                if hasattr(current, 'text'):
                    text = current.text.strip()
                    if text:
                        section_content += text + " "
                current = current.next_sibling
            
            # If we found content, save it
            if section_content:
                section_keywords = f"{section_title}, {title}, {category}".lower()
                
                PageContent.objects.update_or_create(
                    page_path=page_path,
                    section=self.clean_section_name(section_title),
                    defaults={
                        'title': f"{title} - {section_title}",
                        'content': section_content.strip(),
                        'keywords': section_keywords,
                        'page_category': category
                    }
                )

    def extract_faqs(self, soup, category, page_name):
        """Extract FAQs from accordions or similar structures"""
        # Look for accordion items which often contain FAQs
        accordion_items = soup.find_all(class_=re.compile(r'accordion-item'))
        
        for item in accordion_items:
            question_elem = item.find(['button', 'h2', 'h3', 'h4'])
            answer_elem = item.find(class_=re.compile(r'accordion-body|accordion-content|collapse'))
            
            if question_elem and answer_elem:
                question = question_elem.text.strip()
                answer = answer_elem.text.strip()
                
                if question and answer:
                    # Store in the PageContent model for the chatbot to find
                    page_path = f'/{category}/{page_name}#faq'
                    section_keywords = f"faq, {question}, {category}".lower()
                    
                    PageContent.objects.update_or_create(
                        page_path=page_path,
                        section=f"faq-{self.clean_section_name(question)}",
                        defaults={
                            'title': f"FAQ: {question}",
                            'content': answer,
                            'keywords': section_keywords,
                            'page_category': category
                        }
                    )
                    
                    # Also store in the FAQ model
                    FAQ.objects.update_or_create(
                        question=question,
                        defaults={
                            'answer': answer,
                            'keywords': section_keywords,
                            'category': category
                        }
                    )

    def clean_section_name(self, section_name):
        """Clean section name to be used as an identifier"""
        # Replace spaces and special characters with hyphens
        section_name = re.sub(r'[^\w\s]', '', section_name.lower())
        section_name = re.sub(r'\s+', '-', section_name)
        return section_name[:50]  # Limit length 