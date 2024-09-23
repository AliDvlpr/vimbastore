from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.views.decorators.csrf import csrf_protect
from django.core.paginator import Paginator
from jalali_date import datetime2jalali
from core.models import User
from store.models import *
from core.utils import generate_otp
from .forms import *
import logging
from django.utils import timezone

logger = logging.getLogger(__name__)

def home(request):
    return render(request, 'front/home.html')

@login_required(login_url='/login/')
def profile(request):
    user = request.user
    customer = Customer.objects.get(user=user)
    wallet = Wallet.objects.get(customer=customer)
    user_form = UserProfileForm(instance=user)
    context = {
        'user': user,
        'customer': customer,
        'wallet': wallet,
        'user_form': user_form,
    }
    return render(request, 'front/profile.html', context)

@login_required
def update_profile(request):
    if request.method == 'POST':
        user_form = UserProfileForm(request.POST, instance=request.user)
        if user_form.is_valid():
            user_form.save()
            return redirect('profile')  # Redirect to the profile page after saving
    else:
        user_form = UserProfileForm(instance=request.user)
    
    return render(request, 'profile.html', {'user_form': user_form})

@login_required(login_url='/login/')
def orders(request):
    user = request.user
    customer = Customer.objects.get(user=user)
    wallet = Wallet.objects.get(customer=customer)
    context = {
        'user': user,
        'customer': customer,
        'wallet': wallet,
    }
    return render(request, 'front/orders.html', context)

@login_required(login_url='/login/')
def wallet(request):
    user = request.user
    customer = Customer.objects.get(user=user)
    wallet = Wallet.objects.get(customer=customer)
    transactions = Transaction.objects.filter(wallet=wallet).order_by('-created_at')
    for transaction in transactions:
        logger.debug(f"Transaction ID: {transaction.id}, Date: {transaction.created_at}")    
        transaction.created_at = datetime2jalali(transaction.created_at).strftime('%Y-%m-%d %H:%M')
    paginator = Paginator(transactions, 5)

    page_number = request.GET.get('page') or 1
    page_obj = paginator.get_page(page_number)
    context = {
        'user': user,
        'customer': customer,
        'wallet': wallet,
        'transactions': transactions,
        'page_obj': page_obj,
    }
    return render(request, 'front/wallet.html', context)

@login_required(login_url='/login/')
def deposit_money(request):
    if request.method == 'POST':
        user = request.user
        customer = Customer.objects.get(user=user)
        wallet = Wallet.objects.get(customer=customer)
        # Create a new transaction with status 'pending'
        new_transaction = Transaction.objects.create(
            wallet=wallet,
            amount=request.POST.get('amount'),
            status='P',  # Assuming 'P' stands for 'pending'
            created_at=timezone.now()
        )
        return redirect('transaction_success')  # Redirect to a success page or wherever you want

    return render(request, 'front/deposit_money.html')

@login_required(login_url='/login/')
def transaction_success(request):
    return render(request, 'front/transaction_success.html')

@login_required(login_url='/login/')
def support(request):
    user = request.user
    customer = Customer.objects.get(user=user)
    wallet = Wallet.objects.get(customer=customer)
    context = {
        'user': user,
        'customer': customer,
        'wallet': wallet,
    }
    return render(request, 'front/support.html', context)

@csrf_protect
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            phone = form.cleaned_data['phone']
            try:
                user = User.objects.get(phone=phone)
            except User.DoesNotExist:
                user = User(phone=phone, username=phone)
                user.save()
                customer = Customer(user=user)
                customer.save()
                wallet = Wallet(customer=customer)
                wallet.save()

            otp = generate_otp()
            user.otp = otp
            user.save()

            return redirect('verify_otp', phone=phone)
    else:
        form = LoginForm()
    return render(request, 'front/login.html', {'form': form})

@csrf_protect
def verify_otp(request, phone):
    try:
        user = User.objects.get(phone=phone)
    except User.DoesNotExist:
        return redirect('login')

    print(f"""
            =====================================

             Received OTP for {phone}: {user.otp}
          
            =====================================
          """)
    
    if request.method == 'POST':
        form = OTPForm(request.POST)
        if form.is_valid():
            otp_received = form.cleaned_data['otp']
            if user.otp == otp_received:
                login(request, user)
                user.otp = None
                user.save()
                return redirect('profile')
            else:
                form.add_error('otp', 'Invalid OTP')
    else:
        form = OTPForm()
    return render(request, 'front/verify_otp.html', {'form': form, 'phone': phone})

def logout_confirmation(request):
    return render(request, 'front/logout_confirmation.html')

def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('/login/')
    return redirect('/profile/')