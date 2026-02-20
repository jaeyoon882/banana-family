from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from .models import Item,Category
from .forms import NewItemForm, EditItemForm

def browse(request):
    query = request.GET.get('query','')
    items = Item.objects.filter(is_sold=False)
    categories = Category.objects.all()
    category_id = request.GET.get('category','')
    
    if category_id:
        #the keyword 'category_id' -> automatically decided by django for foreign key of item model
        items = items.filter(category_id = category_id)
    
    #if user searched for something
    if query:
        #filter items that contains the query either in name or descrption of the item
        items = items.filter(Q(name__icontains=query) | Q(description__icontains=query))
    
    return render(request, 'item/browse.html', {
        'items':items,
        'query':query,
        'categories':categories,
        'category_id':category_id
    })

#renders product details page
def detail(request, pk):
    item = get_object_or_404(Item, pk=pk)
    #get 3 related items(exclude the chosen item) list
    related_items = Item.objects.filter(category=item.category, is_sold=False).exclude(pk=pk)[0:3]
    return render(request,'item/detail.html',{
        "item":item,
        "related_items":related_items
    })

@login_required
def new(request):
    #if client post new item
    if request.method == 'POST':
        #get everything from post request
        form = NewItemForm(request.POST,request.FILES)
        if form.is_valid():
            #commit false : not saving to database yet (not all attributes of item model is filled out)
            item = form.save(commit=False)
            item.created_by = request.user
            item.save()
            #redirect to details page of the item uploaded
            return redirect('item:detail',pk=item.id)

    else:
        form = NewItemForm()
        return render(request,'item/form.html',{
            "form":form,
            "title":'New item'
        })
        
@login_required
def delete(request,pk):
    item = get_object_or_404(Item, pk=pk, created_by = request.user)
    item.delete()
    return redirect('dashboard: index')

@login_required
def edit(request,pk):
    item = get_object_or_404(Item, pk=pk,created_by = request.user)
    if request.method == 'POST':
        form = EditItemForm(request.POST,request.FILES,instance=item)
        if form.is_valid():
            form.save()
            return redirect('item:detail',pk=item.id)

    else:
        form = EditItemForm(instance=item)
        return render(request,'item/form.html',{
            "form":form,
            "title":'Edit item'
        })
    
    
