import re
from difflib import get_close_matches
import logging
from typing import Dict, Any, Optional, List, Tuple
from django.apps import apps
from django.db.models import Q, Model, Field
from django.db.models.fields import CharField, TextField, DateTimeField, BooleanField, IntegerField
from textblob import TextBlob
from .textblob_analyzer import correct_spelling, extract_noun_phrases
from .result_formatter import format_search_results_rich, format_as_markdown, format_for_chat
from django.utils import timezone
from jinja2 import Environment, FileSystemLoader

logger = logging.getLogger(__name__)


def initialize_search_engine() -> Dict[str, Any]:
    """
    Build a mapping of keyword to model for dynamic searching.
    Prioritizes models from the home app.
    """
    model_mapping: Dict[str, Any] = {}
    
    # Priority models from home app that we want to search
    priority_models = [
        'BlogPost',         # For blog content
        'CyberChallenge',  # For challenge information
        'Job',             # For job listings
        'Article',         # For articles
        'Skill',           # For skill information
        'Course',          # For course information
        'Announcement',    # For announcements
        'Webpage',         # For webpage content
        'Project',         # For project information
    ]
    
    logger.info("Initializing search engine models...")
    
    # First, add all models from the home app
    for model in apps.get_models():
        if model._meta.app_label == 'home':
            key = model.__name__.lower()
            model_mapping[key] = model
            # Also add the verbose name as a key
            verbose_name = model._meta.verbose_name.lower().replace(' ', '_')
            model_mapping.setdefault(verbose_name, model)
            
            # Add common variations of the model name
            if key.endswith('y'):
                # Handle plural form (e.g., category -> categories)
                plural = f"{key[:-1]}ies"
                model_mapping.setdefault(plural, model)
            else:
                # Regular plural
                model_mapping.setdefault(f"{key}s", model)
    
    logger.info(f"Initialized search models: {list(model_mapping.keys())}")
    return model_mapping


def extract_keywords(text: str) -> list[str]:
    """
    Enhanced keyword extraction using TextBlob.
    Extracts important words and noun phrases.
    """
    # Get noun phrases
    blob = TextBlob(text)
    noun_phrases = [np for np in blob.noun_phrases if len(np) > 2]
    
    # Get words excluding stopwords (common words like 'the', 'and', etc.)
    important_words = [
        word.lower() for word in blob.words 
        if len(word) > 2 and word.lower() not in ['the', 'and', 'for', 'that', 'this', 'with']
    ]
    
    # Combine and remove duplicates
    keywords = list(set(important_words + noun_phrases))
    
    # Fall back to simple regex extraction if TextBlob yields no results
    if not keywords:
        keywords = [w for w in re.findall(r"\w+", text.lower()) if len(w) > 2]
    
    return keywords


def spell_correct(word: str, vocabulary: list[str]) -> str:
    """
    Correct a single token via TextBlob's spelling correction.
    Falls back to fuzzy matching if TextBlob correction isn't in vocabulary.
    """
    # Try TextBlob correction first
    blob_word = TextBlob(word)
    corrected = str(blob_word.correct())
    
    # If the corrected word is in our vocabulary, use it
    if corrected in vocabulary:
        return corrected
    
    # Otherwise, fall back to fuzzy matching
    matches = get_close_matches(word, vocabulary, n=1, cutoff=0.8)
    return matches[0] if matches else word


