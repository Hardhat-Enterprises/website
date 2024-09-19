from django.shortcuts import render

# Create your views here.


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import UserClickEvent
from django.contrib.auth import get_user_model
import json

User = get_user_model()

@csrf_exempt
def user_click_event(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            page_url = data.get('page_url')
            clicked_element = data.get('clicked_element')

            if not page_url or not clicked_element:
                return JsonResponse({'error': 'Page URL and clicked element are required.'}, status=400)
            user = request.user if request.user.is_authenticated else None
            UserClickEvent.objects.create(
                user=user,
                page_url=page_url,
                clicked_element=clicked_element
            )

            return JsonResponse({'message': 'Click event saved successfully.'}, status=201)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data.'}, status=400)

    return JsonResponse({'error': 'Invalid HTTP method. Only POST is allowed.'}, status=405)
