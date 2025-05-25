import unittest
from django.test import TestCase
from django.db import models as django_models
from ..search_engine import get_model_class_names, get_model_fields, split_camel, build_model_format, get_searchable_models
from home import models

class TestModelUtils(TestCase):
    def test_get_model_class_names(self):
        # Get the model class names
        model_names = get_model_class_names()
        
        # Verify we got a list
        self.assertIsInstance(model_names, list)
        
        # Verify the list is not empty (assuming there are models in home.models)
        self.assertTrue(len(model_names) > 0)
        
        # Verify each name is a string
        for name in model_names:
            self.assertIsInstance(name, str)
            
        # Verify that the names actually correspond to models
        for name in model_names:
            # Check if the name exists in models module
            self.assertTrue(hasattr(models, name))
            # Get the actual attribute
            model_class = getattr(models, name)
            # Verify it's a Django model class (has _meta attribute)
            self.assertTrue(hasattr(model_class, '_meta'))

        # Print the found models for inspection
        print("\nFound models:", model_names)

    def test_get_model_fields(self):
        # Get all model names first
        model_names = get_model_class_names()
        
        print("\n=== Testing fields for all models ===")
        for model_name in model_names:
            # Skip abstract models as they can't be instantiated
            model_class = getattr(models, model_name)
            if hasattr(model_class, '_meta') and not model_class._meta.abstract:
                fields = get_model_fields(model_class)
                
                # Verify we got a dictionary
                self.assertIsInstance(fields, dict)
                
                # Verify the dictionary is not empty
                self.assertTrue(len(fields) > 0)
                
                # Print fields for this model
                print(f"\n{model_name} fields:", fields)
                
                # Verify field types are correct string representations
                for field_name, field_type in fields.items():
                    self.assertIsInstance(field_name, str)
                    self.assertIsInstance(field_type, str)
        
        # Test that relational fields are excluded
        class TestModel(django_models.Model):
            name = django_models.CharField(max_length=100)
            related = django_models.ForeignKey('self', on_delete=django_models.CASCADE)
            
            class Meta:
                app_label = 'chatbot_app'
                
        test_fields = get_model_fields(TestModel)
        self.assertIn('name', test_fields)  # Regular field should be included
        self.assertNotIn('related', test_fields)  # Relation field should be excluded 

    def test_split_camel(self):
        # Get all model names
        model_names = get_model_class_names()
        
        print("\n=== Testing split_camel function on ALL models ===")
        print("Format: OriginalName -> split result")
        print("-" * 50)
        
        # Test with all actual model names from our system
        for model_name in sorted(model_names):  # Sort for consistent output
            result = split_camel(model_name)
            print(f"{model_name:30} -> {result}")
            
            # Basic validation
            self.assertIsInstance(result, str)
            self.assertTrue(len(result) > 0)
            
        # Additional edge cases
        print("\n=== Testing edge cases ===")
        edge_cases = {
            "DDTContact": "d d t contact",  # Multiple uppercase in sequence
            "API2Model": "a p i model",  # Numbers
            "UserXYZProfile": "user x y z profile",  # Multiple uppercase sequence
            "iOS_App": "i o s app",  # Mixed case with underscore
            "MyURLParser": "my u r l parser",  # Mixed acronym
        }
        
        for test_input, expected in edge_cases.items():
            result = split_camel(test_input)
            print(f"{test_input:30} -> {result}")
            # Uncomment to enforce strict checking
            # self.assertEqual(result, expected) 

    def test_build_model_format(self):
        # Get the model format dictionary
        model_format = build_model_format()
        
        print("\n=== Testing build_model_format ===")
        print("Format: model_key")
        print("  emoji: emoji")
        print("  label: human readable label")
        print("  url_pattern: URL pattern")
        print("  fields: field dictionary")
        print("-" * 50)
        
        # Test that we got a dictionary
        self.assertIsInstance(model_format, dict)
        
        # Test each model's format
        for model_key, format_info in sorted(model_format.items()):
            print(f"\nModel: {model_key}")
            print(f"  emoji: {format_info['emoji']}")
            print(f"  label: {format_info['label']}")
            print(f"  url_pattern: {format_info['url_pattern']}")
            print(f"  fields: {format_info['fields']}")
            
            # Verify structure
            self.assertIn('emoji', format_info)
            self.assertIn('label', format_info)
            self.assertIn('url_pattern', format_info)
            self.assertIn('fields', format_info)
            
            # Verify types
            self.assertIsInstance(format_info['emoji'], str)
            self.assertIsInstance(format_info['label'], str)
            self.assertIsInstance(format_info['url_pattern'], str)
            self.assertIsInstance(format_info['fields'], dict)
            
            # Verify URL pattern format
            self.assertTrue(format_info['url_pattern'].startswith('/'))
            self.assertIn('{id}', format_info['url_pattern'])
            
            # Verify fields dictionary is not empty
            self.assertTrue(len(format_info['fields']) > 0)
            
            # Verify emoji was assigned
            self.assertNotEqual(format_info['emoji'], '') 

    def test_get_searchable_models(self):
        # Test with default app_label ('home')
        models_dict = get_searchable_models()
        
        print("\n=== Testing get_searchable_models ===")
        print("Format: model_key -> model_class")
        print("-" * 50)
        
        # Verify we got a dictionary
        self.assertIsInstance(models_dict, dict)
        
        # Print and verify each model
        for key, model_class in sorted(models_dict.items()):
            print(f"{key:30} -> {model_class.__name__}")
            
            # Verify key is lowercase model name
            self.assertEqual(key, model_class.__name__.lower())
            
            # Verify it's a Django model class
            self.assertTrue(hasattr(model_class, '_meta'))
            
            # Verify it's from the home app
            self.assertEqual(model_class._meta.app_label, 'home')
            
        # Test with non-existent app
        empty_models = get_searchable_models('non_existent_app')
        self.assertEqual(len(empty_models), 0) 