from django.http import HttpResponse
from django.shortcuts import redirect,render
from lists.models import Item
# Create your views here.
def home_page(request):
    if request.method=='POST':
        Item.objects.create(text=request.POST['item_text'])
        return redirect('/')

    items=Item.objects.all()
    return render(request, 'home.html',{'items':items})
    #else:
        #new_item_text=''
    #item=Item()
    #item.text=request.POST.get('item_text', '')
    #item.save()
    
    return  render(request, 'home.html')#,{
        #'new_item_text': new_item_text,
   # })

