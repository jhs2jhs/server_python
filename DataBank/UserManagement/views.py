import DBUtil.sutil as myutil
import re
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.utils.translation import ugettext as _
from django.core.urlresolvers import get_callable
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth import login as auth_login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.sites.models import get_current_site
from django.template import RequestContext
from django.utils.http import urlquote, base36_to_int
from django.contrib.auth import authenticate, login
from django.core.context_processors import csrf

def user_login(request, template_name='registration/login.html', redirect_field_name=REDIRECT_FIELD_NAME):
    """Displays the login form and handles the login action."""
    username = myutil.get_http_param(request, "username")
    password = myutil.get_http_param(request, "password")
    errors = []
    #print "************"
    #print request.method
    if username == "":
        errors.append("username can not be empty")
    if username == None:
        username = ""
    if password == "":
        errors.append("password can not be empty")
    if password == None:
        password = ""
    print username, password, "hello"
    if username != "" and password != "":
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                if not errors:
                    login(request, user)
                    redirect_to = myutil.get_http_param(request, redirect_field_name)
                    if redirect_to == None:
                        redirect_to = '/user/'+str(user.id)
                    # Redirect to a success page.
                    return HttpResponseRedirect(redirect_to)
            else:
                # Return a 'disabled account' error message
                return HttpResponse("Return a 'disabled account' error message")
        else:
            errors.append("this user is not exist")
    context_user = {
        "username":username,
        "password":password,
        "next":myutil.get_http_param(request, redirect_field_name)
        }
    context = {"errors":errors, "login":context_user, "user":myutil.check_user(request)}
    context_instance = RequestContext(request)
    # Return an 'invalid login' error message.
    return render_to_response(template_name, context, context_instance)
    

def user_register(request):
    return HttpResponse("login")

def user_logout(request, next_page=None, template_name='registration/logged_out.html', redirect_field_name=REDIRECT_FIELD_NAME):
    "Logs out the user and displays 'You are logged out' message."
    from django.contrib.auth import logout
    logout(request)
    if next_page is None:
        redirect_to = request.REQUEST.get(redirect_field_name, '')
        if redirect_to:
            return HttpResponseRedirect(redirect_to)
        else:
            current_site = get_current_site(request)
            return render_to_response(template_name, {
                'site': current_site,
                'site_name': current_site.name,
                'title': _('Logged out')
            }, context_instance=RequestContext(request))
    else:
        # Redirect to this page until the session has been cleared.
        return HttpResponseRedirect(next_page or request.path)

def logout_then_login(request, login_url=None):
    "Logs out the user if he is logged in. Then redirects to the log-in page."
    if not login_url:
        login_url = settings.LOGIN_URL
    return user_logout(request, login_url)

def redirect_to_login(next, login_url=None, redirect_field_name=REDIRECT_FIELD_NAME):
    "Redirects the user to the login page, passing the given 'next' page"
    if not login_url:
        login_url = settings.LOGIN_URL
    return HttpResponseRedirect('%s?%s=%s' % (login_url, urlquote(redirect_field_name), urlquote(next)))



def template_test(request):
    print request.session.keys
    print request.session.items()
    context = {
        "user": myutil.check_user(request),
            }
    print myutil.check_user(request)
    return render_to_response("base.html", context)

def user_test(request):
    print "***"
    if request.user.is_authenticated():
        print "authenticated"+str(request.user.id),
    else:
        print "not auth:"+str(request.user.is_active)
    print "*****"
    return HttpResponse("user cool:"+str(request.user))