def identify_model_from_prompt(prompt: str, models: Dict[str, Any]) -> Optional[Any]:
    """
    Return the most appropriate model for the prompt.
    Uses TextBlob for better keyword extraction and matching.
    """
    logger.info(f"Identifying model for prompt: '{prompt}'")
    
    # Extract tokens from prompt
    tokens = extract_keywords(prompt)
    logger.debug(f"Extracted tokens: {tokens}")
    
    # Priority matches based on common question patterns
    common_patterns = {
        'job': ['job', 'career', 'position', 'employment', 'work', 'hire', 'hiring'],
        'cyberchallenges': ['challenge', 'ctf', 'puzzle', 'problem', 'task'],
        'blogpost': ['blog', 'post', 'article', 'news', 'update'],
        'skill': ['skill', 'ability', 'competency', 'expertise'],
        'course': ['course', 'class', 'training', 'education'],
        'announcement': ['announcement', 'notice', 'update', 'news'],
        'webpage': ['page', 'website', 'site', 'web', 'appattack', 'malware', 'ptgui', 'smishing', 'vr', 'cybersafe', 'threatmirror'],
        'project': ['project', 'appattack', 'malware', 'pt-gui', 'smishing', 'vr', 'cybersafe', 'threatmirror']
    }
    
    # Check for pattern matches first
    for token in tokens:
        for model_key, patterns in common_patterns.items():
            if token in patterns and model_key in models:
                logger.info(f"Found pattern match for token '{token}' -> model '{model_key}'")
                return models[model_key]
    
    # Try direct matching
    for token in tokens:
        if token in models:
            logger.info(f"Found direct model match for token '{token}': {models[token].__name__}")
            return models[token]
    
    # Try with spelling correction
    for token in tokens:
        corrected_token = correct_spelling(token)
        if corrected_token in models:
            logger.info(f"Found spell-corrected model match: '{token}' -> '{corrected_token}': {models[corrected_token].__name__}")
            return models[corrected_token]
    
    # Check for partial matches
    for token in tokens:
        for model_name in models.keys():
            if token in model_name or model_name in token:
                logger.info(f"Found partial model match: '{token}' matches '{model_name}': {models[model_name].__name__}")
                return models[model_name]
    
    # Try to match against project names
    project_patterns = ['appattack', 'malware', 'pt-gui', 'smishing', 'vr', 'cybersafe', 'threatmirror']
    for token in tokens:
        if token.lower() in project_patterns:
            if 'webpage' in models:
                logger.info(f"Found project name match: '{token}' -> using Webpage model")
                return models['webpage']
            elif 'project' in models:
                logger.info(f"Found project name match: '{token}' -> using Project model")
                return models['project']
    
    # Default to BlogPost for general queries
    default_model = models.get('blogpost')
    if default_model:
        logger.info("No specific model found, defaulting to BlogPost")
        return default_model
    
    # If no BlogPost, try Webpage as fallback
    fallback_model = models.get('webpage')
    if fallback_model:
        logger.info("No BlogPost found, using Webpage as fallback")
        return fallback_model
    
    logger.warning("No matching model found and no default models available")
    return None


def analyze_model_fields(model: Model) -> Dict[str, List[str]]:
    """
    Analyze a model's fields and categorize them by type and importance.
    Returns a dictionary of field categories.
    """
    field_categories = {
        'primary': [],      # Primary identifying fields (title, name, code)
        'content': [],      # Content fields (description, content, text)
        'metadata': [],     # Metadata fields (created_at, status, category)
        'searchable': [],   # All text-searchable fields
        'display': [],      # Fields suitable for display
        'date': [],        # Date/time fields
        'boolean': [],     # Boolean fields
        'numeric': []      # Numeric fields
    }
    
    # Common field patterns
    primary_patterns = ['title', 'name', 'code', 'id', 'slug']
    content_patterns = ['content', 'description', 'text', 'body', 'answer', 'question']
    metadata_patterns = ['status', 'category', 'type', 'tags', 'keywords']
    
    for field in model._meta.fields:
        field_name = field.name
        field_type = field.get_internal_type()
        
        # Categorize by field type
        if isinstance(field, (CharField, TextField)):
            field_categories['searchable'].append(field_name)
            
            # Categorize by field name patterns
            if any(pattern in field_name.lower() for pattern in primary_patterns):
                field_categories['primary'].append(field_name)
            elif any(pattern in field_name.lower() for pattern in content_patterns):
                field_categories['content'].append(field_name)
            elif any(pattern in field_name.lower() for pattern in metadata_patterns):
                field_categories['metadata'].append(field_name)
            
            field_categories['display'].append(field_name)
            
        elif isinstance(field, DateTimeField):
            field_categories['date'].append(field_name)
        elif isinstance(field, BooleanField):
            field_categories['boolean'].append(field_name)
        elif isinstance(field, IntegerField):
            field_categories['numeric'].append(field_name)
    
    logger.debug(f"Field categories for {model.__name__}: {field_categories}")
    return field_categories


