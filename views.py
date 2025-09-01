# views.py
from django.shortcuts import render, get_object_or_404, redirect
from .models import Task, product
from .forms import TaskForm, ProductForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Task List
login_required(login_url="/login")
def task_list(request):
    if request.user.is_admin == False:
        return redirect("/")
    
    tasks = Task.objects.all()
    return render(request, 'task_list.html', {'tasks': tasks})

# Create Task
login_required(login_url="/login")
def create_task(request):
    if request.user.is_admin == False:
        return redirect("/")

    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Task created successfully!')
            return redirect('task_list')
    else:
        form = TaskForm()
    return render(request, 'task_form.html', {'form': form})

# Edit Task
login_required(login_url="/login")
def edit_task(request, pk):
    if request.user.is_admin == False:
        return redirect("/")
    
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, 'Task updated successfully!')
            return redirect('task_list')
    else:
        form = TaskForm(instance=task)
    return render(request, 'task_form.html', {'form': form})

# Delete Task
login_required(login_url="/login")
def delete_task(request, pk):
    if request.user.is_admin == False:
        return redirect("/")
    
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        try:
            task.delete()
            messages.success(request, 'Task deleted successfully!')
            return redirect('task_list')
        except:
            messages.error(request, 'Task Have Active Products')
            return redirect('task_list')
    
    return render(request, 'task_confirm_delete.html', {'task': task})

# Product List
login_required(login_url="/login")
def product_list(request):
    if request.user.is_admin == False:
        return redirect("/")
    
    products = product.objects.all()
    return render(request, 'product_list.html', {'products': products})

# Create Product
login_required(login_url="/login")
def create_product(request):
    if request.user.is_admin == False:
        return redirect("/")
    
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product created successfully!')
            return redirect('product_list')
    else:
        form = ProductForm()
    return render(request, 'product_form.html', {'form': form})

# Edit Product
login_required(login_url="/login")
def edit_product(request, pk):
    if request.user.is_admin == False:
        return redirect("/")
    
    product_instance = get_object_or_404(product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product_instance)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product updated successfully!')
            return redirect('product_list')
    else:
        form = ProductForm(instance=product_instance)
    return render(request, 'product_form.html', {'form': form})

# Delete Product
login_required(login_url="/login")
def delete_product(request, pk):
    if request.user.is_admin == False:
        return redirect("/")
    
    product_instance = get_object_or_404(product, pk=pk)
    if request.method == 'POST':
        product_instance.delete()
        messages.success(request, 'Product deleted successfully!')
        return redirect('product_list')
    return render(request, 'product_confirm_delete.html', {'product': product_instance})
