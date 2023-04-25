from django.urls import path, include
from django.http import HttpResponse, JsonResponse, HttpRequest
import time
from util import error_response, can_be_restricted
import json
from django.views.decorators.csrf import csrf_exempt

import os


@csrf_exempt
@can_be_restricted
def export(request: HttpRequest, language: str):
    language = language.lower()
    is_valid = language+".json" in os.listdir("index/translations")
    if not is_valid:
        return error_response("errors.translations.get.invalid_language", f"Language {language} is not valid")
    return JsonResponse(
        {"success": True, "data": json.load(open("index/translations/"+language+".json", "r", encoding="utf-8"))}, safe=False)
