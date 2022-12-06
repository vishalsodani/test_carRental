        
from django.contrib.auth.models import User
from django.test import TestCase, Client
from appointment.models import *


class appointmentTestCases(TestCase):

    def test_schedule_appointment(self):
        print(self._testMethodName)
        newUser = User.objects.create_user(username="driver", email="driver@gmail.com", password="drive")
        data={
            "id":newUser.id,
            'appointment_time':'05:07',
            "appointment_date":'2022-07-06'
            }
            
        User.objects.filter(id=newUser.id)
        appointment = Appointment_data()
        appointment.user_id = newUser.id
        appointment.appt_time = "05:07"
        appointment.appt_date = "2022-07-06"
        appointment.purpose = "appointment"
        appointment.save()

        self.client.login(username='driver', password='drive')
        data = {
            'username': "robot",
            'firstname': "machine",
            'lastname': "learning",
            'email': 'robot@gmail.com',
            'id': newUser.id,
            'appt_time': "12pm",
            'appt_date': "12-05-2022"
        }

        response = self.client.post('/scheduleappointment/', data=data)
        # Check that the response is 200 OK.
        self.assertEqual(Appointment_data.objects.get(user_id=), "appointment")

    def test_schedule_testdrive(self):
        print(self._testMethodName)
        newUser = User.objects.create_user(username="robot", email="robot@gmail.com", password="pass")
        newUser.first_name = "machine"
        newUser.last_name = "language"
        newUser.save()

        self.client.login(username='robot', password='pass')
        data = {
            'username': "robot",
            'firstname': "machine",
            'lastname': "learning",
            'email': 'robot@gmail.com',
            'id': newUser.id,
            'appt_time': "12pm",
            'appt_date': "12/05/2022"
        }

        response = self.client.post('/scheduleappointment/', data=data)
        self.assertEqual(Appointment_data.objects.filter(user_id=newUser.id).purpose, "appointment")

    def test_schedule_testdrive_date(self):
        print(self._testMethodName)
        newUser = User.objects.create_user(username="robot", email="robot@gmail.com", password="pass")
        newUser.first_name = "machine"
        newUser.last_name = "language"
        newUser.save()

        self.client.login(username='robot', password='pass')
        data = {
            'username': "robot",
            'firstname': "machine",
            'lastname': "learning",
            'email': 'robot@gmail.com',
            'id': newUser.id,
            'appt_time': "12pm",
            'appt_date': "12/05/2022"
        }

        response = self.client.post('/scheduletestdrive/', data=data)
        self.assertEqual(Appointment_data.objects.filter(user_id=newUser.id).appt_date, data["appt_date"])
