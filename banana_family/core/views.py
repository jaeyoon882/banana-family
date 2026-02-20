from django.shortcuts import render,redirect
from item.models import Category,Item
from .forms import SignupForm

#information about browser, ip address, if its get or post. going to be used in all views
def index(request):
    items = Item.objects.filter(is_sold=False)[0:6]
    categories = Category.objects.all()
    #core/index.html template에 데이터 전달
    return render(request, 'core/index.html', {
        'items':items,
        'categories':categories,
    })

def contact(request):
    return render(request,'core/contact.html')

def signup(request):
    #if the form is submitted
    if request.method == 'POST':
        form = SignupForm(request.POST) #pass all information from form
        if form.is_valid():
            #save to User database
            form.save()
            return redirect('/login/')
    else: 
        #create instance of SignupForm class
        form = SignupForm()
    
    return render(request,'core/signup.html',{
        'form':form
    })
    
