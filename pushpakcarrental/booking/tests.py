import unittest
import datetime

from django.test import TestCase, Client
from django.contrib.auth.models import User
from owner.models import Cars, Coupons
from booking.models import Book_Car

class bookingTestCase(TestCase):
    
    def setUp(self):
        newUser = User.objects.create_user(username="robot", email="robot@gmail.com", password="pass")
        Book_Car.objects.create(user_id=newUser,capacity='5',from_date='2023-05-07',to_date='2023-05-08',rent='200',is_paid=True,confirmation=1)
    
    def test_bookCar(self):
        print(self._testMethodName)
        newUser = User.objects.create_user(username="mailed", email="mailed@gmail.com", password="letter")
        Book_Car.objects.create(user_id=newUser,capacity='5',from_date='2023-05-07',to_date='2023-05-08',rent='200',is_paid=True,confirmation=1)
        booked_car=Book_Car.objects.get(user_id=newUser.id)
        self.assertEqual(booked_car.capacity,"5")

    def test_bookCar_toDate(self):
        print(self._testMethodName)
        newUser = User.objects.create_user(username="mailed", email="mailed@gmail.com", password="letter")
        Book_Car.objects.create(user_id=newUser,capacity='5',from_date='2023-05-07',to_date='2023-05-08',rent='200',is_paid=True,confirmation=1)
        booked_car=Book_Car.objects.get(user_id=newUser.id)
        self.assertEqual(booked_car.rent,200)
        
class test_bookCar(TestCase):
    
    def test_bookCar(self):
        data= {
            "capacity":'5',
            "success":'success'
        }
        newUser = User.objects.create_user(username="mailed", email="mailed@gmail.com", password="letter")
        from_date = datetime.datetime.strptime('2023-05-07'+ ' ' +'00:00', '%Y-%m-%d %H:%M')
        to_date = datetime.datetime.strptime('2023-05-08' + ' ' + '00:00', '%Y-%m-%d %H:%M')
        difference = to_date-from_date
        c = round(float(round(difference.total_seconds() / (3600), 2)) * 1 * float(5),2)
        book_car = Book_Car(user_id=newUser, capacity=5,from_date=from_date,to_date=to_date,rent=c,is_paid=False, confirmation=False)
        book_car.save()
        
        response=self.client.post("/bookcar/",data=data)
        self.assertEqual(book_car.rent,c)
        
    def test_editBooking(self):
        newUser = User.objects.create_user(username="mailed", email="mailed@gmail.com", password="letter")
        book_car = Book_Car(user_id=newUser, capacity=5,from_date=datetime.datetime(2023,7,8),to_date=datetime.datetime(2023,7,10),rent=200,is_paid=False, confirmation=False)
        book_car.save()
        data= {
            'booking':book_car,
            'id': newUser.id
        }
        response=self.client.post("/editbooking/",data=data)
        self.assertEqual(response.status_code,200)