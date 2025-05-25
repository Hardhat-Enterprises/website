from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from chatbot_app.search_engine import (
    search_engine,
    spell_correct,
    identify_model_from_prompt,
    extract_search_term,
    get_searchable_models
)
from termcolor import colored
import time

class Command(BaseCommand):
    help = 'Test the chatbot search functionality with various test cases'

    def add_arguments(self, parser):
        parser.add_argument(
            '--verbose',
            action='store_true',
            help='Show detailed test output'
        )
        parser.add_argument(
            '--timing',
            action='store_true',
            help='Show timing information for searches'
        )

    def success(self, message):
        self.stdout.write(self.style.SUCCESS(f"✓ {message}"))

    def error(self, message):
        self.stdout.write(self.style.ERROR(f"✗ {message}"))

    def info(self, message):
        self.stdout.write(self.style.NOTICE(f"ℹ {message}"))

    def run_test(self, name, func):
        """Run a test and print its result"""
        try:
            start_time = time.time()
            result = func()
            duration = time.time() - start_time
            
            if result:
                self.success(f"{name} ({duration:.3f}s)")
                return True
            else:
                self.error(f"{name} ({duration:.3f}s)")
                return False
        except Exception as e:
            self.error(f"{name} - Exception: {str(e)}")
            return False

    def test_spell_correction(self):
        """Test spell correction functionality"""
        test_cases = [
            ("cybre security", "cyber security"),
            ("malwar detection", "malware detection"),
            ("penetraton testing", "penetration testing"),
            ("firewal skills", "firewall skills"),
            ("chalenge", "challenge")
        ]
        
        all_passed = True
        for input_text, expected in test_cases:
            corrected, was_corrected = spell_correct(input_text)
            if corrected != expected:
                if self.verbose:
                    self.error(f"Spell correction failed: '{input_text}' → '{corrected}' (expected: '{expected}')")
                all_passed = False
            elif self.verbose:
                self.success(f"Spell correction: '{input_text}' → '{corrected}'")
        
        return all_passed

    def test_model_identification(self):
        """Test model identification from various prompts"""
        models = get_searchable_models()
        test_cases = [
            ("show me cyber challenges", "cyberchallenge"),
            ("what skills do I need", "skill"),
            ("list all courses", "course"),
            ("recent announcements", "announcement"),
            ("tell me about projects", "project")
        ]
        
        all_passed = True
        for prompt, expected in test_cases:
            model_key = identify_model_from_prompt(prompt, models)
            if model_key != expected:
                if self.verbose:
                    self.error(f"Model identification failed: '{prompt}' → '{model_key}' (expected: '{expected}')")
                all_passed = False
            elif self.verbose:
                self.success(f"Model identification: '{prompt}' → '{model_key}'")
        
        return all_passed

    def test_term_extraction(self):
        """Test search term extraction from prompts"""
        models = get_searchable_models()
        test_cases = [
            ("show me cyber challenges about encryption", "encryption"),
            ("what skills do I need for penetration testing", "penetration testing"),
            ("list all courses", ""),  # Empty term for listing all
            ("recent announcements about security", "security"),
            ("tell me about projects with python", "python")
        ]
        
        all_passed = True
        for prompt, expected in test_cases:
            model_key = identify_model_from_prompt(prompt, models)
            if not model_key:
                if self.verbose:
                    self.error(f"Could not identify model for: '{prompt}'")
                all_passed = False
                continue
                
            term = extract_search_term(prompt, model_key, models)
            if term != expected:
                if self.verbose:
                    self.error(f"Term extraction failed: '{prompt}' → '{term}' (expected: '{expected}')")
                all_passed = False
            elif self.verbose:
                self.success(f"Term extraction: '{prompt}' → '{term}'")
        
        return all_passed

    def test_full_search(self):
        """Test complete search functionality with real queries"""
        test_cases = [
            # Original test cases
            "what cyber challenges are available today",
            "show me skills related to penetration testing",
            "list recent announcements",
            "tell me about malware visualization project",
            "courses about cybersecurity",
            "what challenges involve encryption",
            
            # New natural language variations
            "any announcements today?",
            "got any new challenges?",
            "show me today's articles",
            "what skills are trending?",
            "any cybersecurity courses available?",
            "latest projects?",
            "do we have any new challenges today?",
            "what announcements did I miss?",
            "show me articles about malware",
            "any challenges about web security?",
            "what's new in announcements?",
            "got any python courses?",
            "show me networking skills",
            "any projects involving AI?",
            "what challenges are hot right now?"
        ]
        
        all_passed = True
        for query in test_cases:
            try:
                start_time = time.time()
                results = search_engine(query)
                duration = time.time() - start_time
                
                if isinstance(results, dict) and 'error' in results:
                    if self.verbose:
                        self.error(f"Search failed for '{query}': {results['error']}")
                    all_passed = False
                else:
                    if self.verbose:
                        self.success(f"Search successful for '{query}' - {len(results['results'])} results ({duration:.3f}s)")
                        if self.timing:
                            self.info(f"Query info: {results.get('query_info', {})}")
            except Exception as e:
                if self.verbose:
                    self.error(f"Search error for '{query}': {str(e)}")
                all_passed = False
        
        return all_passed

    def handle(self, *args, **options):
        self.verbose = options['verbose']
        self.timing = options['timing']
        
        self.stdout.write("\n🔍 Testing Chatbot Search Functionality\n")
        
        tests = [
            ("Spell Correction", self.test_spell_correction),
            ("Model Identification", self.test_model_identification),
            ("Term Extraction", self.test_term_extraction),
            ("Full Search", self.test_full_search)
        ]
        
        total = len(tests)
        passed = 0
        
        for name, func in tests:
            if self.run_test(name, func):
                passed += 1
                
        self.stdout.write("\n" + "="*50 + "\n")
        if passed == total:
            self.success(f"All {total} tests passed!")
        else:
            self.error(f"{passed}/{total} tests passed") 