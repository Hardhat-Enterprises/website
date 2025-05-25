# Import necessary libraries
from textblob import TextBlob  # For text processing and NLP tasks
from typing import Dict, Any, List, Tuple, Optional  # For type hinting
import logging  # For logging errors and information
from langdetect import detect  # For language detection

# Set up logger for this module
logger = logging.getLogger(__name__)


def analyze_sentiment(text: str) -> Dict[str, float]:
    """
    Analyze sentiment of text, returning polarity and subjectivity scores.
    
    Args:
        text (str): The input text to analyze.

    Returns:
        Dict[str, float]: Dictionary with 'polarity' and 'subjectivity' scores.
            - Polarity: -1.0 (negative) to 1.0 (positive)
            - Subjectivity: 0.0 (objective) to 1.0 (subjective)
    """
    blob = TextBlob(text)  # Create a TextBlob object for NLP tasks
    return {
        'polarity': blob.sentiment.polarity,  # Sentiment polarity score
        'subjectivity': blob.sentiment.subjectivity  # Sentiment subjectivity score
    }


def extract_noun_phrases(text: str) -> List[str]:
    """
    Extract noun phrases from the text using TextBlob's noun phrase extraction.

    Args:
        text (str): The input text to process.

    Returns:
        List[str]: List of noun phrases found in the text.
    """
    blob = TextBlob(text)
    return list(blob.noun_phrases)


def correct_spelling(text: str) -> str:
    """
    Attempt to correct spelling in the text using TextBlob's spelling correction.
    Note: This is relatively slow for longer texts.

    Args:
        text (str): The input text to correct.

    Returns:
        str: The text with corrected spelling.
    """
    blob = TextBlob(text)
    return str(blob.correct())


def get_pos_tags(text: str) -> List[Tuple[str, str]]:
    """
    Perform part-of-speech tagging on the text.
    Returns list of (word, tag) tuples.

    Args:
        text (str): The input text to tag.

    Returns:
        List[Tuple[str, str]]: List of (word, POS tag) tuples.
    """
    blob = TextBlob(text)
    return blob.tags


def translate_text(text: str, from_lang: str='auto', to_lang: str='en') -> Optional[str]:
    """
    Translate text from one language to another using TextBlob's translation.
    Default behavior detects language and translates to English.

    Args:
        text (str): The input text to translate.
        from_lang (str, optional): Source language code. Defaults to 'auto' (auto-detect).
        to_lang (str, optional): Target language code. Defaults to 'en' (English).

    Returns:
        Optional[str]: Translated text, or None if translation fails.
    """
    try:
        blob = TextBlob(text)
        return str(blob.translate(from_lang=from_lang, to_lang=to_lang))
    except Exception as e:
        logger.error(f"Translation error: {e}")  # Log translation errors
        return None


def tokenize_text(text: str) -> List[str]:
    """
    Tokenize text into words using TextBlob's word tokenizer.

    Args:
        text (str): The input text to tokenize.

    Returns:
        List[str]: List of word tokens.
    """
    blob = TextBlob(text)
    return list(blob.words)


def detect_language(text: str) -> str:
    """
    Detect the language of the input text using langdetect.
    Returns ISO 639-1 language code.

    Args:
        text (str): The input text to analyze.

    Returns:
        str: Detected language code (e.g., 'en' for English).
    """
    try:
        return detect(text)
    except:
        # Fallback to assuming English if detection fails
        return 'en'


def analyze_text(text: str) -> Dict[str, Any]:
    """
    Perform comprehensive text analysis using TextBlob.
    Returns a dictionary with sentiment, noun phrases, POS tags, tokens, and word counts.

    Args:
        text (str): The input text to analyze.

    Returns:
        Dict[str, Any]: Dictionary containing various text analysis results:
            - 'sentiment': {'polarity', 'subjectivity'}
            - 'noun_phrases': list of noun phrases
            - 'pos_tags': list of (word, POS tag) tuples
            - 'tokens': list of word tokens
            - 'word_counts': word frequency dictionary
    """
    blob = TextBlob(text)
    
    return {
        'sentiment': {
            'polarity': blob.sentiment.polarity,
            'subjectivity': blob.sentiment.subjectivity
        },
        'noun_phrases': list(blob.noun_phrases),
        'pos_tags': blob.tags,
        'tokens': list(blob.words),
        'word_counts': blob.word_counts,
    } 