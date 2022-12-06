from django.shortcuts import render
from user.views import *
from booking.views import *
from .models import *
from django.core.mail import EmailMessage, send_mail
from pushpakcarrental import settings
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
import datetime
import math
from django.conf import settings
from django.http.response import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import TemplateView
from user import tokens
from user.tokens import generate_token
import secrets
import string
from django.contrib.auth.base_user import BaseUserManager
# Create your views here.
def digitalCheckin(request):
    if request.method == 'POST':
        check_in_date = datetime.datetime.strptime(request.POST['check_in_date']+ ' ' + request.POST['check_in_time'], '%Y-%m-%d %H:%M')
        checkin = Digital_Check_In()
        checkin.user = request.user
        checkin.check_in_date = check_in_date
        checkin.save()
        messages.success(request, 'Digital checkin done successfully')
        return render(request, 'digitalcheckin.html')
    else:
        return render(request, 'digitalcheckin.html')



@login_required
def referFriend(request):
    if request.method == 'POST':
        refer_friend = Refer_Friend(
            refer_friend = request.POST['refer_friend'],
            user = request.user
        )
        refer_friend.save()
        # start email template
        subject = "Welcome to Pushpak Cars!!"
        message = "Hello Welcome to Pushpak Cars!!\n"        
        from_email = settings.EMAIL_HOST_USER
        to_list = [request.POST['refer_friend']]
        send_mail(subject, message, from_email, to_list, fail_silently=True)

        success = 'success'
        return render(request, 'refer_friend.html', {'success':success})
    else:
        return render(request, 'refer_friend.html')

def myWallet(request):
    pass