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
from django.shortcuts import redirect

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
      return redirect('view_cate')
  return render(request,'staff/add_cate.html',{'form':form})

@permission_required('is_staff', login_url="/")
def add_chall(request):
  form = ChallengeForm(request.POST or None)
  if request.method == 'POST':
    if form.is_valid():
      form.save()
      return redirect('view_challs')
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
    return redirect('view_cate')
    
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
    return redirect('view_challs')

@permission_required('is_staff', login_url="/")
def edit_user(request, userID):
  user = None
  try:
    user = User.objects.get(id=userID)
    edit_form = UserEditProfile(request.POST or None, instance=user)
    if request.method == 'POST':
      if edit_form.is_valid():
        edit_form.save()
        return HttpResponseRedirect('/admin/users')
    return render(request,'staff/edit_user.html',{'form':edit_form})
  except User.DoesNotExist:
    print "User "+ userID +" not found"
    return redirect('view_users')

@permission_required('is_staff', login_url="/")
def view_validations(request):
    validations = Validation.objects.all()
    return render(request,'staff/view_validations.html',{'validations':validations})

@permission_required('is_staff', login_url="/")
def delete_validation(request, validationID):
    try:
        Validation.objects.filter(id=validationID).delete()
    except Validation.DoesNotExist:
        return redirect('view_validations')
    return redirect('view_validations')


@permission_required('is_staff', login_url="/")
def delete_chall(request, challID):
    try:
        Challenge.objects.filter(id=challID).delete()
    except Challenge.DoesNotExist:
        return redirect('view_challs')
    return redirect('view_challs')

@permission_required('is_staff', login_url="/")
def delete_cate(request, cateID):
    try:
        Categorie.objects.filter(id=cateID).delete()
    except Categorie.DoesNotExist:
        return redirect('view_cate')
    return redirect('view_cate')
