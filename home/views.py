from django.shortcuts import render
from django.http import JsonResponse
# Create your views here.
from django.shortcuts import render
from math import ceil
import json
import  datetime
# Create your views here.
from django.shortcuts import render,HttpResponse,redirect
from home.models import *
from  django.contrib.auth.models import User 
from django.contrib.auth import logout,authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login
from  django.contrib import messages
from .algo import *

from datetime import datetime ,timedelta,date
      
from django.shortcuts import render
from django.template import RequestContext
from django.contrib import messages
import pymysql
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
import os
from datetime import date
import os
import json
from web3 import Web3, HTTPProvider
import ipfshttpclient as  ips
import os
from django.core.files.storage import FileSystemStorage
import pickle
deployed_contract = '0xF597653688B174DeF777C473f4c762E60DAe29cd'
def getpoduct_function(lefn):
    blockchain_address = 'http://127.0.0.1:9545' #Blokchain connection IP
    web3 = Web3(HTTPProvider(blockchain_address))
    web3.eth.defaultAccount = web3.eth.accounts[0]
    compiled_contract_path = 'Ecommerce.json' #ecommerce contract code
    deployed_contract_address = deployed_contract #hash address to access student contract
    with open(compiled_contract_path) as file:
        contract_json = json.load(file)  # load contract info as JSON
        contract_abi = contract_json['abi']  # fetch contract's abi - necessary to call its functions
    file.close()
    contract = web3.eth.contract(address=deployed_contract_address, abi=contract_abi) #now calling contract to access data
   
    details = contract.functions.getProduct().call()  
    # print(details)

    objects = []
    rows = details.split("\n")
    x = len(rows)-1
    if lefn != 0:
        if x >lefn:
            x =lefn

        
  
        
    for i in range(x):
        arr = rows[i].split("#")
        # print("my=== "+str(arr[0])+" "+arr[1]+" "+arr[2]+" ")
        if arr[0] == 'addproduct':
               
            obj = {
                    "supplier": arr[1],
                    "productname": arr[2],
                    "prize": arr[3],
                    "qty": arr[4],
                    "desc":arr[5],
                    "img":"http://127.0.0.1:8000/media/shop/images/7v3hvjcixb14y1zhw9pd.jpg",
                    "slug": f"\BookOrder?farmer='+arr[1]+'&crop={arr[2]}"
                } 
            # print(arr,obj)

            objects.append(obj)
    # print(objects)
    return objects

details = ""

def readDetails(contract_type):
    global details
    details = ""
    print(contract_type+"======================")
    blockchain_address = 'http://127.0.0.1:9545' #Blokchain connection IP
    web3 = Web3(HTTPProvider(blockchain_address))
    web3.eth.defaultAccount = web3.eth.accounts[0]
    compiled_contract_path = 'Ecommerce.json' #ecommerce contract code
    deployed_contract_address = deployed_contract #hash address to access student contract
    with open(compiled_contract_path) as file:
        contract_json = json.load(file)  # load contract info as JSON
        contract_abi = contract_json['abi']  # fetch contract's abi - necessary to call its functions
    file.close()
    contract = web3.eth.contract(address=deployed_contract_address, abi=contract_abi) #now calling contract to access data
    if contract_type == 'signup':
        details = contract.functions.getUser().call()
    if contract_type == 'addproduct':
        details = contract.functions.getProduct().call()
    if contract_type == 'bookorder':
        details = contract.functions.getOrder().call()    
    print(details)   

