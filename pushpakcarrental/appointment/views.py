from django.shortcuts import render
from car.views import *
from sales.views import *
from .models import *
from django.contrib.auth.models import User, Group

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
def scheduleTestDrive(request):
    if request.method == 'POST':
        try:
            user_id = request.POST['id']
            appt_time = request.POST['appointment_time']
            appt_date = request.POST['appointment_date']

            # Statement checks if user id is present
            User.objects.filter(id=user_id)

            appointment = Appointment()
            appointment.user_id = user_id
            appointment.appt_time = appt_time
            appointment.appt_date = appt_date
            appointment.purpose = "test_drive"

            appointment.save()

            return redirect(list_users)
        except:
            # Error workflow
            return dashboard()


def scheduleAppointment(request):
    if request.method == 'POST':
        try:
            user_id = request.POST['id']
            appt_time = request.POST['appointment_time']
            appt_date = request.POST['appointment_date']

            # Statement checks if user id is present
            User.objects.filter(id=user_id)

            appointment = Appointment()
            appointment.user_id = user_id
            appointment.appt_time = appt_time
            appointment.appt_date = appt_date
            appointment.purpose = "appointment"

            appointment.save()

            return redirect(list_users)
        except:
            # Error workflow
            return dashboard()


def Appointment(request):
    if request.method == 'POST':
        user = request.user
        appointment = request.POST['appointment']
        date_scheduled = datetime.datetime.strptime(request.POST['appointment_date']+ ' ' + request.POST['appointment_time'], '%Y-%m-%d %H:%M')
        appointment = Appointment_data()
        appointment.user = user
        appointment.appointment = appointment
        appointment.date_scheduled = date_scheduled
        appointment.save()
        messages.success(request, 'Your appointment has been scheduled')
        return render(request, 'appointment.html')
    return render(request, 'appointment.html')