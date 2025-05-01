from django.shortcuts import render, redirect
from .models import Expense, Income
from .forms import ExpenseForm, IncomeForm
from django.db.models import Sum
from datetime import datetime
from django.db.models.functions import ExtractMonth
import calendar
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required


@login_required(login_url='login')
def dashboard(request):

    month = request.GET.get('month')
    category = request.GET.get('category') 

    expenses_qs = Expense.objects.filter(user=request.user).order_by('-date')
    incomes_qs = Income.objects.filter(user=request.user).order_by('-date')

    if month:
        expenses_qs = expenses_qs.filter(date__month=month)
        incomes_qs = incomes_qs.filter(date__month=month)

    if category:
        expenses_qs = expenses_qs.filter(category__iexact=category)

    expenses_by_months = Expense.objects.filter(user=request.user)\
        .annotate(month=ExtractMonth('date'))\
        .values('month')\
        .annotate(total=Sum('amount'))\
        .order_by('month')

    incomes_by_months = Income.objects.filter(user=request.user)\
        .annotate(month=ExtractMonth('date'))\
        .values('month')\
        .annotate(total=Sum('amount'))\
        .order_by('month')
    
    expense_by_category = Expense.objects.filter(user=request.user)\
        .values('category')\
        .annotate(total=Sum('amount'))\
        
    category_labels = []
    category_totals = []

    for item in expense_by_category:
        category_labels.append(item['category'])
        category_totals.append(float(item['total']))


    months = [calendar.month_name[i] for i in range(1, 13)]
    expense_data = [0] * 12
    income_data = [0] * 12

    for e in expenses_by_months:
        expense_data[e['month'] - 1] = float(e['total'])

    for i in incomes_by_months:
        income_data[i['month'] - 1] = float(i['total'])

    total_expense = expenses_qs.aggregate(total=Sum('amount'))['total'] or 0
    total_income = incomes_qs.aggregate(total=Sum('amount'))['total'] or 0
    balance = total_income - total_expense

    month_choices = [
    ('1', 'January'), ('2', 'February'), ('3', 'March'),
    ('4', 'April'), ('5', 'May'), ('6', 'June'),
    ('7', 'July'), ('8', 'August'), ('9', 'September'),
    ('10', 'October'), ('11', 'November'), ('12', 'December'),
    ]

    context = {
        'expenses': expenses_qs.order_by('-date'),
        'incomes': incomes_qs.order_by('-date'),
        'total_expense': total_expense,
        'total_income': total_income,
        'balance': balance,
        'selected_month': month,
        'selected_category': category,
        'month_choices': month_choices,
        'months': months,
        'expense_data': expense_data,
        'income_data': income_data,
        'category_labels': category_labels,
        'category_totals':category_totals
    }
    return render(request, 'finance/dashboard.html', context)

    
def add_expense(request):
    if request.method =='POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user
            expense.save()
            return redirect('dashboard')  
    else:
        form = ExpenseForm()
    return render(request,  'finance/add_expense.html', {'form': form})
        

def add_income(request):
    if request.method == 'POST':
        form = IncomeForm(request.POST)
        if form.is_valid():
            income = form.save(commit=False)
            income.user = request.user
            income.save()
            return redirect('dashboard')
    else:
        form = IncomeForm()
    return render(request, 'finance/add_income.html', {'form': form})

def edit_expense(request, pk):
    expense = Expense.objects.get(pk=pk , user=request.user)

    if request.method == 'POST':
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = ExpenseForm(instance=expense)

    return render(request, 'finance/edit_expense.html', {'form': form})

def delete_expense(request, pk):
    expense = Expense.objects.get(pk=pk, user = request.user)

    if request.method == 'POST':
        expense.delete()
        return redirect('dashboard')
    
    return render(request, 'finance/delete_expense.html', {'expense': expense})

def edit_income(request, pk):
    income = Income.objects.get(pk=pk, user = request.user)

    if request.method == 'POST':
        form = IncomeForm(request.POST, instance=income)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = IncomeForm(instance=income)
    
    return render(request, 'finance/edit_income.html', {'form' : form})

def delete_income(request, pk):
    income = Income.objects.get(pk=pk, user = request.user)
    if request.method == 'POST':
        income.delete()
        return redirect('dashboard')
    
    return render(request, 'finance/delete_income.html', {'income' : income})


def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserCreationForm()  

    return render(request, 'finance/register.html', {'form': form})


    



    