def saveDataBlockChain(currentData, contract_type):
    global details
    global contract
    details = ""
    blockchain_address = 'http://127.0.0.1:9545'
    web3 = Web3(HTTPProvider(blockchain_address))
    web3.eth.defaultAccount = web3.eth.accounts[0]
    compiled_contract_path = 'Ecommerce.json' #ecommerce contract file
    deployed_contract_address = deployed_contract #contract address
    with open(compiled_contract_path) as file:
        contract_json = json.load(file)  # load contract info as JSON
        contract_abi = contract_json['abi']  # fetch contract's abi - necessary to call its functions
    file.close()
    contract = web3.eth.contract(address=deployed_contract_address, abi=contract_abi)
    readDetails(contract_type)
    if contract_type == 'signup':
        details+=currentData
        msg = contract.functions.addUser(details).transact()
        tx_receipt = web3.eth.waitForTransactionReceipt(msg)
    if contract_type == 'addproduct':
        details+=currentData
        msg = contract.functions.addProduct(details).transact()
        tx_receipt = web3.eth.waitForTransactionReceipt(msg)
    if contract_type == 'bookorder':
        details+=currentData
        msg = contract.functions.bookOrder(details).transact()
        tx_receipt = web3.eth.waitForTransactionReceipt(msg)

# Create your views here.
def home(request): 
   
    if request.user.is_authenticated:
        now = datetime.now()
        last = date.today() - timedelta(days=30)
        timestamp = datetime.date(now)
        


        customer = request.user
        # order ,created = Order.objects.get_or_create(customer=customer,complete=False)
        # items = order.orderitems_set.all()
        # cartitems = order.get_cart_item

        # latest = products.objects.filter(pub_date__range=[last, timestamp])
            
        dataa = getpoduct_function(10),
                
        context = {'latest' : dataa,}
    else:
        latest = getpoduct_function(10)
        
        dataa = products.objects.all()
        context = {'dataa' : dataa,"latest":latest}
    

    return render(request,'home.html',context)
def cart(request):
    customer = request.user
    order ,created = Order.objects.get_or_create(customer=customer,complete=False)
    items = order.orderitems_set.all()
    cartitems = order.get_cart_item



    
    order ,created = Order.objects.get_or_create(customer=customer,complete=False)
    items = order.orderitems_set.all()
    context = {'items':items,'order':order,'cartitems':cartitems}


    return render(request,'cart.html',context)


def updatecart(request):
    data = json.loads(request.body)
    productid = data['productsid']
    action = data['action']
    
    customer = request.user
    product = products.objects.get(id=productid)
    order ,created = Order.objects.get_or_create(customer=customer,complete=False)
    orderitems ,created = Orderitems.objects.get_or_create(order=order,product=product)
    cartitems = order.get_cart_item
    if action == 'add':
        
        orderitems.quantity = (orderitems.quantity + 1)

    elif action == "remove":
            orderitems.quantity = (orderitems.quantity-1)
    elif action == 'delete':
        orderitems.quantity = 0


    orderitems.save()
    if orderitems.quantity <= 0 :
            orderitems.delete()
    

    return JsonResponse("your cart is added",safe=False)



def processorder(request):
    print('data:',request.body)
    customer = request.user
    transection_id = datetime.datetime.now().timestamp
    order ,created = Order.objects.get_or_create(customer=customer,complete=False)

    data = json.loads(request.body)
    total = float(data['form']['total'])
    order.transaction_id = transection_id
    print(transection_id)
    if total == order.get_cart_total:
        order.complete = True
    order.save()

    if order.complete == True:
        ShippingOrder.objects.create(
            customer = customer,
            order = order,
            
            address =data['shipping']['address'],
            city = data['shipping']['country'],

            zipcode = data['shipping']['zip'],
            
            state =  data['shipping']['state'],
        )
         
    return JsonResponse("payment has been done....",safe=False)




def check(request):
    return render(request,'check.html')

def checkout(request):
    customer = request.user
    order ,created = Order.objects.get_or_create(customer=customer,complete=False)
    items = order.orderitems_set.all()
    cartitems = order.get_cart_item
    context = {'items':items,'order':order,'cartitems':cartitems}
    


    return render(request,'checkout.html',context)
def search(request):
    return render(request,'search.html')


