from django.http import JsonResponse
from Account.models import account

def user_search(request):
    if request.user.is_admin:
        query = request.GET.get('q', '')
        users = account.objects.filter(name__icontains=query)[:10]
        results = [{'id': user.id, 'text': user.name} for user in users]
        return JsonResponse({'results': results})
    else:
        return ""