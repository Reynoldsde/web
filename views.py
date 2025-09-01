from django.shortcuts import render, redirect
from products.models import product, show_product_list
from adminpanel.models import selection_log, finished_task, customer_service_link
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.contrib import messages
from chat.models import Conversation_Ticket, Message
from Account.models import vip_plans
from datetime import date
from adminpanel.models import Terms_and_conditions
from django.db.models import Q

@login_required(login_url="/login")
def home_page(request):
    if request.user.is_active == False:
        return redirect("/logout")
    
    find_ticket = Conversation_Ticket.objects.filter(user=request.user.pk)
    get_link = customer_service_link.objects.all().first().link if customer_service_link.objects.all().exists() else ""

    if find_ticket.exists():
        all_messages = Message.objects.filter(ticket=find_ticket.last())
        plans = vip_plans.objects.all()
        return render(request, "./homepage.html", {"conversation": all_messages, "plans": plans, "customer_service_user":get_link})   
    else:
        plans = vip_plans.objects.all()
        return render(request, "./homepage.html", {"plans": plans, "customer_service_user":get_link})


@login_required(login_url="/login")
def terms(request):
    if request.user.is_active == False:
        return redirect("/logout")
    
    terms_and = Terms_and_conditions.objects.all().first().terms if Terms_and_conditions.objects.all().exists() else ""
    
    return render(request, "./terms.html", {"terms": terms_and})

@login_required(login_url="/login")
def tasks(request):
    if request.user.is_active == False:
        return redirect("/logout")


    # Fetch products related to the current user based on show_product_list and premium status
    products_check = product.objects.filter(
        Q(task=request.user.assigned_task) & 
        (
            # Check if the product has an associated `show_product_list` and the user is in that list
            Q(id__in=show_product_list.objects.filter(user_account=request.user).values('product_id')) |
            # Or, if the product does not have an associated `show_product_list`, show it to all users
            ~Q(id__in=show_product_list.objects.values('product_id'))
        )
    ).distinct().order_by('id')


    # Convert the queryset to a list if needed
    client_products = list(products_check)
    
    # Retrieve task_name and task_index, with a default index of 0 if task_index is None
    task_name = request.user.assigned_task if request.user.assigned_task else ""
    index = request.user.task_index if request.user.task_index is not None else 0  # Set default index to 0

    # Handle the previous, current, and next products safely
    try:
        pre_product = client_products[index - 1] if index > 0 else None
        main_product = client_products[index] if index < len(client_products) else None
        pov_product = client_products[index + 1] if index < len(client_products) - 1 else None
    except:
        pre_product = False
        main_product = False
        pov_product = False

    if main_product == None:
        old_assigned_task = request.user.assigned_task.task_name if request.user.assigned_task != None else False
        request.user.assigned_task = None
        request.user.task_index = 0
        request.user.save()

        if selection_log.objects.filter(client_id=request.user).exists():
            messages.success(request, "Congratulations! Your set task is done")
        
        if old_assigned_task != False:
            create_log = finished_task(user=request.user, task_name=old_assigned_task, date=date.today())
            create_log.save()

    finished_task_counter = finished_task.objects.filter(user=request.user, date=date.today()).count()
    user_has_plan = True if request.user.vip_plan != None else False

    if user_has_plan:
        if finished_task_counter < request.user.vip_plan.sets_per_day:
            return render(request, "./tasks.html", {
                "products_check": products_check,
                "number_of_products": products_check.count(),
                "pre_product": pre_product,
                "main_product": main_product,
                "pov_product": pov_product,
                "task_name": task_name,
                "current_index": index,
                "recharge_message": "Reset your account"
            })
        else:
            return render(request, "./tasks.html", {
                "products_check": products_check,
                "number_of_products": products_check.count(),
                "pre_product": pre_product,
                "main_product": main_product,
                "pov_product": pov_product,
                "task_name": task_name,
                "current_index": index,
                "recharge_message": "Congrats, you have finished tasks of the day!"
            })      
    else:
        return render(request, "./tasks.html", {
            "products_check": products_check,
            "number_of_products": products_check.count(),
            "pre_product": pre_product,
            "main_product": main_product,
            "pov_product": pov_product,
            "task_name": task_name,
            "current_index": index,
            "recharge_message": "Contact Support to Assign Tasks"
        })         

@login_required(login_url="/login")
def update_index(request):
    if request.user.is_active == False:
        return redirect("/logout")

    if request.method == "POST":
        product_pk = request.POST["product"]
        selected_product = product.objects.get(pk=product_pk)
        
        total_recieved = float(selected_product.product_price) * float(selected_product.commission_rate / 100)

        if selected_product.premium_product == False or request.user.show_premium_products == False:
            save_log = selection_log(client_id=request.user, product_name=selected_product.product_name, date=datetime.now(), product_price=selected_product.product_price, product_commission=selected_product.commission_rate if request.user.vip_plan == None else request.user.vip_plan.profit_per_submission, total_received=total_recieved)
            save_log.save()
            
            request.user.balance += total_recieved
            request.user.save()

            request.user.balance = round(request.user.balance, 3)
            request.user.save()

            request.user.task_index = request.user.task_index + 1 if request.user.task_index else 0 + 1
            request.user.save()

            messages.success(request, f"Congratulations! You've earned a {total_recieved}$ commission")
            return redirect("/tasks/")
        else:
            if request.user.encounter_negative and request.user.balance < 0:
                messages.success(request, "Congratulations, You have encountered a premium product, contact customer service")
                return redirect("/tasks")
            
            elif request.user.encounter_negative and request.user.balance > 0:
                request.user.task_index = request.user.task_index + 1 if request.user.task_index else 0 + 1
                request.user.encounter_negative = False
                request.user.save()
                
                return redirect("/tasks")
            
            elif request.user.encounter_negative == False and request.user.balance > 0:
                save_log = selection_log(client_id=request.user, product_name=selected_product.product_name, date=datetime.now(), product_price=selected_product.product_price, product_commission=None, total_received=selected_product.negative_amount)
                save_log.save()

                if selected_product.negative_amount >= 0:
                    request.user.balance += (selected_product.negative_amount * -1)
                    request.user.save()
                
                elif selected_product.negative_amount < 0:
                    request.user.balance += selected_product.negative_amount
                    request.user.save()

                request.user.balance = round(request.user.balance, 3)
                request.user.encounter_negative = True
                request.user.save()

                messages.success(request, "Congratulations, You have encountered a premium product, contact customer service")
                return redirect("/tasks")
            
            elif request.user.balance == 0:
                messages.error(request, "You Don't Have Enough Balance")
                return redirect("/tasks")