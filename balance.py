from django.shortcuts import render, redirect
from django.db.models import Sum, F
from django.contrib.auth.decorators import login_required
from decimal import Decimal
from adminpanel.models import selection_log, WithdrawalRequest

@login_required(login_url="/login")
def balance_tracking(request):
    if request.user.is_active == False:
        return redirect("/logout")
    
    # Get the current user
    user = request.user

    total_commissions = selection_log.objects.filter(client_id=user).annotate(
        actual_commission=F('product_price') * F('product_commission') / 100.0
    ).aggregate(Sum('actual_commission'))['actual_commission__sum'] or 0.0

    # Round the total commissions to 3 decimal places
    total_commissions = round(float(total_commissions), 3)

    # Fetch all withdrawal requests
    withdrawals = WithdrawalRequest.objects.filter(user=user)

    # Calculate total withdrawals (approved ones as Decimal)
    total_withdrawals = withdrawals.filter(status='APPROVED').aggregate(Sum('amount'))['amount__sum'] or Decimal('0.00')
    total_withdrawals = round(float(total_withdrawals), 3)

    # Calculate current balance (commissions - withdrawals)
    current_balance = user.balance

    return render(request, 'balance_tracking.html', {
        'total_commissions': total_commissions,
        'total_withdrawals': total_withdrawals,
        'current_balance': current_balance,
        'withdrawals': withdrawals
    })