def singleproduct(request):
    
       
    if request.method == 'GET':
        global details
        pid = request.GET['crop']
        user = ''
        with open("session.txt", "r") as file:
            for line in file:
                user = line.strip('\n')
        file.close()
        det = getpoduct_function(100)

        # print(det)
        for i  in range(len(det)):
            if det[i]['productname'] == pid:
                print(det[i])
                break

        single = det[i]
        context = {'single' : single,"username":user}
        return render(request,'singleproduct.html',context)

    

    
def tracker(request):
    product = products.objects.all()
    print(product)
    n = len(product)
    nSlides = n//4 + ceil((n/4)-(n//4))
    params = {'no_of_slides':nSlides, 'range': range(1,nSlides),'product': product}
    return render(request, 'tracker.html', params)

    
        

    return render(request,'tracker.html',context)
def user(request):

    
    product= products.objects.all()
    allProds=[]
    catprods= products.objects.values('sub_category', 'id')
    cats= {item["sub_category"] for item in catprods}
    for cat in cats:
        prod=products.objects.filter(sub_category=cat)
        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        allProds.append([prod, range(1, nSlides), nSlides])

    params={'allProds':allProds 
    }
    return render(request,"tracker.html", params)

    

    
def Contact(request):
    if request.method =="POST":
            name = request.POST['Name']
            email = request.POST['Email']
            phn = request.POST['Phoneno']
            desc = request.POST['Message']
               
              
            ins = contact(name=name,desc=desc,phn=phn,email=email)
            ins.save()
            messages.success(request,"your details has been recorded")



    
    return render(request,'contact.html')

def productss(request):
       
    if request.user.is_authenticated:
        
        customer = request.user
        order ,created = Order.objects.get_or_create(customer=customer,complete=False)
        items = order.orderitems_set.all()
        cartitems = order.get_cart_item


        latest = products.objects.filter(pub_date__range=["2020-09-17", "2020-09-18"])
        
        # dataa = products.objects.all()
        dataa =  getpoduct_function(10)
            
        context = {'dataa' : dataa,'items':items,"latest":latest,'cartitems':cartitems}
        
        return render(request,'products.html',context)
    else:
        user = ''
        with open("session.txt", "r") as file:
            for line in file:
                user = line.strip('\n')
        file.close()
        
        
        dataa = getpoduct_function(100)
        #  dataa = products.objects.all()
            
        context = {'dataa' : dataa,'username':user}
    
        return render(request,'products.html',context)




#api
def login(request):
    if request.method == 'POST':
       loginuser = request.POST['loginuser'] 
       loginPassword= request.POST['loginPassword']
       user = authenticate(username=loginuser,password=loginPassword)
       if user is not None:
            auth_login(request,user)
            messages.success(request,"sucessfully login")
            
            return redirect('home')
       else:
           messages.error(request,'invalid username')
           return redirect('login')
  
    return render(request,'login.html')
def logouts(request):
    logout(request)
    messages.success(request,'successfully logout')
    return redirect('home')
    



def signin(request):
    if request.method == 'POST':
       user = request.POST['signupuser'] 
       email = request.POST['signupemail']
       signupfname = request.POST['signupfname']
       signupsname = request.POST['signupsname']
       pass1 = request.POST['inputPassword1']
       pass2 = request.POST['inputPassword2']
       if len(user) > 10:
            messages.error(request,"user name should be less than 10 characters")
            return redirect('home')
            
       if pass1 != pass2:
            messages.error(request,"passwoard should be match")
            return redirect('home')

       if not user.isalnum():
            messages.error(request,"username must be in alphabhates and numaric")
            return redirect('home')



       myuser = User.objects.create_user(user,email,pass1)
       myuser.first_name= signupfname
       myuser.last_name = signupsname
       myuser.save()
       messages.success(request,"your account has been successfully created")
       create_cus = Customer.objects.get_or_create(user=user,name=signupfname,email=email)
       create_cus.save()
       return redirect('signin')
       
    else:
        return render(request,'signinpage.html')  

       

