from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import WithdrawalRequest
from .forms import WithdrawalRequestForm
from django.contrib import messages

@login_required(login_url="/login")
def withdrawal_request_list(request):
    if request.user.is_active == False:
        return redirect("/logout")

    if request.user.is_admin == False:
        return redirect("/")

    withdrawal_requests = WithdrawalRequest.objects.all()
    return render(request, 'withdrawal_request_list.html', {'withdrawal_requests': withdrawal_requests})


@login_required(login_url="/login")
def edit_withdrawal_request(request, pk):
    if request.user.is_active == False:
        return redirect("/logout")

    if request.user.is_admin == False:
        return redirect("/")

    withdrawal_request = get_object_or_404(WithdrawalRequest, pk=pk)
    
    if request.method == 'POST':
        form = WithdrawalRequestForm(request.POST, instance=withdrawal_request)
        
        if form.is_valid():
            withdrawal_request = form.save(commit=False)  # Get the object without saving
            
            # Logic for balance adjustment
            if withdrawal_request.status == 'APPROVED':
                if withdrawal_request.user.pending_withdraw_balance >= withdrawal_request.amount:
                    withdrawal_request.user.total_withdrawed += withdrawal_request.user.pending_withdraw_balance
                    withdrawal_request.user.pending_withdraw_balance = withdrawal_request.user.pending_withdraw_balance - float(withdrawal_request.amount)
                    withdrawal_request.user.save()
                    
                    withdrawal_request.save()
                    messages.success(request, "Withdrawal request approved successfully.")
                    return redirect('/adminpanel/withdrawal-requests/')
                
                else:
                    messages.error(request, "Insufficient balance for approval.")
                    return redirect('/adminpanel/withdrawal-requests/')

            elif withdrawal_request.status == 'REJECTED':
                withdrawal_request.user.balance += float(withdrawal_request.amount)
                withdrawal_request.user.pending_withdraw_balance -= float(withdrawal_request.amount)
                withdrawal_request.user.save()  # Save the updated user balance

                withdrawal_request.save()  # Save the rejected request
                messages.success(request, "Withdrawal request rejected successfully.")
                return redirect('/adminpanel/withdrawal-requests/')
            
            # If the status is pending or unchanged, save the request
            withdrawal_request.save()
            messages.info(request, "Withdrawal request updated successfully.")
            return redirect('/adminpanel/withdrawal-requests/')

    else:
        form = WithdrawalRequestForm(instance=withdrawal_request)

    return render(request, 'edit_withdrawal_request.html', {'form': form})


@login_required(login_url="/login")
def delete_withdrawal_request(request, pk):
    if request.user.is_active == False:
        return redirect("/logout")
    
    if request.user.is_admin == False:
        return redirect("/")
    
    withdrawal_request = get_object_or_404(WithdrawalRequest, pk=pk)
    withdrawal_request.delete()
    return redirect('/adminpanel/withdrawal-requests/')