def format_model_result(result: Model, field_categories: Dict[str, List[str]]) -> Dict[str, Any]:
    """Format a model instance result with all fields."""
    formatted = {
        'model': result._meta.model_name,
        'id': result.id
    }
    
    # Include all fields and their values
    for field in result._meta.fields:
        field_name = field.name
        formatted[field_name] = getattr(result, field_name)
        
    # Add related manager instances if they exist
    for rel in result._meta.related_objects:
        if hasattr(result, rel.get_accessor_name()):
            related = getattr(result, rel.get_accessor_name()).all()
            if related.exists():
                formatted[rel.name] = [r.id for r in related]
    
    return formatted


def _format_result_item(item: Dict[str, Any]) -> Dict[str, Any]:
    """Format a single result item with all fields."""
    return item  # Now returns the complete item


def perform_search(prompt: str) -> list[Any]:
    """
    Identify the target model and return queryset filtered by prompt keywords.
    Enhanced with TextBlob for more effective searching and smart field handling.
    """
    logger.info(f"Performing search for prompt: '{prompt}'")
    
    try:
        models_map = initialize_search_engine()
        model = identify_model_from_prompt(prompt, models_map)
        
        if not model:
            logger.warning("No suitable model found for search")
            return []
        
        logger.info(f"Using model: {model.__name__}")
        
        # Analyze model fields
        field_categories = analyze_model_fields(model)
        logger.debug(f"Analyzed fields for {model.__name__}")
        
        # Extract keywords with TextBlob
        keywords = extract_keywords(prompt)
        logger.debug(f"Extracted keywords: {keywords}")
        
        # Check if this is a model-only query
        model_name = model.__name__.lower()
        model_verbose_name = model._meta.verbose_name.lower()
        model_variations = {
            model_name,
            f"{model_name}s",
            model_name[:-1] + "ies" if model_name.endswith('y') else f"{model_name}s",
            model_verbose_name,
            f"{model_verbose_name}s",
        }
        
        if len(keywords) == 1 and keywords[0].lower() in model_variations:
            logger.info("Model-only query detected - returning 3 most recent items")
            
            # Determine best ordering field
            order_field = None
            # Try primary date fields first
            for field in ['updated_at', 'created_at', 'last_updated', 'timestamp']:
                if field in field_categories['date']:
                    order_field = f'-{field}'
                    logger.debug(f"Using date field for ordering: {field}")
                    break
            
            # Fallback to priority if available
            if not order_field and 'priority' in field_categories['numeric']:
                order_field = '-priority'
                logger.debug("Using priority field for ordering")
            
            # Final fallback to ID
            if not order_field:
                order_field = '-id'
                logger.debug("Using ID for ordering")
            
            results = list(model.objects.all().order_by(order_field)[:3])
            
            # Format results with relevant fields
            formatted_results = []
            for result in results:
                formatted = format_model_result(result, field_categories)
                formatted_results.append(formatted)
                logger.debug(f"Formatted result: {formatted}")
            
            return formatted_results
        
        # If not a model-only query, build search conditions
        q_objects = Q()
        
        # Special handling for project-related searches
        project_patterns = ['appattack', 'malware', 'pt-gui', 'smishing', 'vr', 'cybersafe', 'threatmirror']
        is_project_search = any(pattern in prompt.lower() for pattern in project_patterns)
        
        if is_project_search:
            # If searching for project info, prioritize Project and Webpage models
            if model.__name__.lower() in ['project', 'webpage']:
                # Search in all text fields
                for field in field_categories['searchable']:
                    for kw in keywords:
                        q_objects |= Q(**{f"{field}__icontains": kw})
                
                # For webpages, also search in URL field
                if model.__name__.lower() == 'webpage':
                    for kw in keywords:
                        q_objects |= Q(url__icontains=kw)
                
                # For projects, search in title field
                if model.__name__.lower() == 'project':
                    for kw in keywords:
                        q_objects |= Q(title__icontains=kw)
        else:
            # Regular search in primary fields first
            for field in field_categories['primary']:
                for kw in keywords:
                    q_objects |= Q(**{f"{field}__icontains": kw})
            
            # Then search in content fields
            for field in field_categories['content']:
                for kw in keywords:
                    q_objects |= Q(**{f"{field}__icontains": kw})
            
            # Finally search in metadata fields
            for field in field_categories['metadata']:
                for kw in keywords:
                    q_objects |= Q(**{f"{field}__icontains": kw})
        
        logger.debug(f"Built query conditions: {str(q_objects)}")
        
        # Execute search
        results = list(model.objects.filter(q_objects).distinct())
        
        # If no results found in primary model and it's a project search,
        # try the other project-related model
        if not results and is_project_search:
            alternate_model = None
            if model.__name__.lower() == 'project':
                alternate_model = models_map.get('webpage')
            elif model.__name__.lower() == 'webpage':
                alternate_model = models_map.get('project')
            
            if alternate_model:
                logger.info(f"No results found, trying alternate model: {alternate_model.__name__}")
                alt_field_categories = analyze_model_fields(alternate_model)
                alt_q_objects = Q()
                
                # Search in all text fields of alternate model
                for field in alt_field_categories['searchable']:
                    for kw in keywords:
                        alt_q_objects |= Q(**{f"{field}__icontains": kw})
                
                results = list(alternate_model.objects.filter(alt_q_objects).distinct())
        
        # Format results with relevant fields
        formatted_results = []
        for result in results:
            formatted = format_model_result(result, field_categories)
            formatted_results.append(formatted)
            if formatted_results:
                logger.debug(f"First formatted result: {formatted_results[0]}")
        
        return formatted_results
        
    except Exception as e:
        logger.error(f"Search error: {str(e)}", exc_info=True)
        return []


