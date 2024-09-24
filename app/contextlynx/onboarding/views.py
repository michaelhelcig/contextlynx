# onboarding/views.py

from django.shortcuts import render

def onboarding_view(request):
    return render(request, 'onboarding/onboarding.html')