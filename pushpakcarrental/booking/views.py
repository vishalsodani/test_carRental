from django.shortcuts import redirect, render
from feedback.views import *
from accident.views import *
from transaction.views import *
import datetime
from .models import *
from django.contrib import messages
# Create your views here.
def fareEstimator(request):
    return render(request, 'fare_estimator.html')

def editBooking(request):
    if request.method == 'POST':
        booking_id = request.POST['id']
        booking = Book_Car.objects.filter(id=booking_id).first()
        from_date = booking.from_date
        to_date = booking.to_date
        return render(request, 'editbooking.html',{
            'id':booking.id,
            'capacity':booking.capacity,
            'from_date':from_date.strftime("%Y-%m-%d"),
            'to_date':to_date.strftime("%Y-%m-%d"),
            'from_time':from_date.strftime("%H:%M"),
            'to_time':to_date.strftime("%H:%M"),
            'subscription':booking.subscription,
            })
    pass

def updateBooking(request):
    if request.method == 'POST':
        booking_id = request.POST['id']
        capacity = request.POST['capacity']
        from_date = datetime.datetime.strptime(request.POST['from_date']+ ' ' + request.POST['from_time'], '%Y-%m-%d %H:%M')
        to_date = datetime.datetime.strptime(request.POST['to_date'] + ' ' + request.POST['to_time'], '%Y-%m-%d %H:%M')
        difference = to_date-from_date
        c = round(float(round(difference.total_seconds() / (3600), 2)) * 1 * float(capacity),2)
        book_car = Book_Car.objects.filter(id=booking_id).update(capacity=capacity,from_date=from_date,to_date=to_date,rent=c,is_paid=False, confirmation=False)
        # book_car.save()
        success = "Your booking is being processed and the bill for your booking is $"+str(c)
        return render(request, 'bookcar.html',{'success':success})  

    return render(request, 'bookcar.html') 

def deleteBooking(request):
    if request.method == 'POST':
        booking_id = request.POST['id']
        booking = Book_Car.objects.filter(id=booking_id)
        booking.delete()
        return redirect(bookings)
    return redirect(booking)

def cancelBooking(request):
    pass

def retrieveBooking(request):
    pass

def rescheduleBooking(request):
    pass

@login_required
def bookCar(request):
    if request.method == 'POST':
        capacity = request.POST['capacity']
        from_date = datetime.datetime.strptime(request.POST['from_date']+ ' ' + request.POST['from_time'], '%Y-%m-%d %H:%M')
        to_date = datetime.datetime.strptime(request.POST['to_date'] + ' ' + request.POST['to_time'], '%Y-%m-%d %H:%M')
        difference = to_date-from_date
        c = round(float(round(difference.total_seconds() / (3600), 2)) * 1 * float(capacity),2)
        subscription = request.POST['subscription']
        book_car = Book_Car(user=request.user, capacity=capacity,from_date=from_date,to_date=to_date,rent=c,is_paid=False, confirmation=False, subscription=subscription)
        
        book_car.save()
        success = "Your booking is being processed and the bill for your booking is $"+str(c)
        return render(request, 'bookcar.html',{'success':success})  

    return render(request, 'bookcar.html')  

def finalizeCar(request):
    bookings = Book_Car.objects.all()
    return render(request, 'finalizebooking.html',{'bookings':bookings})

def finalizeCarBooking(request):
    if request.method == 'POST':
        booking_id = request.POST['id']
        booking = Book_Car.objects.filter(id=booking_id).first()
        cars = Cars.objects.filter(capacity=booking.capacity)
        for car in cars:
            # check for dates
            a = car.booked_from
            b = car.booked_to
            c = booking.from_date
            d = booking.to_date
            if a is None and b is None:
                car.booked_from = c
                car.booked_to = d
                car.is_available = False
                mybooking = Cars.objects.filter(id=car.id).update(booked_from=c,booked_to=d)
                if mybooking is True:
                    messages.success(request, "Booking is successful")
                    return redirect(finalizeCarBooking)
            elif a<=c<=b is False and a<=d<=b is False:
                car.booked_from = c
                car.booked_to = d
                car.is_available = False
                mybooking = Cars.objects.filter(id=car.id).update(booked_from=c,booked_to=d)
                if mybooking is True:
                    messages.success(request, "Booking is successful")
                    return redirect(finalizeCarBooking)
            else:
                messages.error(request, "No car available in this duration")
                return redirect(finalizeCar)                 
            
    bookings = Book_Car.objects.all()
    return render(request, 'finalizebooking.html',{'bookings':bookings})

def bookings(request):
    bookings = Book_Car.objects.all()
    return render(request, 'bookings.html',{'bookings':bookings})

def upgradeCar(request):
    pass