def verify_search_connection() -> dict:
    """
    Verify that the search engine can connect to models and perform a basic search.
    Returns a status dictionary with details about the connection.
    """
    try:
        # Test model initialization
        models_map = initialize_search_engine()
        
        if not models_map:
            return {
                "status": "warning",
                "message": "Search engine initialized but no models were loaded"
            }
            
        # Try a basic search
        test_search = perform_search("test")
        
        return {
            "status": "success",
            "message": "Search engine is connected and operational",
            "models_count": len(models_map)
        }
        
    except Exception as e:
        logger.error(f"Search engine connection error: {str(e)}")
        return {
            "status": "error",
            "message": f"Could not connect to search engine: {str(e)}"
        }


def format_search_results(results: Dict[str, Any], query: str, format_type: str = 'rich') -> Dict[str, Any]:
    """Format search results for display.
    
    Args:
        results: Dictionary containing search results or error message
        query: Original search query string
        format_type: Type of formatting to apply ('rich' or 'markdown')
        
    Returns:
        Dictionary containing formatted results and metadata
    """
    from .result_formatter import format_search_results_rich, format_as_markdown
    
    formatted = {
        'query': query,
        'total': len(results.get('results', [])) if isinstance(results, dict) else 0,
        'timestamp': timezone.now().isoformat(),
        'results': []
    }
    
    # Copy any error message
    if isinstance(results, dict) and 'error' in results:
        formatted['error'] = results['error']
        return formatted

    # Delegate formatting to result_formatter.py based on format type
    if format_type == 'rich':
        formatted['display_text'] = format_search_results_rich(results, query)
    elif format_type == 'markdown':
        formatted['display_text'] = format_as_markdown(results, query)
    else:
        # Plain text format - keep existing logic for backward compatibility
        if isinstance(results, dict) and 'results' in results:
            formatted['results'] = [
                _format_result_item(item) for item in results['results']
            ]
    
    return formatted

