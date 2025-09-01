from .models import customer_service_link
from django.shortcuts import render, redirect
from django.utils.crypto import get_random_string
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required


@login_required(login_url="/login")
def customer_service(request):
    if request.user.is_admin:
        if request.method == "POST":
            link = request.POST["link"]
            get_link = customer_service_link.objects.all()
            
            if get_link.exists():
                link_instance = get_link.first()
                link_instance.link = link
                link_instance.save()
            else:
                create_link = customer_service_link(link=link)
                create_link.save()

            return render(request, "customer_service_code.html", {"pre_url": get_link.first().link})
        
        get_link = customer_service_link.objects.all().first().link if customer_service_link.objects.all().exists() else ""
        return render(request, "customer_service_code.html", {"pre_url": get_link})
        