from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.http import Http404
from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings
from game.models import game_controll, game_detail, game_overview
from django.contrib.auth.models import User
from django.db.models import Max, F
from django.views.decorators.csrf import csrf_exempt
import json

# @login_required
def index(request):

    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    user = request.user
    obj_game_controll = game_controll.objects.filter(game_status = 1)
    if len(obj_game_controll) > 0:
        user_detail = game_detail.objects.filter(game_id = obj_game_controll[0].game_id,
                                                game_round=obj_game_controll[0].game_round,
                                                user_id=user
                                                )[0]

        odds = game_overview.objects.filter(game_id = obj_game_controll[0].game_id,
                                            game_round=obj_game_controll[0].game_round,
                                            )[0]

    template = loader.get_template('game/index.html')

    context = {
        "user_balance" : user_detail.balance,
        "user_bet_red" : user_detail.bet_red,
        "user_bet_white" : user_detail.bet_white,
        "odds_red" : odds.total_red,
        "odds_white" : odds.total_white,
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


# api palyer
@login_required
def player_api_betting_red(request):
    user = request.user
    now_bet_amount = request.GET.get('now_bet_amount','')
    user_balance = game_detail.objects.filter(user_id = user)[0].balance

    if int(now_bet_amount) > int(user_balance) :
        return HttpResponse('player_api_betting_red WARRING! BALANCE NOT ENOUGH')
    else:
        obj_status = game_controll.objects.filter(game_status = 1)
        if len(obj_status) > 0:
            game_detail.objects.filter(game_id=obj_status[0].game_id,
                                        game_round=obj_status[0].game_round,
                                        user_id=user).update(
                                            balance = F('balance') - int(now_bet_amount),
                                            bet_red = F('bet_red') + int(now_bet_amount)
                                            )
            game_overview.objects.filter(game_id=obj_status[0].game_id,
                                        game_round=obj_status[0].game_round,
                                        ).update(
                                            total_red = F('total_red') + int(now_bet_amount),
                                        )
        return HttpResponse('player_api_betting_red updated')

@login_required
def player_api_betting_white(request):
    user = request.user
    now_bet_amount = request.GET.get('now_bet_amount','')
    user_balance = game_detail.objects.filter(user_id = user)[0].balance

    if int(now_bet_amount) > int(user_balance) :
        return HttpResponse('player_api_betting_white WARRING! BALANCE NOT ENOUGH')
    else:
        obj_status = game_controll.objects.filter(game_status = 1)
        if len(obj_status) > 0:
            game_detail.objects.filter(game_id=obj_status[0].game_id,
                                        game_round=obj_status[0].game_round,
                                        user_id=user).update(
                                            balance = F('balance') - int(now_bet_amount),
                                            bet_white = F('bet_white') + int(now_bet_amount)
                                            )
            game_overview.objects.filter(game_id=obj_status[0].game_id,
                                        game_round=obj_status[0].game_round,
                                        ).update(
                                            total_white = F('total_white') + int(now_bet_amount),
                                        )

        return HttpResponse('player_api_betting_white updated')

@login_required
def player_api_update_odds(request):
        return HttpResponse('player_api_update_odds')

# polling api
@login_required
@csrf_exempt
def polling_apis(request):
    user = request.user
    obj_game_controll = game_controll.objects.filter(game_status = 1)
    if len(obj_game_controll) > 0:
        user_detail = game_detail.objects.filter(game_id = obj_game_controll[0].game_id,
                                                game_round=obj_game_controll[0].game_round,
                                                user_id=user
                                                )[0]

        odds = game_overview.objects.filter(game_id = obj_game_controll[0].game_id,
                                            game_round=obj_game_controll[0].game_round,
                                            )[0]
    ret_dict ={
        "user_balance" : user_detail.balance,
        "user_bet_red" : user_detail.bet_red,
        "user_bet_white" : user_detail.bet_white,
        "odds_red" : odds.total_red,
        "odds_white" : odds.total_white,
    }
    ret_json = json.dumps(ret_dict)
    return HttpResponse(ret_json)



# api admin
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
            game_controll.objects.create(game_id = new_game_id, game_round = 0, game_status = 1)
            game_overview.objects.create(game_id = new_game_id, game_round = 0, total_red=0, total_white=0)

            # create users
            game_detail.objects.all().delete()
            for user in users:
                game_detail.objects.create( game_id = new_game_id, game_round = 0, user_id = user, balance=5000, bet_red=0, bet_white=0)

        else:
            game_detail.objects.all().delete()
            for user in users:
                game_detail.objects.create( game_id = new_game_id, game_round = 0, user_id = user, balance=5000, bet_red=0, bet_white=0)
            game_controll.objects.create(game_id = 0, game_round = 0, game_status = 1)
            game_overview.objects.create(game_id = new_game_id, game_round = 0, total_red=0, total_white=0)

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
