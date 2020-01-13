from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.http import Http404
from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings
from game.models import game_controll, game_detail, game_overview
from django.contrib.auth.models import User
from django.db.models import Max

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

    if not request.user.is_superuser:
        return redirect('/')

    template = loader.get_template('game/controll_pannel.html')
    context = {

    }
    return HttpResponse(template.render( context ,request))


def admin_api_game_over(request):
    if request.user.is_superuser:
        game_controll.objects.filter(game_status = 1).update(game_status = 0)
        game_controll.objects.filter(game_status = 2).update(game_status = 0)

        return HttpResponse('admin_api_game_over')

def admin_api_new_game(request):
    if request.user.is_superuser:
        users = User.objects.all()
        
        game_controll.objects.filter(game_status = 1).update(game_status = 0)
        game_controll.objects.filter(game_status = 2).update(game_status = 0)
        tmp = game_controll.objects.all()
        if ( len(tmp) > 0):
            obj = tmp.aggregate(Max('game_id'))
            new_game_id = obj['game_id__max'] + 1
            new_game = game_controll(game_id = new_game_id, game_round = 0, game_status = 1)
            new_game.save()

            # create users
            game_detail.objects.all().delete()
            for user in users:
                game_detail.objects.create( game_id = new_game_id, game_round = 0, user_id = user, balance=5000, bet_red=0, bet_white=0)

        else:
            game_detail.objects.all().delete()
            game_detail.objects.create( game_id = new_game_id, game_round = 0, user_id = user, balance=5000, bet_red=0, bet_white=0)
            new_game = game_controll(game_id = 0, game_round = 0, game_status = 1)
            new_game.save()

        return HttpResponse('admin_api_new_game')

def admin_api_confirm(request):
    if request.user.is_superuser:
        win = request.GET.get('btn','')
        if (win != None):
            return HttpResponse('admin_api_confirm {}'.format(win))

def admin_api_lock(request):
    if request.user.is_superuser:
        game_controll.objects.filter(game_status = 1).update(game_status = 2)
        return HttpResponse('admin_api_lock')