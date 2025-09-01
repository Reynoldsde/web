from django.shortcuts import render, get_object_or_404, redirect
from .models import account
from django.views.decorators.http import require_POST
from .forms import ClientForm
from django.db.models import Q
from .models import selection_log, finished_task
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib import messages

@login_required(login_url="/login")
def client_list(request):
    if request.user.is_active == False:
        return redirect("/logout")

    if request.user.is_admin == False:
        return redirect("/")
    
    query = request.GET.get('q', '')
    if query:
        clients = account.objects.filter(
            Q(username__icontains=query) |
            Q(name__icontains=query) |
            Q(email__icontains=query) |
            Q(phone__icontains=query)
        )
    else:
        clients = account.objects.all()

    return render(request, 'client_list.html', {'clients': clients})

@login_required(login_url="/login")
@require_POST
def delete_client(request, pk):
    if request.user.is_active == False:
        return redirect("/logout")

    if request.user.is_admin == False:
        return redirect("/")
    
    client = get_object_or_404(account, pk=pk)
    client.delete()
    return redirect('client_list')  # Redirect to the client list page

@login_required(login_url="/login")
def view_client(request, pk):
    if request.user.is_active == False:
        return redirect("/logout")

    if request.user.is_admin == False:
        return redirect("/")
    
    client = get_object_or_404(account, pk=pk)
    get_log =  finished_task.objects.filter(user_id=client).order_by('-pk')
    
    return render(request, 'view_client.html', {'client': client, "get_log": get_log})

@login_required(login_url="/login")
def edit_client(request, pk):
    if request.user.is_active == False:
        return redirect("/logout")
    
    if request.user.is_admin == False:
        return redirect("/")

    client = get_object_or_404(account, pk=pk)  # Ensure the model is correctly referenced

    if request.method == 'POST':
        form = ClientForm(request.POST, request.FILES, instance=client)
        if form.is_valid():
            form.save()
            return redirect('client_list')  # Redirect to client list after saving
    else:
        form = ClientForm(instance=client)

    return render(request, 'edit_client.html', {'form': form, 'client': client})

@login_required(login_url="/login")
def reset_premium_client(request):
    if request.user.is_admin:
        if request.method == "POST":
            client_id = request.POST["client_id"]
            
            get_client = account.objects.get(pk=client_id)
            get_client.task_index += 1
            get_client.encounter_negative = False
            get_client.save()
            
            messages.success(request, "Client Can Now Procceed With Task")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))