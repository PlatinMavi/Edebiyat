from django.http import JsonResponse,HttpRequest
from http import HTTPStatus
import time
from index.models import RestrictedAccessModel

class RestrictedAccess:
	def __init__(self,request:HttpRequest, until: int = time.time() + 30, reason: str = "unknown_reason"):
		self.ip = request.META.get("REMOTE_ADDR")
		self.until = until
		self.reason = reason

def restrict_access_support(func):
	def wrapper(*args,**kwargs):
		return_value = func(*args,**args)
		if type(return_value) == RestrictedAccessModel:
			return error_response("errors.request.restricted",f"Blocked access for {return_value.time} seconds")
	return wrapper


def post_requests_only(func):
	def wrapper(request, *args, **kwargs):
		if request.method.lower() != "post":
			return error_response("errors.request.method_not_allowed",f"{request.method.upper()} requests to this endpoint is not allowed")
		return func(request, *args, **kwargs)
	return wrapper

def can_be_restricted(func):
	def wrapper(request, *args, **kwargs):
		if request.method.lower() != "get":
			return error_response("errors.request.method_not_allowed",f"{request.method.upper()} requests to this endpoint is not allowed")
		return func(request, *args, **kwargs)
	return wrapper

def is_request_restricted(request:HttpRequest) -> bool:
	return RestrictedAccessModel.objects.get(ip_adress=request.META.get("REMOTE_ADDR"))

def can_be_restricted(func):
	def wrapper(request,*args, **kwargs):
		model = is_request_restricted(request)
		if model:
			return error_response("errors.request.restricted",f"Blocked access for {time.time()-model.until} seconds for reason {model.reason}")
		return_value = func(request, *args, **kwargs)
		if type(return_value) == RestrictedAccess:
			RestrictedAccessModel(ip_adress = return_value.ip,reason=return_value.reason,until=return_value.until).save()
			return error_response("errors.request.restricted",f"Blocked access for {time.time()-model.until} seconds for reason {model.reason}")



	return wrapper

def error_response(error_name: str, error_details: str = ""):
	return JsonResponse(
		{"success": False, "error": error_name or "",
		 "error_details": error_details, "time": time.time()},status=HTTPStatus.BAD_REQUEST)
#Cascadia Code