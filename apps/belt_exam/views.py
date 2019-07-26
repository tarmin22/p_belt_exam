from django.shortcuts import render, HttpResponse,redirect
from apps.belt_exam.models import *
import bcrypt
from django.contrib import messages
from datetime import datetime
from dateutil.relativedelta import relativedelta

def index(request):
    return render(request,"belt_exam/index.html")

################################## Register #################################################

def register(request):
    print(request.POST)
    is_valid = True

    pw_hash = bcrypt.hashpw(request.POST['f_pw'].encode(), bcrypt.gensalt())
    print(pw_hash)
    request.session['first_name']= request.POST['f_name']
    request.session['last_name']= request.POST['l_name']
    request.session['email']= request.POST['femail']


    errors = User.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key,value in errors.items():
            messages.error(request,value)
        return redirect('/')
    else:
        new_user= User.objects.create(first_name= request.POST['f_name'],last_name=request.POST['l_name'],email=request.POST['femail'],password=pw_hash)
        messages.success(request,"You have successfully registered.")

        return redirect('/')

def login_user(request):
    errors = User.objects.user_validator(request.POST)
    if len(errors) > 0:
        for key,value in errors.items():
            messages.error(request,value)
        return redirect('/')
    else:
        current_user = User.objects.filter(email=request.POST['log_email'])
        print(current_user[0].email)
        request.session['first_name']=current_user[0].first_name
        request.session['user_id'] = current_user[0].id
        return redirect("/success")


    ###################### Success ##############################################

def success(request):
    if not 'user_id' in request.session:
        messages.error(request,"You are not logged in.")
        return redirect("/")
    else:
        # user = User.objects.get(id = request.session['user_id'])
        org = Org.objects.all()
        
        context ={
            "current_user" : User.objects.get(id = request.session['user_id']),
            "all_orgs" : org,
            # "my_trip":Trip.objects.filter(create_by = user)
            # "all_trips":Trip.objects.all()

        }
    return render(request,"belt_exam/add_org.html",context)


################################ Create a new organization ######################################
def create_org(request):

    valid =True
    if len(request.POST['name']) < 1:
        messages.error(request,"Need to enter an Org name")
        valid =False

    if len(request.POST['name']) < 6:
        messages.error(request,"Need to enter an Org name larger than 5 characters")
        valid =False
   
    if len(request.POST['desc']) < 11:
        messages.error(request,"Need to enter an Org description with 10 or more characters")
        valid =False

    if len(request.POST['desc']) < 1:
        messages.error(request,"Need to enter an Org description")
        valid =False


    if valid:   
        user = User.objects.get(id = request.session['user_id'])
        new_org = Org.objects.create(name = request.POST['name'], desc = request.POST['desc'], created_by =user)
        new_org.joined_by.add(user)
    

    return redirect("/success")


############################### org info ######################################################
def org_info(request, org_id):
    org=Org.objects.get(id=org_id)
    user = User.objects.get(id = request.session['user_id'])
    
    print(org.id)
    context = {
        "org": org,
        "user": user
    }
    return render(request,"belt_exam/org_info.html", context)

######################### join group #########################################
def join_org(request,org_id):
    user = User.objects.get(id = request.session['user_id'])
    org=Org.objects.get(id=org_id)
    org.joined_by.add(user)
    return redirect("/org_info/" + org_id)

######################### join group #########################################
def leave_org(request,org_id):
    user = User.objects.get(id = request.session['user_id'])
    org=Org.objects.get(id=org_id)
    org.joined_by.remove(user)
    return redirect("/org_info/" + org_id)


    #############################Log out ###################################
def logout(request):
    request.session.clear()
    return redirect("/")



###################################### Remove an org ###################################

def remove_org(request, org_id):
    org= Org.objects.get(id = org_id)
    org.delete()
    return redirect("/success")

