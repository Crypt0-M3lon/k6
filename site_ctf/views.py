# Create your views here.
#-*- coding: utf-8 -*-

from django.http import Http404
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import auth
from django.http import HttpResponseRedirect
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.sessions.backends.db import SessionStore
from models import *
from forms import *
from django.template import *
from django.db.models import Sum, Max
from django.views.defaults import page_not_found as default_page_not_found
from django.views.defaults import server_error as default_server_error 
import operator
from django.contrib.auth.decorators import login_required
import calendar
import uuid
from django.shortcuts import redirect
from django.core.mail import send_mail

def accueil(request):
    return render(request, 'accueil.html')

def apropos(request):
    return render(request, 'apropos.html')

def reglement(request):
    return render(request, 'reglement.html')

@login_required
def challs(request):
    challs_dic={}
    challs_validation={}
    categories = Categorie.objects.all()
    form = None

    userPoints = Validation.objects.filter(user=request.user).aggregate(Sum('value'))
    if userPoints['value__sum'] is None:
        userPoints['value__sum']=0
    for categorie in categories:
        challs_dic[categorie]=[]
        challs_validation[categorie]=0
    challs = Challenge.objects.filter(private=False, seuil__lte=userPoints['value__sum'], categorie__isnull=False)
    for chall in challs:
        try:
            validated = Validation.objects.get(chall=chall, user=request.user)
            form = None
        except Validation.DoesNotExist:
            form = ValidationForm(idChall=chall.id)
            challs_validation[chall.categorie]=challs_validation[chall.categorie]+1
        challs_dic[chall.categorie].append((chall, form))


    return render(request, 'challs.html',{'challs_dic':challs_dic,'challs_validation':challs_validation})

@login_required
def view_chall(request, challID):
    chall = None
    validated = None
    form = None
    try:
        chall = Challenge.objects.get(id=challID)
    except Challenge.DoesNotExist:
        raise Http404
    try:
        validated = Validation.objects.get(chall=chall, user=request.user)
    except Validation.DoesNotExist:
        form = ValidationForm(idChall=chall.id)
    return render(request, 'view_chall.html',{'chall':chall,'form':form})

@login_required
def validation(request):
    form = ValidationForm(request.POST or None)
    print form.__dict__
    print request.POST
    if request.method == 'POST':
        if form.is_valid():
            if form.validateFlag():
                chall = Challenge.objects.get(id=form.data['flagID']) 
                valid = Validation()
                valid.user = request.user
                valid.chall = chall
                valid.value = chall.points
                valid.save()
                return render(request,'validation_ok.html')
            else:
                return render(request,'validation_fail.html')
    return render(request, 'post_no_param.html')

def login_user(request):
   if request.user.is_authenticated():
       return render(request, 'accueil.html')
   if request.method == 'POST':
       user = authenticate(username=request.POST['user'], password=request.POST['password'])
       if user is not None:
           if user.is_active:
               login(request, user)
               return render(request, 'accueil.html')
           else:
               return render(request, 'user_not_activated.html')
       else:   
           return render(request, 'login_fail.html')
   else:
       return render(request, 'login.html')


def logout_user(request):
    auth.logout(request)
    return render(request, 'logout.html')

def register(request):
    if not request.user.is_authenticated():
        if request.method == 'POST':
            form = UserCreateForm(request.POST)
            if form.is_valid():
                new_user = form.save()
                new_user.is_active = False
                new_user.save()
                code = uuid.uuid1().hex
                content = """
                Merci de vous être inscrit sur k6 !
                Pour compléter votre inscription et participer au CTF, veuillez cliquer sur le lien ci-dessous :
                http://k6.afteam.fr/activate/"""+code +"""

                Attention, le lien ne sera plus valide sous 48h. Passé ce délai vous devrez refaire une demande d'inscription.

                Pour tout renseignement, envoyez un mail à K6. AFTeam@gmail.com

                L'équipe AFTeam.
                """
                if not send_mail('Activation du compte K6',content,'k6.afteam@gmail.com',[new_user.email]):
                    print error
                    return render(request, "register.html", {'form': form})
                activation = ActivateUser()
                activation.user=new_user
                activation.activationCode=code
                activation.save()
                return render(request, 'mail_sent.html')
        else:
            form = UserCreateForm()
        return render(request, "register.html", {'form': form})
    else:
        return redirect('accueil')


def activate(request, codeID):
    try:
        activation = ActivateUser.objects.get(activationCode=codeID)
        user = activation.user
        user.is_active = True
        user.save()
        activation.delete()
        return render(request, 'activated.html')
    except:
        return redirect('accueil')

def view_user(request, userID):
    ok_graph = True
    user = None
    try:
        u = User.objects.get(id=userID)
        u.validation_set.all()
        vals = u.validation_set.all()
        cats = Categorie.objects.all().values('name')
        dic = {}
        total=0
        pie=[]
        validations_all = {}
        total_points_categorie={}
        #on initialise un dictionnaire avec le total de points par catégorie à 0
        for cat in cats:
            dic[cat['name']]=0
            validations_all[cat['name']]=[]
            total_points_categorie[cat['name']]=0
        #on ajoute pour chaque validation le nombre de points correspondant a la catégorie dans le dictionnaire
        for val in vals:
            c = Challenge.objects.get(id=val.chall_id)
            dic[c.categorie.name] += val.value
            total+=val.value
        # on initialise un tuple(nom catégorie, %) pour le pie graph, si division par 0 on ne le trace pas
        try:
            for key in dic:
                pie.append((key,float(dic[key])/float(total)*100.0))    
        except:
            ok_graph=False

        # on initialise un tuple(timestamp javascript, le nombre de points, le nom du chall + valeur) pour le graph
        total=0
        validations = vals.order_by('timestamp')
        validations_total = []
        for validation in validations:
            total+=validation.value
            #Python time is in milisecond, javasript time in second, so *1000
            chall = Challenge.objects.get(id=validation.chall_id)
            print_chall = chall.name + " - " + str(validation.value) + " points"
            validations_total.append((calendar.timegm(validation.timestamp.utctimetuple())*1000,total,print_chall))
            
            total_points_categorie[chall.categorie.name]+=validation.value
            validations_all[chall.categorie.name].append((calendar.timegm(validation.timestamp.utctimetuple())*1000,total_points_categorie[chall.categorie.name],print_chall))
        return render(request, 'view_user.html',{'user_':u,'vals':dic,'ok_graph':ok_graph,'pie':pie, 'validations':validations_total, 'validations_all':validations_all})
    except User.DoesNotExist:
        return redirect('accueil')

def view_scoreboard(request):
    user_point = []
    validations_graph = {}
    users = User.objects.all()
    for user in users:
        total = 0
        user_validations=[]
        validations = user.validation_set.get_queryset()
        for validation in validations:
            total+=validation.value
            chall = Challenge.objects.get(id=validation.chall_id)
            print_chall = chall.name + " - " + str(validation.value) + " points"
            user_validations.append((calendar.timegm(validation.timestamp.utctimetuple())*1000,total,print_chall))
        if user_validations: 
            validations_graph[user]=user_validations
        value = validations.aggregate(Sum('value'))['value__sum']
        date = validations.aggregate(Max('timestamp'))['timestamp__max']
        if value is None:
            value=0
        user_point.append((user,value, date))
    user_point=sorted(user_point,key=operator.itemgetter(1),reverse=True)
   
    dic={}
    i=1
    for user in user_point:
        dic[i]=user 
        i+=1
    return render(request,'scoreboard.html',{'dic':dic,'validations_graph':validations_graph})

def page_not_found(request):
    return render_to_response('404.html')
