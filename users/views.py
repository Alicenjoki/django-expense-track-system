from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.models import User
import json
from django.views.generic import View
from validate_email import validate_email
from django.contrib import messages
from django.core.mail import EmailMessage, send_mail
from django.conf import settings
from django.urls import reverse

# for email activation
import django
from django.utils.encoding import force_bytes,force_str, DjangoUnicodeDecodeError
django.utils.encoding.force_text = force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from .utils import token_generator
from django.contrib import auth

# Create your views here.

class LoginView(View):
    def get(self, request):
        return render(request, 'registration/login.html')
    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']

        if username and password:
            user = auth.authenticate(username=username, password=password)

            if user:
                if user.is_active:
                    auth.login(request, user)
                    messages.success(request, f"welcome {username}, you are logged in")
                    return redirect('expenses')
                messages.error(request, 'account is not active please check your email')
            messages.error(request, 'Invalid credentials, try again')
        messages.error(request, 'Please fill all fields')
        return render(request, 'registration/login.html')

class UsernameValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        username = data['username']

        if not str(username).isalnum():
            return JsonResponse({'username_error': 'username should only contain alpha numeric characters'}, status=400)
    
        if User.objects.filter(username=username).exists():
            return JsonResponse({'username_error': 'Sorry, the username already exists please select another username'}, status=409)
        return JsonResponse({'username_valid': True})
    

class EmailValidationView(View):
    def post(self, request):
        data =json.loads(request.body)
        email = data['email']
        if not validate_email(email):
            return JsonResponse({'email_error': "Invalid email format"}, status=400)
        if User.objects.filter(email=email).exists():
            return JsonResponse({'email_error' : 'Sorry, the email ha already been taken, please choose another email'}, status=400)
        return JsonResponse({'email_valid':True})


class Register(View):
    def get(self, request):
        return render(request, 'registration/register.html')
    
    def post(self, request):
        # Get user data

        # Validate the data

        # Create account
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        context ={
            'fieldValues':request.POST
        }

        if not User.objects.filter(username=username).exists():
            if not User.objects.filter(email=email).exists():
                if len(password) <6:
                    messages.error(request, 'Password is too short')
                    if not str(password).isalnum():
                        messages.error(request, 'Password should include both alpha numeric and special character such as #,_ only')
                    return render(request, 'registration/register.html', context )
                
                user = User.objects.create_user(username=username, email=email)
                user.set_password(password)
                user.is_active=False
                user.save()
                email_subject = 'Activate your account'
                # path_to_view
                    # getting domain we are on
                domain = get_current_site(request).domain
                    # encode the uid
                uidb64 = urlsafe_base64_encode(force_bytes(user.pk))

                    #relative url to verify
                link = reverse('activate', kwargs={'uidb64':uidb64, 'token':token_generator.make_token(user)})

                activate_url = 'http://' + domain + link

                email_body = 'Hi ' + user.username + 'Please verify your email using the link below \n' + activate_url

                email = EmailMessage(
                    email_subject,
                    email_body,
                    'noreply@semycolon.com',
                    [email],
                )
                
                email.send(fail_silently=False)
                # if request.method =='POST':
                #     message = 'Hello'
                #     email = request.POST['email']
                #     name = request.POST['name']
                #     send_mail(
                #         'contact Form', #title
                #         message,
                #         'settings.EMAIL_HOST_USER',
                #         [email],
                #         fail_silently=False
                #     )
                messages.success(request, f'Hello {username}, your account has successfully been created. Please check your email to activate your account')
                return render(request, 'registration/register.html', context )
        
        return render(request, 'registration/register.html', context )

class Verification(View):
        #uidb64 is encoded uid 
        # #token verify user to not use the link twice
    def get(self, request, uidb64, token):  
        try:
            id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=id) #checking the link is only used once

            if not token_generator.check_token(user,token):
                return redirect('login' +'?message='+'User already active' ) #the ?message= statements is message becauser

            if user.is_active:
                return redirect('login')
            user.is_active = True
            user.save()

            messages.success(request, 'Account activated successfully')
            return redirect('login')
        except Exception as ex:
            pass
            
        return redirect ('login')

# other option for email activation

# class VerificationView(View):
#   def get(self, request, uidb64, token):
#     try:
#       id = force_str(urlsafe_base64_decode(uidb64))
#       user = User.objects.get(pk=id)
      
#     except(TypeError, ValueError, OverflowError, User.DoesNotExist):
#         user = None
   
#     if user is not None and token_generator.check_token(user, token):
#         user.is_active = True
#         user.save()

#         messages.success(request, 'Account activated successfully')
#         return redirect('login')
     
#     elif not token_generator.check_token(user, token):
#         messages.warning(request,'User already activated')
#         return redirect('login')
     
#     elif user.is_active:
#         return redirect('login')

#     else:
#         messages.error(request, 'Activation link is invalid!')
#         return redirect('login')


    
#     return redirect('login')


class LogoutView(View):
    def post(self, request):
        auth.logout(request)
        messages.success(request, 'You have successfully logged out')
        return redirect('login')