def UserLogin(request):
    if request.method == 'POST':
        username = request.POST.get('username', False)
        password = request.POST.get('password', False)
        usertype = request.POST.get('type', False)
        status = 'none'
        readDetails("signup")
        
        rows = details.split("\n")

        for i in range(len(rows)-1):
            arr = rows[i].split("#")
            if arr[0] == "signup":
                if arr[1] == username and arr[2] == password and arr[6] == usertype:
                    status = 'success'
                    break
        if status == 'success' and usertype == 'Supplier':
            file = open('session.txt','w')
            file.write(username)
            file.close()
            # context= {'data':"Welcome "+username}
            context= {'data':"Welcome "+username,'username':username}
            messages.success(request,"sucessfully login")
            
            return render(request,'tracker.html',context)  
            
        elif status == 'success' and usertype == 'Consumer':
            file = open('session.txt','w')
            file.write(username)
            file.close()
            context= {'data':"Welcome "+username,'username':username}
            messages.success(request,"sucessfully login")
            
            return render(request,'home.html',context)  
            
        else:
            context= {'data':'Invalid login details'}
            messages.error(request,'invalid username')
            return redirect('login')   


   
def Signup(request):
    if request.method == 'POST':
        username = request.POST.get('username', False)
        password = request.POST.get('password', False)
        contact = request.POST.get('contact', False)
        email = request.POST.get('email', False)
        address = request.POST.get('address', False)
        usertype = request.POST.get('type', False)
        print(username,password,contact,email,address,usertype)
        record = 'none'
        readDetails("signup")
        rows = details.split("\n")
        for i in range(len(rows)-1):
            arr = rows[i].split("#")
            if arr[0] == "signup":
                if arr[1] == username:
                    record = "exists"
                    break
        if record == 'none':
            data = "signup#"+username+"#"+password+"#"+contact+"#"+email+"#"+address+"#"+usertype+"\n"
            saveDataBlockChain(data,"signup")
            context= {'data':'Signup process completd and record saved in Blockchain'}
            # return render(request, 'Register.html', context)
            return redirect('login')
        else:
            context= {'data':username+' Username already exists'}
            # return render(request, 'Register.html', context)    
            return redirect('login')
            # return render(request, 'Register.html', context)    

def BookOrder(request):
    if request.method == 'GET':
        global details
        pid = request.GET['crop']
        user = ''
        with open("session.txt", "r") as file:
            for line in file:
                user = line.strip('\n')
        file.close()
        readDetails("signup")
        rows = details.split("\n")
        for i in range(len(rows)-1):
            arr = rows[i].split("#")
            if arr[0] == "signup":
                if arr[1] == user:
                    details = arr[3]+","+arr[4]+","+arr[5]
                    break
        today = date.today()            
        data = "bookorder#"+pid+"#"+user+"#"+details+"#"+str(today)+"\n"
        saveDataBlockChain(data,"bookorder")
        output = 'Your Order details Updated<br/>'
        messages.success(request,"sucessfully login")
        context= {'data':output,'username':user}
        return redirect("products")     


def AddProductAction(request):
    if request.method == 'POST':
        cname = request.POST.get('t1', False)
        qty = request.POST.get('t2', False)
        price = request.POST.get('t3', False)
        desc = request.POST.get('t4', False)
        print(cname,qty,price,desc)
        # image = request.FILES['t5'].read()
        # imagename = request.FILES['t5'].name
        user = ''
        with open("session.txt", "r") as file:
            for line in file:
                user = line.strip('\n')
        file.close()
        # myfile = pickle.dumps(image)
        # hashcode = api.add_pyobj(myfile)
        hashcode = "d"
        data = "addproduct#"+user+"#"+cname+"#"+price+"#"+qty+"#"+desc+"#"+hashcode+"\n"
        saveDataBlockChain(data,"addproduct")
        context= {'data':"Product details saved and IPFS image storage hashcode = "+hashcode,'username':user}
        messages.success(request,"sucessfully added products")
        return render(request,'tracker.html',context)
        
