from django.shortcuts import render, get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from item.models import Item
from .models import Conversation
from .forms import ConversationMessageForm

@login_required
def new_conversation(request, item_pk):
    #get item that correlates with item pk
    item = get_object_or_404(Item, pk = item_pk)   
    
    #if you created this item post
    if item.created_by == request.user:
        return redirect('dashboard:index')
    #first, get all conversations related to the item
    #then, get conversation in which request.user.id is included in members(in Conversation model)
    conversations = Conversation.objects.filter(item=item).filter(members__in=[request.user.id])
    
    #if conversation already exists, redirect to that conversation
    if conversations:
        return redirect('conversation:detail', pk=conversations.first().id)
    
    if request.method == 'POST':
        form = ConversationMessageForm(request.POST)
        if form.is_valid():
            #create Conversation object(insert item from above to item field in Conversation model)
            conversation = Conversation.objects.create(item=item)
            conversation.members.add(request.user)
            conversation.members.add(item.created_by)
            conversation.save()
            
            conversation_message = form.save(commit=False)
            conversation_message.conversation = conversation
            conversation_message.created_by = request.user
            conversation_message.save()
            
            return redirect('item:detail',pk=item_pk)
    
    else:
        form = ConversationMessageForm()
    
    return render(request,'conversation/new.html',{
        'form':form
    })
    

@login_required
def inbox(request):
    conversations = Conversation.objects.filter(members__in=[request.user.id])
    
    return render(request,'conversation/inbox.html',{
        'conversations': conversations
    })
    
@login_required
def detail(request, pk):
    conversation = Conversation.objects.filter(members__in=[request.user.id]).get(pk=pk)

    if request.method == 'POST':
        form = ConversationMessageForm(request.POST)

        if form.is_valid():
            conversation_message = form.save(commit=False)
            conversation_message.conversation = conversation
            conversation_message.created_by = request.user
            conversation_message.save()

            conversation.save()

            return redirect('conversation:detail', pk=pk)
    else:
        form = ConversationMessageForm()

    return render(request, 'conversation/detail.html', {
        'conversation': conversation,
        'form': form
    })