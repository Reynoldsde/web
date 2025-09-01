# views.py
from django.shortcuts import render, get_object_or_404, redirect
from .forms import VipPlanForm
from django.contrib.auth.decorators import login_required
from Account.models import vip_plans
from django.contrib import messages

@login_required(login_url="/login")
def vip_plan_list(request):
    if request.user.is_admin:
        plans = vip_plans.objects.all()
        return render(request, 'vip_plan_list.html', {'plans': plans})
    else:
        return redirect("/")

@login_required(login_url="/login")
def create_vip_plan(request):
    if request.user.is_admin:
        if request.method == 'POST':
            form = VipPlanForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('vip_plan_list')
        else:
            form = VipPlanForm()
        return render(request, 'vip_plan_form.html', {'form': form})
    else:
        return redirect("/")

@login_required(login_url="/login")
def edit_vip_plan(request, pk):
    if request.user.is_admin:
        plan = get_object_or_404(vip_plans, pk=pk)
        if request.method == 'POST':
            form = VipPlanForm(request.POST, instance=plan)
            if form.is_valid():
                form.save()
                return redirect('vip_plan_list')
        else:
            form = VipPlanForm(instance=plan)
        return render(request, 'vip_plan_form.html', {'form': form})
    else:
        return redirect("/")
    
@login_required(login_url="/login")
def delete_vip_plan(request, pk):
    if request.user.is_admin:
        plan = get_object_or_404(vip_plans, pk=pk)
        if request.method == 'POST':
            plan.delete()
            messages.success(request, 'VIP Plan deleted successfully.')
            return redirect('vip_plan_list')
        return render(request, 'delete_vip_plan.html', {'plan': plan})