from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *
from django.contrib import messages
from django.core.paginator import Paginator
import json
from django.http import JsonResponse
from userprefrences.models import UserPreference


# Create your views here.
# @login_required(login_url='/registration/login')
def search_expenses(request):
    if request.method == 'POST':
        # form = AddExpenseForm(request.POST)
        # category = form.cleaned_data.get('category')
        # amount = form.cleaned_data.get('amount')
        # description = form.cleaned_data.get('description')
        # date = form.cleaned_data.get('date')
        search_str = json.loads(request.body).get('searchText')

        expenses = Expense.objects.filter(
            amount__istarts_with=search_str, owner=request.user) | Expense.objects.filter(
            date__istarts_with=search_str, owner=request.user) | Expense.objects.filter(
            description__icontains=search_str, owner=request.user) | Expense.objects.filter(
            category__icontains=search_str, owner=request.user)

        data = expenses.values()

        return JsonResponse(list(data), safe=False)



@login_required(login_url='/registration/login')
def home(request):
    return render(request, 'expenses/home.html')

@login_required(login_url='/registration/login')
def expenses(request):
    categories = Category.objects.all()
    expenses = Expense.objects.filter(owner=request.user)
    paginator = Paginator(expenses, 2)
    page_number = request.GET.get('page')
    page_obj =Paginator.get_page(paginator,page_number)
    currency = UserPreference.objects.get(user=request.user).currency
    context={
        'categories':categories,
        'expenses':expenses,
        'page_obj':page_obj,
        'currency':currency,
    }
    return render(request, 'expenses/expenses.html',context)

@login_required(login_url='/registration/login')
def add_expense(request):
    expense = Expense.objects.all()
    categories = Category.objects.all()

    if request.method == 'POST':
        form = AddExpenseForm(request.POST)
        if form.is_valid():
            # form.save()
            category = form.cleaned_data.get('category')
            amount = form.cleaned_data.get('amount')
            description = form.cleaned_data.get('description')
            date = form.cleaned_data.get('date')
            if not amount:
                messages.error(request, f'Please enter an amount')
                return redirect('add_expense')
            elif not category:
                messages.error(request, f'Please enter a category')
                return redirect('add_expense')
            elif not description:
                messages.error(request, f'Please enter a description')
                return redirect('add_expense')
            else:
                Expense.objects.create(owner= request.user, amount=amount, category=category, description=description, date= date)
                messages.success(request, f'Successfully added {category} expense')
                return redirect('expenses')
            
        else:
            messages.error(request, 'Unable to add an expense')
    else:
        form = AddExpenseForm()

    context={
        'form':form,
        'expense': expense,
        'values' : request.POST,
    }    
    return render(request, 'expenses/add_expense.html', context)

@login_required(login_url='/registration/login')
def edit_expense(request, uuid):
    expenses = Expense.objects.get(id=uuid)

    if request.method == 'POST':
        form = AddExpenseForm(request.POST, instance=expenses)
        if form.is_valid():
            form.save()
            category = form.cleaned_data.get('category')
            messages.success(request, f'You have successfully edited {category} expense')
            return redirect('expenses')
        else:
            messages.error(request, f'Unable to edit {category} expense')
    else:
        form= AddExpenseForm(instance=expenses)

    context={
        'expenses':expenses,
        'form':form,
    }

    return render(request, 'expenses/edit_expense.html', context)
