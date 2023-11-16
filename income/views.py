from django.shortcuts import render,redirect
from .models import *
from .forms import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from userprefrences.models import UserPreference
# Create your views here.
@login_required
def income(request):
    income = Income.objects.filter(user=request.user)
    paginator = Paginator(income, 2)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator,page_number)
    currency = UserPreference.objects.get(user=request.user).currency
    context={
        'income':income,
        'page_obj':page_obj,
        'currency': currency,
    }
    return render(request, 'income/income.html', context)

@login_required
def add_income(request):
    if request.method == 'POST':
        form = IncomeForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data.get('amount')
            source = form.cleaned_data.get('source')
            description = form.cleaned_data.get('description')
            created = form.cleaned_data.get('created')

            # validate user input
            if not amount:
                form = IncomeForm(request.POST)
                messages.error(request, 'Please Enter an amount')
                return redirect('income')
            if not source:
                form = IncomeForm(request.POST)
                messages.error(request, 'Please Enter an amount')
                return redirect('income')
            if not description:
                form = IncomeForm(request.POST)
                messages.error(request, 'Please Enter an amount')
                return redirect('income')

            Income.objects.create(user=request.user, amount=amount, source=source, description=description, created=created)
            messages.success(request, 'You have successfully added an income')
            return redirect('income')
        else:
            messages.error(request, 'Unable to add your income, please try again')
    else:
        form = IncomeForm()
    context={
        'form':form,
    }
    return render(request, 'income/add_income.html', context)

@login_required
def edit_income(request, uuid):
    income = Income.objects.get(id=uuid)

    if request.method == 'POST':
        form= IncomeForm(request.POST, instance=income)
        if form.is_valid():
            form.save()
            # or you can use
            # income.user=request.user
            # income.amount = amount
            # income.source = source
            # income.description = description
            # income.date = date
            # expense.save()
            source = form.cleaned_data.get('source')
            messages.success(request, f'You have successfully updated {source} income')
            return redirect('income')
        else:
            messages.error(request, f'Unable to Edit {source} income, please try again')
    else:
        form = IncomeForm(instance=income)
    context={
        'form':form,
        'income':income,
    }
    return render(request, 'income/edit_income.html', context)

@login_required
def delete_income(request,uuid):
    income = Income.objects.get(id=uuid)
    if request.method == 'POST':
        income.delete()
        messages.success(request, f'you have successfully deleted an income')
        return redirect('income')
    
    context={
        'income':income,
    }

    
    return render(request, 'income/delete_income.html', context)


