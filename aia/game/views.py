from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.http import Http404
from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings

# @login_required
def index(request):

    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

    template = loader.get_template('game/index.html')
    context = {

    }
    return HttpResponse(template.render( context ,request))
    # return HttpResponse('hello world')

def controll_pannel(request):
    template = loader.get_template('game/controll_pannel.html')
    context = {

    }
    return HttpResponse(template.render( context ,request))
