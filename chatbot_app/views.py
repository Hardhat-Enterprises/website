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

# Add default project responses mapping
project_responses = {
    'appattack': """Oh, you're interested in AppAttack? That's awesome! 🚀 AppAttack is perfect for anyone who's passionate
    about web security and application development. It's like a playground for learning about real-world vulnerabilities!<br>
    <br>Here's what makes it special:
    <br>• 🎯 Interactive challenges that feel like real-world scenarios<br>
    • 📊 Progress tracking to see how you're improving<br>
    • 👥 Team collaboration features to learn with others<br>
    • 💡 Detailed feedback to help you grow<br>
    • 🛡️ Real-world vulnerability testing<br>
    • 🔍 Hands-on security experience<br>
    <br>🎯 Perfect for:
    <br>• Web developers<br>
    • Security enthusiasts<br>
    • Problem solvers<br>
    • Team players<br>
    • Anyone interested in web security!<br>
    <br>🔗 <a href="/appattack/" class="learn-more-link">Learn more here</a>
    <br>Want to get involved? Sign Up via this link <a href="/accounts/register/">Register here</a>""",

    'pt_gui': """Oh, you're interested in the Deakin Detonator Toolkit (DDT)? That's fantastic! 🛠️ This project is perfect for those who want to get hands-on with penetration testing in a user-friendly way. It's like having a Swiss Army knife for security testing!<br>
    <br>Here's what makes DDT special:
    <br>• 🎯 44+ pen-testing tools at your fingertips<br>
    • 💻 User-friendly GUI interface<br>
    • 🚀 Built with Tauri, React, and Mantine<br>
    • 🐍 Python-powered automation<br>
    • 📚 12 HackTheBox walkthroughs included<br>
    • 🔧 Streamlined workflow automation<br>
    <br>🎯 Key Features:
    <br>• Automated vulnerability scanning<br>
    • Manual testing tools<br>
    • Report generation<br>
    • Simplified command execution<br>
    • Interactive tool interfaces<br>
    • Comprehensive documentation<br>
    <br>💪 Available Tools Include:
    <br>• Nmap for network scanning<br>
    • SMB Enumeration tools<br>
    • Shodan API integration<br>
    • JohnTheRipper & Hashcat<br>
    • Hydra for password attacks<br>
    • Many more security tools!<br>
    <br>🔗 <a href="/ptgui_viz/" class="learn-more-link">Learn more here</a>
    <br>Want to get involved? Sign Up via this link <a href="/accounts/register/">Register here</a>""",

    
    'smishing_detection': """Ah, Smishing Detection! 🛡️ This is a super relevant project in today's mobile-first world. We're revolutionizing mobile security!<br>
    <br>Here's what makes it exciting:
    <br>• 🔍 AI-powered SMS threat detection<br>
    • 📱 Works on both Android and iOS<br>
    • ⚡ Real-time protection<br>
    • 🤖 Machine learning algorithms<br>
    • 🛡️ User-friendly security<br>
    • 🌐 Global anti-scam initiative<br>
    <br>🎯 Key Features:
    <br>• Real-time SMS analysis<br>
    • Machine learning detection<br>
    • Instant threat notifications<br>
    • Smart message analysis<br>
    • Educational resources<br>
    • User-friendly interface<br>
    <br>💪 What it protects against:
    <br>• Phishing SMS attempts<br>
    • Malicious URLs<br>
    • Scam messages<br>
    • Social engineering attacks<br>
    • Data theft attempts<br>
    <br>🔗 <a href="/smishing_detection/" class="learn-more-link">Learn more here</a>
    <br>Want to get involved? <a href="/accounts/register/" class="learn-more-link">Sign up here</a>""",
    
    'malware_visualization': """Oh, you're curious about Malware Visualization? That's awesome! 🔍🔮<br>
    <br>🚨 Malware Visualization is like the Sherlock Holmes of cybersecurity — it helps you see the invisible threats hiding in your system through smart, interactive visual tools. Whether you're a cyber pro or just malware-curious, this platform gives you the power to uncover and understand malware patterns in a whole new way.<br>
    <br>Here's what makes it special:
    <br>• 📊 User-friendly visual analysis of malware activity<br>
    • 🤖 AI-enhanced detection for both known and novel threats<br>
    • 💡 No need for deep technical expertise to get started<br>
    • 🌐 Integrates with tools like MapBox & Leaflet.js for dynamic interaction<br>
    • 📈 A dashboard preview that shows malware trends clearly<br>
    • 💪 Built to foster collaboration within the security community<br>
    <br>🚨 Project Goals include:
    <br>• Creating a sleek, powerful tool for malware analysis<br>
    • Improving how threats are found and removed<br>
    • Making cybersecurity more accessible and efficient<br>
    • Encouraging tech community involvement<br>
    <br>🔗 <a href="/malware_viz/" class="learn-more-link">Learn more here</a>
    <br>Want to get involved? <a href="/accounts/register/" class="learn-more-link">Sign up here</a>""",
   
   'vr': """VR Security Training? Now we're talking! 🎮 This is perfect for those who want to experience cybersecurity training in a whole new dimension. It's like being in a cybersecurity action movie!<br>
    <br>Here's what makes it revolutionary:
    <br>• 🕶️ Immersive VR learning experiences<br>
    • 🎯 Real-world scenario simulations<br>
    • 🏢 Small business focused training<br>
    • 🛡️ Interactive security challenges<br>
    • 📚 Comprehensive learning modules<br>
    • 🤝 Industry-aligned content<br>
    <br>🎯 Training Modules:
    <br>• Password security mastery<br>
    • Data encryption practices<br>
    • Network security setup<br>
    • Safe web browsing habits<br>
    • Phishing attack recognition<br>
    • Wi-Fi security configuration<br>
    <br>💪 Key Benefits:
    <br>• Virtual security scenarios<br>
    • Hands-on training<br>
    • Team-based challenges<br>
    • Progress tracking<br>
    • Real-time feedback<br>
    • Measurable outcomes<br>
    <br>🔗 <a href="/vr/" class="learn-more-link">Learn more here</a>
    <br>Want to get involved? <a href="/accounts/register/" class="learn-more-link">Sign up here</a>""",
    
    'deakin_threat_mirror': """DeakinThreatmirror? Now that's a fascinating project! 🎯 It's perfect for those who love turning complex data into beautiful, understandable visualizations. Think of it as a crystal ball for cybersecurity threats!<br>
    <br>Here's what makes it special:
    <br>• 🎯 Open-source threat intelligence platform<br>
    • 📊 Advanced visual analytics for threat data<br>
    • 🤖 Machine learning-powered insights<br>
    • 🌐 Perfect for SMEs and developing economies<br>
    • 💡 User-friendly interface for complex data<br>
    • 🔄 Real-time threat feed aggregation<br>
    <br>🎯 Project Goals:
    <br>• Revolutionize threat analysis and understanding<br>
    • Make cybersecurity accessible for smaller organizations<br>
    • Transform raw data into actionable intelligence<br>
    • Support developing economies with cost-effective solutions<br>
    <br>💪 Key Benefits:
    <br>• Real-time threat data visualization<br>
    • Interactive maps and dashboards<br>
    • Customizable threat analysis<br>
    • Cost-effective solutions<br>
    • Easy-to-understand insights<br>
    • Community-driven development<br>
    <br>🔗 <a href="/deakinThreatmirror/" class="learn-more-link">Learn more here</a>
    <br>Want to get involved? <a href="/accounts/register/" class="learn-more-link">Sign up here</a>""",
}


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
        # Override mapping for project and webpage results
        model_type = result.get('model', '').lower()
        if model_type in ['project', 'webpage']:
            raw_key = result.get('title', '') if model_type == 'project' else result.get('url', '')
            key = raw_key.lower().replace('-', '_').replace(' ', '_')
            if key in project_responses:
                return project_responses[key]
            # Fallback: if no direct project_responses key, match keys that start with this key + '_'
            for resp_key in project_responses:
                if resp_key.startswith(key + "_"):
                    return project_responses[resp_key]
        
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


