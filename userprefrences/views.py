from django.shortcuts import render
import os
import json
from django.conf import settings
from .models import *
from django.contrib import messages
# Create your views here.
def prefered(request):
    currency_data =[]
    file_path= os.path.join(settings.BASE_DIR, 'currencies.json')
    
    # python debugger for  testing
    # import pdb
    # pdb.set_trace()

    with open(file_path, 'r') as json_file:
        data = json.load(json_file)

        for k,v in data.items():
            currency_data.append({'name':k, 'value':v})  

    exists = UserPreference.objects.filter(user=request.user).exists()
    user_prefrence = None

    if exists:
        user_prefrence = UserPreference.objects.get(user=request.user)

    if request.method =='GET':

        return render(request, 'preferences/prefered.html', context={'currencies':currency_data, 'user_prefrence':user_prefrence})

    else:
        
        currency = request.POST['currency']

        if exists:
            user_prefrence.currency = currency
            user_prefrence.save()
        else:
            UserPreference.objects.create(user=request.user, currency = currency)
        messages.success(request, 'Changes saved successfully')
        return render(request, 'preferences/prefered.html', context={'currencies':currency_data,'user_prefrence':user_prefrence})
        


