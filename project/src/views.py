from django.shortcuts import render
from django.contrib.auth.models import User

def home_page(request):
    users = User.objects.all().order_by('-date_joined')
    context = {
        'users': users
    }
    return render(request, 'index.html', context)