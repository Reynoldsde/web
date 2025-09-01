from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from chat.models import Conversation_Ticket, Message
from Account.models import account
from django.http import JsonResponse


@login_required(login_url="/login")
def chat(request):
    if request.user.is_admin:
        try:
            conversation_pk = request.GET['conversation']
        except:
            conversation_pk = None

        if conversation_pk:
            find_ticket = Conversation_Ticket.objects.filter(pk=conversation_pk)
            
            if find_ticket.exists():
                name = account.objects.get(pk=find_ticket.last().user).name
                all_conv = Conversation_Ticket.objects.all()
                all_messages = Message.objects.filter(ticket=find_ticket.last())

                for i in all_messages:
                    if i.read == False:
                        i.read = True
                        i.save()

                return render(request, "./chat_admin.html", {"conversation": all_messages, "conversations": all_conv, "conversation_pk": conversation_pk, "name": name})   
        
        all_conv = Conversation_Ticket.objects.all()
        return render(request, "./chat_admin.html", {"conversations": all_conv})
    


@login_required(login_url="/login")
def conversation_list_json(request):
    if request.user.is_admin:
        # Fetch all conversations
        conversations = Conversation_Ticket.objects.all()

        # Prepare conversation data
        conversation_data = []
        for conversation in conversations:
            last_message = Message.objects.filter(ticket=conversation).last()
            unread_count = Message.objects.filter(ticket=conversation, read=False).exclude(sender=request.user).count()

            conversation_data.append({
                "id": conversation.id,
                "user_name": account.objects.get(pk=conversation.user).name,  # Adjust according to your Account model
                "last_message": {
                    "content": last_message.content if last_message else None,  # Get content if last_message exists
                    "timestamp": last_message.timestamp.strftime('%m/%d/%Y %I:%M %p') if last_message else None,  # Format date
                } if last_message else None,
                "unread_messages": "&nbsp;" + str(unread_count) + " Messages&nbsp;" if unread_count != 0 else "",  # Only include count if greater than 0
                "last_date": last_message.timestamp.strftime('%m/%d/%Y %I:%M %p') if last_message else None,  # Format date if last_message exists
            })

        # Return JSON response
        return JsonResponse({"conversations": conversation_data}, status=200)


@login_required(login_url="/login")
def check_new_messages(request):
    if request.user.is_admin:
        unread_count = Message.objects.filter(read=False).exclude(sender=request.user).count()
        return JsonResponse({"unread_count": unread_count})