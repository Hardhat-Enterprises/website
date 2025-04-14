from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def chat_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            message = data.get('message', '')
            
            # For now, just return the predefined response
            return JsonResponse({
                'response': 'Hi! I am currently being developed and cannot answer your queries. Come back soon!'
            })
        except json.JSONDecodeError:
            return JsonResponse({
                'error': 'Invalid JSON data'
            }, status=400)
    
    # For GET requests, render the chat interface with initial message
    return render(request, 'chatbot_app/chat.html', {
        'initial_message': 'Hello! Welcome to Hardhat Enterprises. How can I assist you today?'
    }) 