import usermanager.util as myutil

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

login_in_path = "/accounts/login/"
def check_user_login(request):
    user = request.user
    print user.is_authenticated()
    if not user.is_authenticated():
        # all need to pass in the redirect
        url = login_in_path+"?"+REDIRECT_FIELD_NAME+"="+request.path+""
        #url = login_in_path
        print url
        return HttpResponseRedirect(url)
        #return HttpResponseRedirect("/accounts/login/")
    else:
        return None
'''
login_check_result = check_user_login(request)
    if (login_check_result != None):
        return login_check_result
'''    


def request_token(request):
    return HttpResponse("hello")
    
def user_authorization(request):
    return HttpResponse("hello")
    
def access_token(request):
    return HttpResponse("hello")
    
def public_info(request):
    return HttpResponse("hello")

# service provider prepares the request_token to consumer
def request_prepare(request):
    return HttpResponse("hello")

def access_prepare(request):
    return HttpResponse("hello")

def resource_get_or_create(resource_name, resource_url, resource_readonly):
    resource = Resource.objects.get_or_create(name=resource_name, url=resource_url, is_readonly=resource_readonly)
    return resource

def resource_add(request):
    print request.POST
    param_resource_name = myutil.get_http_param(request, "resource_name")
    param_resource_url = myutil.get_http_param(request, "resource_url")
    param_resource_readonly = myutil.get_http_param(request, "resource_readonly")
    if (param_resource_name != None and param_resource_url != None and param_resource_readonly != None):
        resource_name = param_resource_name
        resource_url = param_resource_url
        resource_readonly = (param_resource_readonly.strip() == "true")
        resource = resource_get_or_create(resource_name, resource_url, resource_readonly)
        print resource
    print resource_readonly
    return HttpResponseRedirect("/sauth/generate_request_token/")

def consumer_get_or_create(user, consumer_name, consumer_desc, consumer_target):
    key = myutil.new_key()
    secret = myutil.new_secret()
    # need to check and set status 
    consumer = Consumer.objects.get_or_create(
            name=consumer_name, 
            desc=consumer_desc, 
            target=consumer_target,
            key = key,
            secret = secret,
            user = user
            )
    return consumer

def consumer_add(request):
    print request.POST
    login_check_result = check_user_login(request)
    if (login_check_result != None):
        return login_check_result
    param_consumer_name = myutil.get_http_param(request, "consumer_name")
    param_consumer_desc = myutil.get_http_param(request, "consumer_description")
    param_consumer_target = myutil.get_http_param(request, "consumer_request_target")
    if (param_consumer_name != None and param_consumer_desc != None and param_consumer_target != None):
        consumer_name = param_consumer_name
        consumer_desc = param_consumer_desc
        consumer_target = param_consumer_target
        user = request.user
        consumer = consumer_get_or_create(user, consumer_name, consumer_desc, consumer_target)
        print consumer
    return HttpResponseRedirect("/sauth/generate_request_token/")

def get_list_resources():
    resources = Resource.objects.all()
    context_resources = []
    for resource in resources :
        resource_id = resource.id,
        resource_name = resource.name
        resource_url = resource.url
        resource_readonly = resource.is_readonly
        context_resource = {
            "id":resource_id,
            "name":resource_name,
            "url":resource_url,
            "readonly":resource_readonly,
            }
        context_resources.append(context_resource)
    return context_resources

def get_list_consumers():
    consumers = Consumer.objects.all()
    context_consumers = []
    for consumer in consumers :
        consumer_id = consumer.id,
        consumer_name = consumer.name
        consumer_desc = consumer.desc
        consumer_target = consumer.target
        consumer_key = consumer.key
        consumer_secret = consumer.secret
        consumer_status = consumer.status
        consumer_user = consumer.user
        context_consumer = {
            "id":consumer_id,
            "name":consumer_name,
            "desc":consumer_desc,
            "target":consumer_target,
            "key":consumer_key,
            "secret":consumer_secret,
            "consumer_status":consumer_status,
            "consumer_user":consumer_user
            }
        #print context_consumer
        context_consumers.append(context_consumer)
    return context_consumers

def get_token_context(my_token):
    token_context = None
    if (my_token != None):
        token_context = {
            "type":my_token.get_token_type_display,
            "key":my_token.key,
            "time_created":my_token.time_created,
            "time_last":my_token.time_last,
            "time_validate":my_token.time_validate,
            "mini_frequency":my_token.mini_frequency,
            "count_used":my_token.count_used,
            }
    return token_context
        

def get_list_tokenManagers():
    tokenmanagers = TokenManager.objects.all()
    context_tokenmanagers = []
    for tokenmanager in tokenmanagers:
        tokenmanager_id = tokenmanager.id
        tokenmanager_resource = tokenmanager.resource
        tokenmanager_consumer = tokenmanager.consumer
        tokenmanager_request = get_token_context(tokenmanager.token_request)
        tokenmanager_private = get_token_context(tokenmanager.token_private)
        tokenmanager_public = get_token_context(tokenmanager.token_public)
        context_tokenmanager = {
            "id": tokenmanager_id,
            "resource": tokenmanager_resource.name,
            "consumer": tokenmanager_consumer.name,
            "request": tokenmanager_request,
            "private": tokenmanager_private,
            "public": tokenmanager_public
            }
        #print context_tokenmanager
        context_tokenmanagers.append(context_tokenmanager)
    return context_tokenmanagers


def tokenmanager_get_or_create(user, resource, consumer):
    isone = TokenManager.objects.filter(user=user, resource=resource, consumer=consumer).count()
    print "**isone:"+str(isone)
    if isone == 0:
        token_key = myutil.new_token()
        token_type = Token.REQUEST
        time_validate = 1000
        mini_frequency = 0
        token = Token.objects.create(key=token_key, token_type=token_type, time_validate=time_validate, mini_frequency=mini_frequency)
        tokenmanager = TokenManager.objects.get_or_create(
            user=user, resource=resource, consumer=consumer,
            token_request=token, key=myutil.new_key(), secret=myutil.new_secret()
            )
        print tokenmanager
    return isone
        
    

def generate_request_token(request):
    #print request.path
    login_check_result = check_user_login(request)
    if (login_check_result != None):
        return login_check_result
    resource_id = myutil.get_http_param(request, "resource_id")
    consumer_id = myutil.get_http_param(request, "consumer_id")
    if (resource_id == None or consumer_id == None):
        context_tokenmanagers = get_list_tokenManagers()
        context_resources = get_list_resources()
        context_consumers = get_list_consumers()
        context = {
            "tokenmanagers": context_tokenmanagers,
            "resources":context_resources, 
            "consumers":context_consumers, 
            "user":myutil.check_user(request)}
        context_instance = RequestContext(request)
        template_name = "generate_request_token.html"
        return render_to_response(template_name, context, context_instance)
    else:
        print "ff"
        resource_id = eval(resource_id)[0]
        consumer_id = eval(consumer_id)[0]
        user = request.user
        resource = Resource.objects.get(id=resource_id)
        consumer = Consumer.objects.get(id=consumer_id)
        print user
        print resource
        print consumer
        token = tokenmanager_get_or_create(user, resource, consumer)
        return HttpResponseRedirect("/sauth/generate_request_token/")
        
    
