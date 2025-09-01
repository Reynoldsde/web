from django.shortcuts import render, redirect
from .forms import InvitationCodeForm
from .models import invitation_code
from django.utils.crypto import get_random_string
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required

@login_required(login_url="/login")
def invitation_codes(request):
    if request.user.is_active == False:
        return redirect("/logout")

    if request.user.is_admin == False:
        return redirect("/")

    all_invitation = invitation_code.objects.all()
    return render(request, "invitation_code.html", {"invitation_codes": all_invitation})

@login_required(login_url="/login")
@require_POST
def delete_invitation_code(request, pk):
    if request.user.is_active == False:
        return redirect("/logout")
    
    if request.user.is_admin == False:
        return redirect("/")
    
    code = get_object_or_404(invitation_code, pk=pk)
    code.delete()
    return redirect('/adminpanel/codes')  # Redirect to the invitation codes list page

@login_required(login_url="/login")
def create_invitation_code(request):
    if request.user.is_active == False:
        return redirect("/logout")

    if request.user.is_admin == False:
        return redirect("/")
    
    if request.method == 'POST':
        form = InvitationCodeForm(request.POST)
        if form.is_valid():
            invitation_code = form.save(commit=False)
            invitation_code.save()
            return redirect('/adminpanel/codes')  # Redirect to the invitation code list page
    else:
        # Generate the code and pass it to the form
        code = get_random_string(8, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
        form = InvitationCodeForm(code=code)

    return render(request, 'create_invitation_code.html', {'form': form})