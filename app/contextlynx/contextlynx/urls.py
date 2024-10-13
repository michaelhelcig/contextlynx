from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

def home_redirect(request):
    if request.user.is_authenticated:
        return redirect('create_note')
    else:
        return redirect('onboarding')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_redirect, name='home'),
    path('', include('core.urls')),
    path('', include('accounts.urls')),
    path('get-started/', include('onboarding.urls')),
    path('create/', login_required(lambda request: redirect('create_note')), name='create_redirect'),
]