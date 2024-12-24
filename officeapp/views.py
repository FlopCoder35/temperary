from django.shortcuts import render,HttpResponse,redirect
from .models import Member,Department,Role
from datetime import datetime
from django.db.models import Q
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login,logout
from django.conf import settings
# Create your views here.

def send_message(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        message = request.POST.get("message")

        # Validate the data (Optional)
        if not name or not email or not message:
            return HttpResponse("All fields are required.", status=400)

        # Send an email or process the data
        try:
            send_mail(
                subject=f"New Message from {name}",
                message=f"Name: {name}\nEmail: {email}\nPhone: {phone}\n\nMessage:\n{message}",
                from_email=email,  # Replace with your email
                recipient_list=[settings.EMAIL_HOST_USER],  # Replace with your email
            )
            return render(request, "thank_you.html", {"name": name})
        except Exception as e:
            return HttpResponse(f"Failed to send message: {str(e)}", status=500)
    return HttpResponse("Invalid request method.", status=405)
def index(request):
    return render(request,'index.html')

def all_member(request):
   mems=Member.objects.all()
   context={
      'mems':mems 
    }
  
   return render(request,'all_member.html',context)
@login_required(login_url='login')
def add_member(request):
    if request.method=='POST':
        firstname=request.POST['firstname']
        lastname=request.POST['lastname']
        dept=request.POST['dept']
        role=request.POST['role']
        salary=int(request.POST['salary'])
        bonus=int(request.POST['bonus'])
        phone=int(request.POST['phone'])
        newmem=Member(firstname=firstname,lastname=lastname,dept_id=dept,role_id=role,phone=phone,salary=salary,bonus=bonus,hire_date=datetime.now())
        newmem.save()
        return HttpResponse('Member Added Successfuly ')
    elif request.method=='GET':
        depts = Department.objects.all()
        roles = Role.objects.all()
        context={
         'depts':depts,
         'roles':roles
        }
        
        return render(request, 'add_member.html', context)
    else:
        return HttpResponse('An Exception Occured ')
@login_required(login_url='login')  
def remove_member(request ,mem_id=0):
    if mem_id:
        try:
            to_be_removed=Member.objects.get(id=mem_id)
            to_be_removed.delete()
            return HttpResponse('Member removed successfuly ')
        except:
            return HttpResponse('Enter a valid id ')    

    mems=Member.objects.all()
    context={
      'mems':mems 
    }
    return render(request,'remove_member.html',context)
def filter_member(request):
    if request.method=='POST':
        firstname=request.POST['firstname']
        lastname=request.POST['lastname']
        dept=request.POST['dept']
        role=request.POST['role']
        salary=request.POST['salary']
        mems=Member.objects.all()
        depts=Department.objects.all()
        roles=Role.objects.all()
        if firstname and firstname != '':
            mems = mems.filter(firstname=firstname)
        if lastname and lastname != '':
            mems = mems.filter(lastname=lastname)
        if dept and dept != '':
            mems = mems.filter(dept_id=dept)  # Assuming 'dept' is the ID of the department
        if role and role != '':
            mems = mems.filter(role_id=role)  # Assuming 'role' is the ID of the role
        if salary and salary != '':
            mems = mems.filter(salary=salary)

        context={
            'mems':mems,
            'depts':depts,
            'roles':roles
        }  
        return  render(request,'all_member.html',context)
    elif request.method=='GET':
          depts = Department.objects.all()
          roles = Role.objects.all()
          mems=Member.objects.all()
          context={
           'depts':depts,
            'roles':roles,
            'mems':mems
          }
        
          return render(request,'filter_member.html',context)
    else:
        return HttpResponse('Error')
    
def custom_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_superuser:
            login(request, user)
            return redirect('index')  # Redirect to any page
        else:
            return HttpResponse('Invalid credentials or not a superuser')
    return render(request, 'login.html')
def custom_logout(request):
    logout(request)
    return redirect('login') 