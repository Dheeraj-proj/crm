from django.shortcuts import render, redirect
from django.forms import inlineformset_factory
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group
from django.contrib import messages
# Create your views here.
from .models import *
from .forms import OrderForm, CreateUserForm, CustomerForm
from .filters import OrderFilter
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .decoraters import *

@unauthenticated_user
def registerPage(request):
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                user = form.save()
                username = form.cleaned_data.get('username')





                messages.success(request, 'Account Registered:' + username)
                return redirect('login')


        context = {'form': form}
        return render(request, 'account/register.html', context)

@unauthenticated_user
def loginPage(request):

        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('home')

            else:
                messages.info(request, 'Username/Password incorrect')

        context = {}
        return render(request, 'account/login.html', context)

def logoutUser(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def userPage(request):
    orders = request.user.customer.order_set.all()
    total_orders = orders.count()
    delivered = orders.filter(status='DELIVERED').count()
    pending = orders.filter(status='PENDING').count()
    print('orders:', orders)

    context = {'orders': orders, 'total_orders': total_orders, 'delivered': delivered,
               'pending': pending}
    return render(request, 'account/user.html', context)


@login_required(login_url='login')
@admin_only
def home(request):

    customers = Customer.objects.all()
    orders = Order.objects.all()
    total_orders = orders.count()
    delivered = orders.filter(status='DELIVERED').count()
    pending = orders.filter(status='PENDING').count()

    context = {'customers': customers, 'orders': orders,
               'total_orders': total_orders, 'delivered': delivered,
               'pending': pending}

    return render(request, 'account/dashboard.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def accountSettings(request):

    customer = request.user.customer
    form = CustomerForm(instance=customer)

    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()

    context = {'form': form}
    return render(request, 'account/account_settings.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def products(request):
    products = Product.objects.all()
    return render(request, 'account/products.html', {'products': products})

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def customer(request, numb):

    customer = Customer.objects.get(id=numb)
    orders = customer.order_set.all()
    TO = orders.count()

    myFilter = OrderFilter(request.GET, queryset=orders)
    orders = myFilter.qs

    context = {'customer': customer, 'orders': orders, 'TO': TO, 'myFilter': myFilter}

    return render(request, 'account/customer.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def createorder(request, yo):

    OrderFormSet = inlineformset_factory(Customer, Order, fields=('product', 'status') )
    customer = Customer.objects.get(id=yo)
    formset = OrderFormSet(queryset= Order.objects.none(), instance=customer)
    if request.method == 'POST':

        formset = OrderFormSet(request.POST, instance=customer)

        if formset.is_valid():

            formset.save()
            return redirect('/')

    context = {'formset': formset}

    return render(request, 'account/order_form.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def updateorder(request, yo):

    order = Order.objects.get(id=yo)
    parentName = order.customer.name
    form = OrderForm(instance=order)

    if request.method == 'POST':

        form = OrderForm(request.POST, instance=order)
        if form.is_valid():

            form.save()
            return redirect('/')

    context = {'form': form}

    return render(request, 'account/update_order_form.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def deleteorder(request, yo):


    order = Order.objects.get(id=yo)
    name = order.customer.name

    if request.method == 'POST':
        order.delete()
        return redirect('/')
    context = {'item': order , 'ot': name}
    return render(request, 'account/delete.html' , context)