from django.shortcuts import render
from django.contrib.auth import logout
from django.http import HttpResponseRedirect

def logout_view(request):
    logout(request)
    print("aoo")
    return HttpResponseRedirect('/accounts/login/')