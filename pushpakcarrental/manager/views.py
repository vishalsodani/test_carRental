from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from employee.views import *
from django.contrib.auth.models import User, Group

from user.views import dashboard


@login_required
def list_users(request):
    users_list = []
    admin = User.objects.filter(is_superuser=True).first()
    users = User.objects.exclude(username=request.user).exclude(username=admin.username).all()

    for doser in users:
        l = list(doser.groups.values_list('name', flat=True))
        user_dictionary = {'username': doser.username, 'first_name': doser.first_name, 'last_name': doser.last_name,
                           'email': doser.email, 'is_staff': l, 'id': doser.id, 'is_active': doser.is_active}
        users_list.append(user_dictionary)

    request.session['users_list'] = users_list
    return render(request, 'list_users.html', {'users': users})


# Create your views here.
def addEmployee(request):
    if request.method == 'POST':
        try:
            user_id = request.POST['id']

            # Fetch user who needs to be made employee
            new_employee = User.objects.get(id=user_id)

            # Add user to the employee group
            employee_group = Group.objects.get(name='employee')
            employee_group.user_set.add(new_employee)

            return redirect(list_users)
        except:
            return dashboard()


def editEmployee(request):
    if request.method == 'POST':
        try:
            user_id = request.POST['id']
            username = request.POST['username']
            mobile = request.POST['mobile']
            firstname = request.POST['firstname']
            lastname = request.POST['lastname']
            email = request.POST['email']
            city = request.POST['city']
            city = city.lower()
            pincode = request.POST['pincode']

            employee = User.objects.get(id=user_id)

            employee.username = username
            employee.mobile = mobile
            employee.firstname = firstname
            employee.lastname = lastname
            employee.email = email
            employee.city = city
            employee.pincode = pincode

            employee.save()

            return redirect(list_users)
        except:
            # Error workflow
            return dashboard()


def deleteEmployee(request):
    if request.method == 'POST':
        user_id = request.POST['id']
        try:
            User.objects.get(id=user_id).delete()
            return redirect(list_users)
        except:
            return dashboard()


def editCarAvailability(request):
    pass


def deleteBooking(request):
    pass


def ApproveRefund(request):
    pass

@login_required
def blockUser(request):
    if request.method == 'POST':
        doser = User.objects.filter(id=request.POST['id']).first()
        if request.POST['ban']:
            mygroup = Group.objects.get(name='ban')
            mygroup.user_set.add(doser)
            mygroup = Group.objects.get(name='employee')
            mygroup.user_set.remove(doser)
            mygroup = Group.objects.get(name='manager')
            mygroup.user_set.remove(doser)
            mygroup = Group.objects.get(name='customer')
            mygroup.user_set.remove(doser)

    return redirect(list_users)


@login_required
def employee(request):
    if request.method == 'POST':
        doser = User.objects.filter(id=request.POST['id']).first()
        l = list(doser.groups.values_list('name', flat = True))
        if 'employee' in l:
            mygroup = Group.objects.get(name='employee')
            mygroup.user_set.remove(doser)
        elif request.POST['employee']:
            mygroup = Group.objects.get(name='employee')
            mygroup.user_set.add(doser)
            mygroup = Group.objects.get(name='ban')
            mygroup.user_set.remove(doser)

    return redirect(list_users)

@login_required
def customer(request):
    if request.method == 'POST':
        doser = User.objects.filter(id=request.POST['id']).first()
        # l = list(doser.groups.values_list('name', flat = True))
        # if 'customer' in l:
        #     mygroup = Group.objects.get(name='customer')
        #     mygroup.user_set.remove(doser)
        if request.POST['customer']:
            mygroup = Group.objects.get(name='customer')
            mygroup.user_set.add(doser)
            mygroup = Group.objects.get(name='ban')
            mygroup.user_set.remove(doser)

    return redirect(list_users)


@login_required
def manager(request):
    if request.method == 'POST':
        doser = User.objects.filter(id=request.POST['id']).first()
        l = list(doser.groups.values_list('name', flat = True))
        if 'manager' in l:
            mygroup = Group.objects.get(name='manager')
            mygroup.user_set.remove(doser)
        elif request.POST['manager']:
            mygroup = Group.objects.get(name='manager')
            mygroup.user_set.add(doser)
            mygroup = Group.objects.get(name='ban')
            mygroup.user_set.remove(doser)

    return redirect(list_users)