@csrf_exempt
@require_http_methods(["POST"])
def general_message_api(request):
    """
    Process messages without requiring a session ID in the URL.
    Creates or retrieves a session based on sender ID in the request.
    """
    try:
        # Parse request data
        try:
            data = json.loads(request.body)
            message_text = data.get('message', '')
            sender_id = data.get('sender', None)
        except (json.JSONDecodeError, TypeError):
            return JsonResponse({
                'status': 'error',
                'message': 'Invalid request format'
            }, status=400)
            
        if not message_text:
            return JsonResponse({
                'status': 'error',
                'message': 'Message is required'
            }, status=400)
            
        # Find or create session based on sender ID
        if sender_id:
            try:
                session, created = ChatSession.objects.get_or_create(
                    session_id=sender_id,
                    defaults={'is_active': True}
                )
            except Exception as db_error:
                logger.error(f"Database error when getting/creating session: {str(db_error)}", exc_info=True)
                return JsonResponse({
                    'status': 'error',
                    'message': 'Database error when processing session',
                    'error_type': 'database_error',
                    'detail': str(db_error)
                }, status=500)
        else:
            # Create a new session if sender ID not provided
            try:
                session = ChatSession.objects.create(
                    session_id=str(uuid.uuid4()),
                    is_active=True
                )
            except Exception as db_error:
                logger.error(f"Database error when creating new session: {str(db_error)}", exc_info=True)
                return JsonResponse({
                    'status': 'error',
                    'message': 'Database error when creating new session',
                    'error_type': 'database_error',
                    'detail': str(db_error)
                }, status=500)
            
        # Update last interaction time
        try:
            session.last_interaction = timezone.now()
            session.save()
        except Exception as db_error:
            logger.error(f"Database error when updating session: {str(db_error)}", exc_info=True)
            return JsonResponse({
                'status': 'error',
                'message': 'Database error when updating session',
                'error_type': 'database_error',
                'detail': str(db_error)
            }, status=500)
        
        # Store the user message
        try:
            ChatMessage.objects.create(
                session=session,
                sender='user',
                message=message_text,
                timestamp=timezone.now()
            )
        except Exception as db_error:
            logger.error(f"Database error when storing user message: {str(db_error)}", exc_info=True)
            return JsonResponse({
                'status': 'error',
                'message': 'Database error when storing user message',
                'error_type': 'database_error',
                'detail': str(db_error)
            }, status=500)
        
        # Process message and get response
        # Extract keywords for search
        try:
            keywords = extract_keywords(message_text)
            logger.debug(f"Extracted keywords: {keywords}")
        except Exception as search_error:
            logger.error(f"Error extracting keywords: {str(search_error)}", exc_info=True)
            return JsonResponse({
                'status': 'error',
                'message': 'Error analyzing message',
                'search_error': str(search_error)
            }, status=500)
        
        # Perform search with extracted keywords
        try:
            # Instead of passing keywords directly, pass the original message text
            # to avoid list strip() issue in perform_search
            search_results = perform_search(message_text, limit=3)
            logger.debug(f"Search results: {search_results}")
        except Exception as search_error:
            logger.error(f"Error in search engine: {str(search_error)}", exc_info=True)
            return JsonResponse({
                'status': 'error',
                'message': 'Error searching database',
                'search_error': str(search_error)
            }, status=500)
        
        # Prepare response based on search results
        try:
            # Format search results - perform_search now returns a list of dictionaries
            if search_results and isinstance(search_results, list):
                # Format search result
                formatted_results = []
                for result in search_results:
                    formatted_result = format_search_result(result)
                    if formatted_result:
                        formatted_results.append(formatted_result)
                
                # Join formatted results
                if formatted_results:
                    response_text = "\n\n".join(formatted_results)
                else:
                    response_text = "I found some information, but couldn't format it properly."
            else:
                response_text = "I'm sorry, I couldn't find relevant information for your query."
        
            # Store the bot response
            try:
                ChatMessage.objects.create(
                    session=session,
                    sender='bot',
                    message=response_text,
                    timestamp=timezone.now()
                )
            except Exception as db_error:
                logger.error(f"Database error when storing bot response: {str(db_error)}", exc_info=True)
                # Continue anyway to return response to user
            
            # Return response
            return JsonResponse({
                'status': 'success',
                'response': response_text,
                'sender_id': session.session_id
            })
        except Exception as format_error:
            logger.error(f"Error formatting search results: {str(format_error)}", exc_info=True)
            return JsonResponse({
                'status': 'error', 
                'message': 'Error formatting search results',
                'detail': str(format_error)
            }, status=500)
        
    except Exception as e:
        logger.error(f"Error in general message API: {str(e)}")
        return JsonResponse({
            'status': 'error',
            'message': 'Internal server error'
        }, status=500)


