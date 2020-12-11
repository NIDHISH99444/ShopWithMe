from django.shortcuts import render,redirect
from store.forms.authforms import CustomerCreationForm,CustomerAuthForm
from django.contrib.auth import authenticate,login as loginUser,logout
from store.models import Tshirt ,SizeVariant,Cart,Order,OrderItem,Payment,Occasion,IdealFor,NeckType,Sleeve,Brand,Color
from math import floor
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from store.forms.checkout_form import CheckForm
from instamojo_wrapper import Instamojo
from Tshop.settings import API_KEY,AUTH_TOKEN
# Create your views here
API = Instamojo(api_key=API_KEY, auth_token=AUTH_TOKEN, endpoint='https://test.instamojo.com/api/1.1/')

def home(request):
    tshirts=[]
    tshirts=Tshirt.objects
    query=request.GET   
    brand=query.get('brand')
    neckType=query.get('neckType')
    color=query.get('color')
    idealFor=query.get('idealFor')
    sleeve=query.get('sleeve')

    print("brand ->",brand)
    if brand!='' and brand is not None:
        print("inside")
        tshirts=tshirts.filter(brand__slug=brand)
    if neckType!='' and neckType is not None:
        print("inside")
        tshirts=tshirts.filter(neck_type__slug=neckType) 
    if color!='' and color is not None:
        print("inside")
        tshirts=tshirts.filter(color__slug=color)
    if idealFor!='' and idealFor is not None:
        print("inside")
        tshirts=tshirts.filter(ideal_for__slug=idealFor)
    if sleeve!='' and sleeve is not None:
        print("inside")
        tshirts=tshirts.filter(sleeve__slug=sleeve)

    else:
        print("outside")
        tshirts=tshirts.all()

    occasion=Occasion.objects.all()
    idealFor=IdealFor.objects.all()
    neckType=NeckType.objects.all()
    sleeve=Sleeve.objects.all()
    brand=Brand.objects.all()
    color=Color.objects.all()


    
    cart=request.session.get('cart')
    print("thing in cart",cart)
    context = {
                "tshirts": tshirts,
                "occasion": occasion,
                "idealFor" : idealFor,
                "neckType" : neckType,
                "sleeve" : sleeve,
                "brand" : brand,
                "color" : color
            }
  
    
    return render(request, template_name="store/home.html",context=context)


def cart(request):
    cart = request.session.get('cart')
    print("Cart details->",cart)
    if cart is None:
        cart = []

    for c in cart:
        tshirt_id = c.get('tshirt')
        tshirt = Tshirt.objects.get(id=tshirt_id)
        c['size'] = SizeVariant.objects.get(tshirt=tshirt_id, size=c['size'])
        c['tshirt'] = tshirt

    print(cart)
    return render(request,
                  template_name='store/cart.html',
                  context={'cart': cart})
                  
def login(request):
    if (request.method == 'GET') :
        
        form= CustomerAuthForm()
        next_page=request.GET.get('next')
        
        if next_page is not None:
            request.session['next_page']=next_page

        context = {
                "form": form
            }
        return render(request, template_name="store/login.html",context=context)
    else:
        print("reqested data",request.POST)
        form=CustomerAuthForm(data=request.POST)
        if form.is_valid():
            username=form.cleaned_data.get("username")
            password=form.cleaned_data.get("password")
            user =authenticate(username=username,password=password)
            if user:
                loginUser(request,user)

                session_cart=request.session.get('cart')
                print("checking cart data ->",session_cart)
                if session_cart is None:
                    session_cart=[]
                else:
                    for c in session_cart:
                        size=c.get('size')
                        quantity= c.get('quantity')
                        tshirt_id=c.get('tshirt')
                        cart_obj=Cart()
                        cart_obj.sizeVariant= SizeVariant.objects.get(size=size,tshirt=tshirt_id)
                        cart_obj.quantity=quantity
                        cart_obj.user=user
                        cart_obj.save()


                cart =Cart.objects.filter(user=user)
                print("cart data",cart)
                

                
                for c in cart :
                    obj={
                        'size': c.sizeVariant.size,
                        'tshirt':c.sizeVariant.tshirt.id,
                        'quantity' : c.quantity

                    } 
                    session_cart.append(obj)
                request.session['cart'] =session_cart
                print("Session data", request.session)
                next_page=request.session.get('next_page')
                print("POST next page is ",next_page)
                if next_page is None:
                    next_page="home"
                return redirect(next_page)
        else:
            context = {
                    "form": form
                }
            return render(request, template_name="store/login.html",context=context)

@login_required(login_url='/login')
def orders(request):
    user=request.user
    print("user  is ",user)
    orders=Order.objects.filter(user=user).order_by('-date').exclude(order_status="PENDING")
    context={
        'orders' : orders
    }
    return render(request, template_name="store/orders.html",context=context)


def signup(request):
    if request.method == 'GET':
        print(request.method)
        form = CustomerCreationForm()
        context = {
            "form": form
        }
        return render(request, template_name="store/signup.html", context=context)
    else:
        print(request.method)
        form = CustomerCreationForm(request.POST)
        if form.is_valid():
            user=form.save()
            user.email =user.username
            user.save()
            print("User",user)
            return render(request,template_name="store/login.html")
        else:
            context = {
            "form": form
            }
            return render(request,template_name="store/signup.html", context=context)

def signout(request):
    logout(request)
    return render(request,template_name="store/home.html")


