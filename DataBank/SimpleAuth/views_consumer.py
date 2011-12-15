import DBUtil.sutil as myutil

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.utils.translation import ugettext as _
from django.core.urlresolvers import get_callable
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from models import *
  


def consumer_request(request):
    print request.POST
    login_check_result = myutil.check_user_login(request)
    if (login_check_result != None):
        return login_check_result
    request_action = myutil.get_http_param(request, "action")
    request_url = myutil.get_http_param(request, "url")
    request_callback = myutil.get_http_param(request, "callback")
    request_token = myutil.get_http_param(request, "token")
    #if (request_action == None):
    #    return HttpResponse("invalidate argument")
    if (request_action == "Detail"):
        params = urllib.urlencode({
            "action":"detail",
            "token_key":request_token,
            "callback":request_callback,
            })
        url = request_url+"?"+params
        return HttpResponseRedirect(url)
    if (request_action == "Request"):
        # request
        params = urllib.urlencode({
            "action":"request",
            "token_key":request_token,
            "callback":request_callback,
            })
        print params
        url = request_url+"?"+params
        return HttpResponseRedirect(url)
    context_request_pairs = []
    if (request_action == "display_request"):
        request_detail = myutil.get_http_param(request, "request_detail")
        request_details = eval(request_detail)
        for key in request_details.keys():
            value = request_details[key]
            context_pair = {"key":key, "value":value}
            context_request_pairs.append(context_pair)
    context_tokenmanager_pairs = []
    if (request_action == "display_tokenmanager"):
        request_detail = myutil.get_http_param(request, "tokenmanager_detail")
        request_details = eval(request_detail)
        print request_details
        '''for key in request_details.keys():
            value = request_details[key]
            context_pair = {"key":key, "value":value}
            context_tokenmanager_pairs.append(context_pair)
        print context_tokenmanager_pairs'''
        context_tokenmanager_pairs = request_details
    context_Request = {
        "url":"http://localhost:8000/sauth/service_request/",
        "token":"8b6b0bae59a44d4286287460c51028f6",
        "callback":"http://localhost:8001/sauth/consumer_request/",
        }
    context = {
        "request_pairs": context_request_pairs,
        "tokenmanager_pairs": context_tokenmanager_pairs,
        "request": context_Request,
        "user": myutil.check_user(request)
        }
    context_instance = RequestContext(request)
    template_name = "consumer_request.html"
    return render_to_response(template_name, context, context_instance)
    
