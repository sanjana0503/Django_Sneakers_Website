from django.conf import settings
from django.shortcuts import render,redirect
import razorpay
from .models import Product, Customer, Cart,OrderPlaced,Payment
from django.views import View
from django.db.models import Count
from .forms import CustomerRegistrationForm,CustomerProfileForm
from django.contrib import messages
from razorpay import Client




# Create your views here.
def home(request):
    return render(request, "app/home.html")

def about(request):
    return render(request, "app/about.html")

def contact(request):
    return render(request, "app/contact.html")

class CategoryView(View):
    def get(self,request,val):
        product= Product.objects.filter(category=val)
        title= Product.objects.filter(category=val).values('title')
        return render(request,"app/category.html",locals())

class CategoryTitle(View):
    def get(self,request,val):
        product = Product.objects.filter(title=val)
        title= Product.objects.filter(category=product[0].category).values('title')
        return render(request,"app/category.html",locals())

class ProductDetail(View):
    def get(self,request,pk):
        product= Product.objects.get(pk=pk)
        return render(request,"app/productdetail.html",locals())


class CustomerRegistrationView(View):
    def get(self,request):
        form= CustomerRegistrationForm()
        return render(request,'app/customerregistration.html',locals())
    def post(self,request):
        form= CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Congratulations! User Registered Successfully")
        else:
            messages.warning(request,"Invalid Input Data")
        return render(request,'app/customerregistration.html',locals())


class ProfileView(View):
    def get(self,request):
        form= CustomerProfileForm()
        return render(request,'app/profile.html',locals())
    
    def post(self,request):
        form= CustomerProfileForm(request.POST)
        if form.is_valid():
            user=request.user
            name=form.cleaned_data['name']
            locality= form.cleaned_data['locality']
            city=form.cleaned_data['city']
            size=form.cleaned_data['size']
            mobile= form.cleaned_data['mobile']
            state=form.cleaned_data['state']
            zipcode= form.cleaned_data['zipcode']
        


            reg = Customer(user=user,name=name,locality=locality,city=city,size=size,mobile=mobile,state=state,zipcode=zipcode)
            reg.save()
            messages.success(request,"Congratulations! Profile Saved Successfully")
        else:
            messages.warning(request,"Invalid Input Data")
        return render(request,'app/profile.html',locals())
    

def address(request):
    add = Customer.objects.filter(user=request.user)
    return render(request, 'app/address.html',locals())
    


class updateAddress(View):
    def get(self, request,pk):
        add =Customer.objects.get(pk=pk)
        form= CustomerProfileForm(instance=add)
        return render(request, 'app/updateAddress.html',locals())
    def post(self,request,pk):
        form= CustomerProfileForm(request.POST)
        if form.is_valid():
            add=Customer.objects.get(pk=pk)
            add.name=form.cleaned_data['name']
            add.locality= form.cleaned_data['locality']
            add.city=form.cleaned_data['city']
            add.mobile= form.cleaned_data['mobile']
            add.state=form.cleaned_data['state']
            add.zipcode= form.cleaned_data['zipcode']
            add.save()
            messages.success(request,"Congratulations! Profile Updated Successfully")
        else:
            messages.warning(request,"Invalid Input Data")
        return redirect("address")
    
def add_to_cart(request):
    user=request.user
    product_id=request.GET.get('prod_id')
    product=Product.objects.get(id=product_id)
    Cart(user=user,product=product).save()
    return redirect("/cart")

def show_cart(request):
    user=request.user         #to get the cart data where user is logged in
    cart= Cart.objects.filter(user=user)
    amount= 0
    for p in cart:
        value=p.quantity * p.product.discounted_price
        amount=amount + value
    totalamount= amount + 40
    return render(request,'app/addtocart.html',locals())

class checkout(View):
    def get(self,request):
        user=request.user
        add=Customer.objects.filter(user=user)
        cart_items=Cart.objects.filter(user=user)
        famount= 0
        for p in cart_items:
            value=p.quantity * p.product.discounted_price
            famount=famount + value
            totalamount=famount + 40
            razoramount= int(totalamount*100)
            client = razorpay.Client(auth=(settings.RAZOR_KEY_ID,settings.RAZOR_KEY_SECRET))
            data= {"amount":razoramount,"currency":"INR", "receipt":"order_rcptid_12"}
            payment_response = client.order.create(data=data)
            print(payment_response)
            # {'id': 'order_NGFNPClQNg2bz4', 'entity': 'order', 'amount': 54000, 'amount_paid': 0, 'amount_due': 54000, 'currency': 'INR', 'receipt': 'order_rcptid_12', 'offer_id': None, 'status': 'created', 'attempts': 0, 'notes': [], 'created_at': 1703434986}
            order_id = payment_response['id']
            order_status = payment_response['status']
            if order_status=="created":
                payment= Payment(
                    user=user,
                    amount=totalamount,
                    razorpay_order_id=order_id,
                    razorpay_payment_status= order_status
                )
                payment.save()
        return render(request, 'app/checkout.html', locals())
    

def payment_done(request):
    order_id = request.GET.get('order_id')
    payment_id = request.GET.get('payment_id')
    cust_id = request.GET.get('cust_id')

    # Debugging
    # print("payment done eid,order_id, old, payment_id, cid, cust id)

    user = request.user

    # Redirecting to "orders"
    # return redirect("orders")

    customer = Customer.objects.get(id=cust_id)  # To update payment status and payment id
    payment = Payment.objects.get(razorpay_order_id=order_id)

    payment.paid = True
    payment.razorpay_payment_id = payment_id
    payment.save()

    # To save order details
    cart = Cart.objects.filter(user=user)
    for c in cart:
        # Creating an OrderPlaced object
        OrderPlaced(user=user, customer=customer, product=c.product, quantity=c.quantity, payment=payment).save()
        c.delete()

    return redirect("orders")

def orders(request):
    order_placed=OrderPlaced.objects.filter(user=request.user)
    return render(request,'app/orders.html',locals())