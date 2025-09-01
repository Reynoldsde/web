from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from adminpanel.models import WithdrawalRequest
from datetime import datetime
from django.contrib import messages


@login_required(login_url="/login")
def create_withdrawal_request(request):
    if request.user.is_active == False:
        return redirect("/logout")
    
    if request.method == 'POST':
        wallet_address = request.POST["wallet_address"]
        amount = request.POST["amount"]

        get_all_requests = WithdrawalRequest.objects.filter(user=request.user) if WithdrawalRequest.objects.filter(user=request.user).exists() else False

        if float(request.user.balance) < float(amount):
            messages.error(request, "Unable to place the order. You don't Have enough balance.")
            return redirect('/withdraw')   
        
        elif get_all_requests != False and get_all_requests.last().status == "PENDING":
            messages.error(request, "Unable to place the order. Please wait for your pending order to be fulfilled.")
            return redirect('/withdraw')
        else:
            create_request = WithdrawalRequest(user=request.user, wallet_address=wallet_address, amount=amount, request_date=datetime.now())
            create_request.save()
            
            request.user.pending_withdraw_balance = float(request.user.pending_withdraw_balance) + float(amount)
            request.user.balance = request.user.balance - float(amount)
            request.user.save()

            messages.success(request, "Your withdrawal request has been created. Please wait, and we will get back to you soon.")
            return redirect('/withdraw')

@login_required(login_url="/login")
def list_withdrawals(request):
    if request.user.is_active == False:
        return redirect("/logout")
    
    withdrawals = WithdrawalRequest.objects.filter(user=request.user)
    return render(request, 'list_withdrawals.html', {'withdrawals': withdrawals})
