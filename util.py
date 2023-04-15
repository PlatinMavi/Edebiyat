from django.http import JsonResponse
from http import HTTPStatus
import time


class RestrictedAccess():
	def __init__(self, time : int = 5):
		self.time = time


def restrict_access_support(func):
	def wrapper(*args,**kwargs):
		return_value = func(*args,**args)
		if type(return_value) == RestrictedAccess:
			return error_response("errors.request.restricted",f"Blocked access for {return_value.time} seconds")
	return wrapper


def post_requests_only(func):
	def wrapper(request, *args, **kwargs):
		if request.method.lower() != "post":
			return error_response("errors.request.method_not_allowed",f"{request.method.upper()} requests to this endpoint is not allowed")
		return func(request, *args, **kwargs)
	return wrapper

def get_requests_only(func):
	def wrapper(request, *args, **kwargs):
		if request.method.lower() != "get":
			return error_response("errors.request.method_not_allowed",f"{request.method.upper()} requests to this endpoint is not allowed")
		return func(request, *args, **kwargs)
	return wrapper

def error_response(error_name: str, error_details: str = ""):
	return JsonResponse(
		{"success": False, "error": error_name or "",
		 "error_details": error_details, "time": time.time()},status=HTTPStatus.BAD_REQUEST)
#Cascadia Code