@csrf_exempt
@require_http_methods(["GET"])
def get_current_user(request):
    """
    Return information about the current user.
    This helps personalize the chatbot interaction.
    """
    try:
        if request.user.is_authenticated:
            return JsonResponse({
                'is_authenticated': True,
                'name': request.user.first_name or request.user.username,
                'email': request.user.email,
                'session_id': request.session.session_key,
                'sender_id': f"user_{request.user.id}" if request.user.id else str(uuid.uuid4())
            })
        else:
            # For anonymous users, generate a unique session ID
            if not request.session.session_key:
                request.session.save()
                
            return JsonResponse({
                'is_authenticated': False,
                'name': 'Guest',
                'session_id': request.session.session_key,
                'sender_id': f"guest_{request.session.session_key}" if request.session.session_key else str(uuid.uuid4())
            })
    except Exception as e:
        logger.error(f"Error in get_current_user: {str(e)}")
        return JsonResponse({
            'is_authenticated': False,
            'name': 'Guest',
            'sender_id': str(uuid.uuid4()),
            'error': str(e)
        })


def test_tool_view(request):
    """Render the test tool UI for debugging the chatbot API."""
    return render(request, 'chatbot_app/test_tool.html', {
        'page_title': 'Chatbot API Test Tool',
        'api_endpoints': {
            'config': '/api/config/',
            'user': '/get-current-user/',
            'verify': '/api/verify/',
            'message': '/api/message/'
        }
    })