def show_product(request ,slug):
    tshirt=Tshirt.objects.get(slug=slug)
    
    size= request.GET.get('size')
    if size is None:
        size=tshirt.sizevariant_set.all().order_by('price').first()
    else:
        size=tshirt.sizevariant_set.get(size=size)
    print("size is ",size)
    size_price=size.price
    sell_price=floor(size_price-(size_price * tshirt.discount/100))

    context={
        'tshirt' : tshirt,
        'price' : size_price,
        'sell_price' :sell_price,
        'active_size' :size
    }
    return render(request,template_name='store/product_details.html',context=context)

def add_to_cart(request,slug,size):
    cart =request.session.get('cart')
    user=None
    
    if request.user.is_authenticated:
        user=request.user
    print("User is ",user)
        
    if cart is None:
        cart=[]
    tshirt=Tshirt.objects.get(slug=slug)
    
    add_cart_for_anom_user(cart,size,tshirt)
    

    if user is not None:
        add_cart_to_database(user,size,tshirt)
    
        

    request.session['cart']=cart
    return_url=request.GET.get('return_url')
    
    return redirect(return_url)


def add_cart_to_database(user,size ,tshirt):
    size=SizeVariant.objects.get(size=size,tshirt=tshirt)
    existing= Cart.objects.filter(user=user, sizeVariant=size)
    print("existing-->",existing)
    if len(existing) > 0 :
        obj =existing[0]
        obj.quantity =obj.quantity+1
        obj.save()
    else:
        c=Cart()
        c.user=user
        c.sizeVariant=size
        c.quantity=1
        c.save()

def add_cart_for_anom_user(cart,size,tshirt):
    flag=True
    for cart_obj in cart : 
        t_id=cart_obj.get('tshirt')
        size_short=cart_obj.get('size')
        if t_id == tshirt.id and size==size_short:
            flag=False
            cart_obj['quantity']=cart_obj['quantity']+1

    if flag:
        cart_obj={
            'tshirt' : tshirt.id,
            'size' : size , 
            'quantity': 1 
        }
        cart.append(cart_obj)

@login_required(login_url='/login')
def checkout(request):
    if request.method=='GET':
        #get request
        form=CheckForm()
        cart=request.session.get('cart')
        if cart is None:
            cart=[]
        
        for c in cart:
            size_str= c.get('size')
            tshirt_id= c.get('tshirt')
            
            size_obj=SizeVariant.objects.get(size=size_str , tshirt=tshirt_id)
            c['size']=size_obj
            c['tshirt']=size_obj.tshirt

        print(cart)   


        context={
            'form':form,
            'cart':cart
        }
        return render(request,template_name="store/checkout.html",context=context)
    else:
        #post request
        form = CheckForm(request.POST)
        user=None
        if request.user.is_authenticated : 
            user=request.user
        if form.is_valid():
            shipping_address=form.cleaned_data.get('shipping_address')
            phone=form.cleaned_data.get('phone')
            payment_method=form.cleaned_data.get('payment_method')
            
            cart=request.session['cart']
            if cart is  None:
                cart=[]
            for c in cart:
                size_str= c.get('size')
                tshirt_id= c.get('tshirt')
                
                size_obj=SizeVariant.objects.get(size=size_str , tshirt=tshirt_id)
                c['size']=size_obj
                c['tshirt']=size_obj.tshirt

            total=cal_total_payable_amount(cart)
            print("Details ->",shipping_address,phone,payment_method,total)
            order=Order()
            order.shipping_address=shipping_address
            order.phone=phone
            order.payment_method=payment_method
            order.total=total
            order.order_status="PENDING"
            order.user=user
            order.save()
           
            #saving order items 
            for c in cart : 
                order_item= OrderItem()
                order_item.order =order
                size=c.get('size')
                tshirt=c.get('tshirt')
                order_item.price= floor(size.price-(size.price *tshirt.discount/100))
                order_item.quantity = c.get('quantity')
                order_item.size =size
                order_item.tshirt=tshirt
                order_item.save()
            response = API.payment_request_create(
            amount=order.total,
            purpose='Payment for Tshirts',
            buyer_name=f'{user.first_name} {user.last_name}',
            send_email=True,
            email=user.email,
            redirect_url="http://localhost:8000/validate_payment"
            )
            print(response['payment_request'])
            payment_request_id= response['payment_request']['id']
            url= response['payment_request']['longurl']
            payment=Payment()
            payment.order=order
            payment.payment_request_id=payment_request_id
            payment.save()

            return redirect(url)
        else:
            print("not a valid data")
            return redirect("checkout")

def cal_total_payable_amount(cart):
    total=0
    print("Session cart data ",cart)
    for c in cart: 
        
        discount=c.get('tshirt').discount
        price=c.get('size').price
        sale_price=floor(price-(price *discount/100))
        total_of_single_product=sale_price * c.get('quantity')
        total+=total_of_single_product 
    return total


def validatePayment(request):
    user=None
    if request.user.is_authenticated : 
        user=request.user
    print("User is ",user)
    payment_request_id=request.GET.get('payment_request_id')
    payment_id=request.GET.get('payment_id')
    print(payment_request_id , payment_id)
    response = API.payment_request_payment_status(payment_request_id,payment_id)
    status=response.get('payment_request').get('payment').get('status')
    if status != "Failed":
        print("Payment Success")
        try:
            payment=Payment.objects.get(payment_request_id=payment_request_id)
            payment.payment_id=payment_id
            payment.payment_status=status
            payment.save()

            orders=payment.order
            orders.order_status="PLACED"
            orders.save()
            cart=[]
            print("inside here")
            request.session['cart']=cart
            print("Seesion data",request.session['cart'])
            Cart.objects.filter(user=user).delete()
            return redirect('orders')
        except:
            return render(request,template_name="store/payment_failed.html")
    else:
        #return error page 
        return render(request,template_name="store/payment_failed.html")
    