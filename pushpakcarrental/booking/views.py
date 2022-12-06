from django.shortcuts import redirect, render
from feedback.views import *
from accident.views import *
from transaction.views import *
import datetime
from .models import *
from django.contrib import messages
# Create your views here.
def fareEstimator(request):
    if request.method == 'POST':
        capacity = request.POST['capacity']
        from_date = datetime.datetime.strptime(request.POST['from_date']+ ' ' + request.POST['from_time'], '%Y-%m-%d %H:%M')
        to_date = datetime.datetime.strptime(request.POST['to_date'] + ' ' + request.POST['to_time'], '%Y-%m-%d %H:%M')
        difference = to_date-from_date
        c = round(float(round(difference.total_seconds() / (3600), 2)) * 1 * float(capacity),2)
        book_car = Book_Car(user_id=request.user, capacity=capacity,from_date=from_date,to_date=to_date,rent=c,is_paid=False, confirmation=False)
        success = "Your estimated fare is $"+str(c)
        return render(request, 'fare_estimator.html',{'success':success})  
    return render(request, 'fare_estimator.html')

def editBooking(request):
    if request.method == 'POST':
        booking_id = request.POST['id']
        booking = Book_Car.objects.filter(id=booking_id).first()
        return render(request, 'editbooking.html',{'booking':booking})
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
        Coupon=0
        check=1
        Coupon = request.POST['coupon']
        if(Coupon==''):
            Coupon=0
            check=0
        elif(Coupon!=''):
            Coupon=50
                
        from_date = datetime.datetime.strptime(request.POST['from_date']+ ' ' + request.POST['from_time'], '%Y-%m-%d %H:%M')
        to_date = datetime.datetime.strptime(request.POST['to_date'] + ' ' + request.POST['to_time'], '%Y-%m-%d %H:%M')
        difference = to_date-from_date
        c = round(float(round(difference.total_seconds() / (3600), 2)) * 1 * float(capacity),2)
        # book_car = Book_Car(user_id=request.user, capacity=capacity,from_date=from_date,to_date=to_date,rent=c,is_paid=False, confirmation=False)
        # book_car.save()
        if(Coupon!=0 and check==1):
            success = "Your booking is being processed and the bill for your booking after applying coupon is $"+str(c-float(Coupon))
            c=c-float(Coupon)
        else:
            success = "Your booking is being processed and the bill for your booking is $"+str(c)       
        #success = "Your booking is being processed and the bill for your booking is $"+str(c)
        book_car = Book_Car(user_id=request.user, capacity=capacity,from_date=from_date,to_date=to_date,rent=c,is_paid=False, confirmation=False)
        book_car.save()
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
