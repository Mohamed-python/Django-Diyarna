from django.http import JsonResponse
from django.shortcuts import render
import json

from django.views.decorators.csrf import csrf_exempt
# Create your views here.
from .bot import get_bot_reply
@csrf_exempt
def chat_api(request):
    if request.method == "POST":
        data = json.loads(request.body)
        user_message = data.get("message", "")
        reply = get_bot_reply(user_message)
        return JsonResponse({"reply": reply})
