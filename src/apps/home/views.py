# -*- coding: utf-8 -*-
from django.shortcuts import render, render_to_response, redirect
from forms import LoginForm

def index(request):
    form = LoginForm()
    return render_to_response('home/index.html', {'form': form,})

def login(request):
    #if request.method == 'POST': 
    form = LoginForm(request.POST) 
    if form.is_valid():
        return redirect('/home/')
    else:
        return redirect('/home/')
    #else:
	#form = LoginForm() # An unbound form

    return redirect('/')

def main(request):
    return render_to_response('home/home.html', {})
