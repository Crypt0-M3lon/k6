# Create your views here.
#-*- coding: utf-8 -*-

from models import *
from forms import *
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.contrib import auth
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.decorators import permission_required

@permission_required('is_staff', login_url="/")
def accueil(request):
  return render(request,'staff/admin.html')

@permission_required('is_staff', login_url="/")
def view_users(request):
  user = User.objects.all()
  return render(request,'staff/view_users.html',{'users':user})

@permission_required('is_staff', login_url="/")
def view_cate(request):
  cate = Categorie.objects.all()
  return render(request,'staff/view_cate.html',{'categories':cate})

@permission_required('is_staff', login_url="/")
def view_challs(request):
  order=''
  if (order == 'normal'):
    order = 'normal'
    challs = Challenge.objects.all().order_by('categorie')
  else:
    order ='reverse'
    challs = Challenge.objects.all().order_by('-categorie')
  return render(request,'staff/view_challs.html',{'challs':challs,'order':order})

@permission_required('is_staff', login_url="/")
def add_cate(request):
  form = CategorieForm(request.POST or None)
  if request.method == 'POST':
    if form.is_valid():
      form.save()
      return HttpResponseRedirect("/admin")
  return render(request,'staff/add_cate.html',{'form':form})

@permission_required('is_staff', login_url="/")
def add_chall(request):
  form = ChallengeForm(request.POST or None)
  if request.method == 'POST':
    if form.is_valid():
      form.save()
      return HttpResponseRedirect("/challs")
  return render(request,'staff/add_chall.html',{'form':form})
    
@permission_required('is_staff', login_url="/")
def edit_cate(request, cateID):
  categorie = None
  try:
    categorie = Categorie.objects.get(id=cateID)
    edit_form = CategorieForm(request.POST or None, instance=categorie)
    if request.method == 'POST':
      if edit_form.is_valid():
        edit_form.save()
        return HttpResponseRedirect('/admin/cate')
    return render(request,'staff/edit_cate.html',{'form':edit_form})
  except Categorie.DoesNotExist:
    return HttpResponseRedirect('/admin/cate')

@permission_required('is_staff', login_url="/")
def edit_chall(request, challID):
  challenge = None
  try:
    challenge = Challenge.objects.get(id=challID)
    edit_form = ChallengeForm(request.POST or None, instance=challenge)
    if request.method == 'POST':
      if edit_form.is_valid():
        edit_form.save()
        return HttpResponseRedirect('/admin/challs')
    return render(request,'staff/edit_chall.html',{'form':edit_form})
  except Challenge.DoesNotExist:
    return HttpResponseRedirect('/admin/challs')

@permission_required('is_staff', login_url="/")
def edit_user(request, userID):
  user = None
  try:
    user = User.objects.get(id=userID)
    edit_form = UserChangeForm(request.POST or None, instance=user)
    if request.method == 'POST':
      if edit_form.is_valid():
        edit_form.save()
        return HttpResponseRedirect('/admin/users')
    return render(request,'staff/edit_user.html',{'form':edit_form})
  except Challenge.DoesNotExist:
    print "User "+ userID +" not found"
    return HttpResponseRedirect('/admin/users')
