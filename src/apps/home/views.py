# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect

def index(request):
    return render(request, "home/index.html", locals())