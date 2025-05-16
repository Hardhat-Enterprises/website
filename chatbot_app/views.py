from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.conf import settings
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
import json, uuid, logging
from jinja2 import Environment, FileSystemLoader

from .models import ChatSession, ChatMessage
from .search_engine import extract_keywords, perform_search, verify_search_connection
from .textblob_analyzer import (
    analyze_sentiment, 
    extract_noun_phrases, 
    correct_spelling, 
    analyze_text,
    detect_language
)
from .debug_logger import setup_debug_logging

# Set up enhanced debug logging
logger = setup_debug_logging()

# Initialize Jinja2 environment for response templates
jinja_env = Environment(loader=FileSystemLoader('chatbot_app/templates/chatbot_app'))
response_template = jinja_env.get_template('chatbot_response_templates.j2')


def chat_view(request):
    """Render the main chat UI."""
    return render(request, 'chatbot_app/chat.html', {
        'page_title': 'Chat with Hardie Hat',
        'chatbot_server_url': request.build_absolute_uri('/chatbot')
    })


@csrf_exempt
@require_http_methods(["GET"])
def verify_connection_api(request):
    """
    Verify that the chatbot is connected and operational.
    This endpoint is used to check if the chatbot services are available.
    """
    try:
        # Check search engine connectivity
        search_status = verify_search_connection()
        
        # Get current timestamp
        current_time = timezone.now().isoformat()
        
        # Return status information
        if search_status["status"] == "success":
            return JsonResponse({
                "status": "success",
                "message": "Chatbot is connected and ready",
                "timestamp": current_time,
                "search_engine": search_status
            })
        else:
            return JsonResponse({
                "status": "warning",
                "message": "Chatbot is partially operational",
                "timestamp": current_time,
                "search_engine": search_status
            })
            
    except Exception as e:
        logger.error(f"Chatbot connection verification error: {str(e)}")
        return JsonResponse({
            "status": "error",
            "message": f"Chatbot connection error: {str(e)}",
            "timestamp": timezone.now().isoformat()
        }, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def session_create_api(request):
    """Create a new chat session and return its ID."""
    try:
        # Create new session
        new_session = ChatSession.objects.create(
            session_id=str(uuid.uuid4()),
            user=request.user if request.user.is_authenticated else None
        )
        
        # Return session info
        return JsonResponse({
            'session_id': new_session.session_id,
            'created_at': new_session.created_at.isoformat(),
            'status': 'active'
        }, status=201)
    except Exception as e:
        logger.error(f"Error creating chat session: {str(e)}")
        return JsonResponse({
            'status': 'error',
            'message': 'Failed to create chat session'
        }, status=500)


@csrf_exempt
@require_http_methods(["GET"])
def session_detail_api(request, session_id):
    """Return session metadata."""
    try:
        session = get_object_or_404(ChatSession, session_id=session_id)
        
        # Check if session is expired (more than 24 hours old)
        if (timezone.now() - session.last_interaction).total_seconds() > 86400:
            session.is_active = False
            session.save()
        
        return JsonResponse({
            'session_id': session.session_id,
            'created_at': session.created_at.isoformat(),
            'last_interaction': session.last_interaction.isoformat(),
            'is_active': session.is_active,
            'message_count': session.messages.count()
        })
    except ObjectDoesNotExist:
        return JsonResponse({
            'status': 'error',
            'message': 'Session not found'
        }, status=404)
    except Exception as e:
        logger.error(f"Error getting session details: {str(e)}")
        return JsonResponse({
            'status': 'error',
            'message': 'Failed to get session details'
        }, status=500)


def format_search_result(result: dict) -> str:
    """Format a search result dictionary into a readable response using Jinja2 templates."""
    try:
        # Determine the model type from the result
        model_type = result.get('model', '').lower()
        
        # Map model types to template macros
        macro_mapping = {
            'cyberchallenge': lambda r: response_template.module.cyber_challenge(
                title=r.get('title', ''),
                category=r.get('category', ''),
                points=r.get('points', 0),
                difficulty=r.get('difficulty', ''),
                description=r.get('description', ''),
                # These fields are required by the macro signature but won't be displayed
                question='',
                choices={},
                correct_answer='',
                explanation=''
            ),
            'announcement': lambda r: response_template.module.announcement(
                message=r.get('message', ''),
                isActive=r.get('isActive', False),
                created_at=r.get('created_at', '')
            ),
            'article': lambda r: response_template.module.article(
                title=r.get('title', ''),
                date=r.get('date', ''),
                author=r.get('author', ''),
                featured=r.get('featured', False),
                likes=r.get('likes', 0),
                content=r.get('content', '')
            ),
            'contact': lambda r: response_template.module.contact(
                name=r.get('name', ''),
                email=r.get('email', ''),
                message=r.get('message', '')
            ),
            'course': lambda r: response_template.module.course(
                title=r.get('title', ''),
                code=r.get('code', ''),
                is_postgraduate=r.get('is_postgraduate', False)
            ),
            'job': lambda r: response_template.module.job(
                title=r.get('title', ''),
                location=r.get('location', ''),
                posted_date=r.get('posted_date', ''),
                closing_date=r.get('closing_date', ''),
                job_type=r.get('job_type', ''),
                description=r.get('description', '')
            ),
            'project': lambda r: response_template.module.project(
                title=r.get('title', ''),
                id=r.get('id', '')
            ),
            'skill': lambda r: response_template.module.skill(
                name=r.get('name', ''),
                description=r.get('description', ''),
                slug=r.get('slug', '')
            ),
            'webpage': lambda r: response_template.module.webpage(
                title=r.get('title', ''),
                url=r.get('url', ''),
                id=r.get('id', '')
            )
        }
        
        # Get the appropriate formatting function
        format_func = macro_mapping.get(model_type)
        if format_func:
            # Call the formatting function with the result data
            return format_func(result)
        
        # Fallback to basic formatting if no matching template
        logger.warning(f"No template found for model type: {model_type}")
        formatted_parts = []
        for key, value in result.items():
            if key != 'model':
                if isinstance(value, dict):
                    formatted_parts.append(f"{key}:")
                    for k, v in value.items():
                        formatted_parts.append(f"  {k}: {v}")
                else:
                    formatted_parts.append(f"{key}: {value}")
        return "\n".join(formatted_parts)
        
    except Exception as e:
        logger.error(f"Error formatting search result: {str(e)}")
        return str(result)


@csrf_exempt
@require_http_methods(["POST"])
def message_api(request, session_id):
    """Handle an incoming user message, perform search, and reply."""
    try:
        logger.info(f"Processing new message for session {session_id}")
        
        # Get session
        try:
            session = ChatSession.objects.get(session_id=session_id)
            logger.debug(f"Found active session: {session_id}")
            
            # Check if session is expired
            if (timezone.now() - session.last_interaction).total_seconds() > 86400:
                session.is_active = False
                session.save()
                logger.warning(f"Session {session_id} has expired")
                raise ObjectDoesNotExist("Session expired")
                
            if not session.is_active:
                logger.warning(f"Session {session_id} is inactive")
                raise ObjectDoesNotExist("Session inactive")
        except ObjectDoesNotExist:
            return JsonResponse({
                'status': 'error',
                'message': 'No active session found'
            }, status=404)
        
        # Parse request data
        try:
            data = json.loads(request.body)
            message_text = data.get('message', '').strip()
            user_info = data.get('user_info', {})
            
            logger.info(f"Received message: '{message_text}'")
            
            if not message_text:
                logger.warning("Empty message received")
                return JsonResponse({
                    'status': 'error',
                    'message': 'Message cannot be empty'
                }, status=400)
        except json.JSONDecodeError:
            logger.error("Invalid JSON data received")
            return JsonResponse({
                'status': 'error',
                'message': 'Invalid JSON data'
            }, status=400)
        
        # Save user message
        user_message = ChatMessage.objects.create(
            session=session,
            sender='user',
            message=message_text,
            timestamp=timezone.now()
        )
        logger.debug(f"Saved user message (ID: {user_message.id})")
        
        # Process message and generate response
        try:
            # Analyze message
            logger.info("Starting message analysis")
            sentiment = analyze_sentiment(message_text)
            logger.debug(f"Sentiment analysis: {sentiment}")
            
            noun_phrases = extract_noun_phrases(message_text)
            logger.debug(f"Extracted noun phrases: {noun_phrases}")
            
            spelling_corrected = correct_spelling(message_text)
            if spelling_corrected != message_text:
                logger.debug(f"Spelling corrected: '{message_text}' -> '{spelling_corrected}'")
            
            language = detect_language(message_text)
            logger.debug(f"Detected language: {language}")
            
            # Perform search with original message text
            logger.info("Initiating search")
            search_results = perform_search(message_text)
            logger.info(f"Search completed: {len(search_results)} results found")
            
            # Generate reply based on search results
            if search_results:
                # Format each result and combine them
                formatted_responses = []
                for i, result in enumerate(search_results, 1):
                    if len(search_results) > 1:
                        formatted_responses.append(f"\nResult {i}:")
                    formatted_responses.append(format_search_result(result))
                
                reply = "\n".join(formatted_responses)
                logger.debug(f"Generated formatted reply with {len(search_results)} results")
            else:
                reply = "I apologize, but I couldn't find specific information matching your query. Could you try rephrasing your question?"
                logger.warning(f"No search results found for query: {message_text}")
            
            # Save bot reply with analysis data
            analysis_data = {
                'sentiment': sentiment,
                'noun_phrases': noun_phrases,
                'spelling_corrected': spelling_corrected,
                'detected_language': language,
                'search_success': bool(search_results)
            }
            
            bot_message = ChatMessage.objects.create(
                session=session,
                sender='bot',
                message=reply,
                metadata=analysis_data,
                timestamp=timezone.now()
            )
            
            # Update session
            session.last_interaction = timezone.now()
            session.save()
            
            return JsonResponse({
                'response': reply,
                'message_id': bot_message.id,
                'timestamp': bot_message.timestamp.isoformat()
            })
            
        except Exception as e:
            logger.error(f"Error processing message for session {session_id}: {str(e)}", exc_info=True)
            return JsonResponse({
                'status': 'error',
                'message': 'Failed to process message. Please try again.'
            }, status=500)
            
    except Exception as e:
        logger.error(f"Unexpected error in message_api: {str(e)}")
        return JsonResponse({
            'status': 'error',
            'message': 'An unexpected error occurred'
        }, status=500)


def analyze_fuzzy_search(request):
    """Render a page to test fuzzy search behavior."""
    return render(request, 'chatbot_app/fuzzy_search.html')


@csrf_exempt
@require_http_methods(["POST"])
def analyze_text_api(request):
    """API endpoint to analyze text using TextBlob."""
    data = json.loads(request.body)
    text = data.get('text', '')
    
    if not text:
        return JsonResponse({'error': 'No text provided'}, status=400)
    
    analysis = analyze_text(text)
    
    return JsonResponse({
        'analysis': analysis,
    })


@csrf_exempt
@require_http_methods(["GET"])
def chatbot_config_api(request):
    """
    Provide configuration data for the chatbot.
    This helps frontend code initialize with the right settings.
    """
    config = {
        'server_url': request.build_absolute_uri('/chatbot'),
        'api_endpoints': {
            'verify': request.build_absolute_uri('/chatbot/api/verify/'),
            'create_session': request.build_absolute_uri('/chatbot/api/session/create/'),
            'session_detail': request.build_absolute_uri('/chatbot/api/session/{session_id}/'),
            'send_message': request.build_absolute_uri('/chatbot/api/session/{session_id}/message/'),
        },
        'bot_name': 'Hardie Hat',
        'version': '1.0',
        'timestamp': timezone.now().isoformat()
    }
    
    return JsonResponse(config)
