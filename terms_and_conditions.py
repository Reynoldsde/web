from .models import Terms_and_conditions
from django.shortcuts import render, redirect
from django.utils.crypto import get_random_string
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required


@login_required(login_url="/login")
def edit_terms(request):
    if request.user.is_admin:
        if request.method == "POST":
            content = request.POST["content"]
            get_link = Terms_and_conditions.objects.all()
            
            if get_link.exists():
                link_instance = get_link.first()
                link_instance.terms = content
                link_instance.save()
            else:
                create_link = Terms_and_conditions(terms=content)
                create_link.save()

            return redirect("/adminpanel/edit_terms")
        
        terms_and = Terms_and_conditions.objects.all().first().terms if Terms_and_conditions.objects.all().exists() else ""
        return render(request, "edit_terms.html", {"terms": terms_and})
        