def ViewOrders(request):
    if request.method == 'GET':
        global details
        user = ''
        with open("session.txt", "r") as file:
            for line in file:
                user = line.strip('\n')
        file.close()
        output = '<table border=1 align=center>'
        objects = []
        readDetails("bookorder")
        rows = details.split("\n")
        for i in range(len(rows)-1):
            arr = rows[i].split("#")
            if arr[0] == 'bookorder':
                print(arr[2]+" "+user)
                details = arr[3].split(",")
                pid = arr[1]
                user = arr[2]
                book_date = arr[4]
                obj = {
                    "productname":pid,
                    "customername": user,
                    "contactno": details[0],
                    "Email":details[1],
                    "Address":details[2],
                    "Ordered_Date":str(book_date)             } 
                objects.append(obj)
        context= {'data':objects,'username':user}
        return render(request, 'vieworders.html', context)     


def updateQuantityBlock(currentData):
    blockchain_address = 'http://127.0.0.1:9545'
    web3 = Web3(HTTPProvider(blockchain_address))
    web3.eth.defaultAccount = web3.eth.accounts[0]
    compiled_contract_path = 'Ecommerce.json' #student contract file
    deployed_contract_address = deployed_contract#contract address
    with open(compiled_contract_path) as file:
        contract_json = json.load(file)  # load contract info as JSON
        contract_abi = contract_json['abi']  # fetch contract's abi - necessary to call its functions
    file.close()
    contract = web3.eth.contract(address=deployed_contract_address, abi=contract_abi)
    msg = contract.functions.addProduct(currentData).transact()
    tx_receipt = web3.eth.waitForTransactionReceipt(msg)


def viewproducts(request):
    if request.method == 'GET':
        print("anna namsthe")

        user = ''
        with open("session.txt", "r") as file:
            for line in file:
                user = line.strip('\n')
        file.close()
        index = 0
        obj = []
        record = ''
        readDetails("addproduct")
        rows = details.split("\n")
        tot_qty = 0
        for i in range(len(rows)-1):
            arr = rows[i].split("#")
            if arr[0] == "addproduct":
                if arr[1] == user:
                    record = arr[0]+"#"+arr[1]+"#"+arr[2]+"#"+arr[3]+"#"+str(tot_qty)+"#"+arr[5]+"#"+arr[6]+"\n"
                    record1 = {
                        "productname":arr[2],
                        "qty":arr[4],
                        "prize":arr[3],
                        "desc":arr[5] 
                    }
                    # print(record1)
                    obj.append(record1)
        print(obj)
        context= {'data':obj,'username':user}
        return render(request, 'viewprodcuts.html', context)
    if request.method == 'POST':
        # data = request.POST
        # print(data)
        pname = request.POST.get('prod', False)
        qty = request.POST.get('qty', False)
        user = ''
        with open("session.txt", "r") as file:
            for line in file:
                user = line.strip('\n')
        file.close()
        index = 0
        record = ''
        readDetails("addproduct")
        rows = details.split("\n")
        tot_qty = 0
        for i in range(len(rows)-1):
            arr = rows[i].split("#")
            if arr[0] == "addproduct":
                if arr[1] == user and arr[2] == pname:
                    tot_qty = int(arr[4])
                    tot_qty = tot_qty + int(qty)
                    index = i
                    record = arr[0]+"#"+arr[1]+"#"+arr[2]+"#"+arr[3]+"#"+str(tot_qty)+"#"+arr[5]+"#"+arr[6]+"\n"
                    break
        for i in range(len(rows)-1):
            if i != index:
                record += rows[i]+"\n"
        updateQuantityBlock(record)
        messages.success(request,"sucessfully updated quantity")
        context= {'username':user}
        return render(request, 'viewprodcuts.html', context)

