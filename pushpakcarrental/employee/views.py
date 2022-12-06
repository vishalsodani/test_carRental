from django.shortcuts import render
from customer.views import digitalCheckin, referFriend
from feedback.models import Feedback
# Create your views here.
def assignCar(request):
    pass

def addDiscount(request):
    pass

def deleteDiscount(request):
    pass

def sfr(request):
    feedback = Feedback.objects.all()
    return render(request, 'sendfeedbackresponse.html', {'feedback':feedback})

def usfr(request):
    if request.method == 'POST':
        feedback = Feedback.objects.filter(id=request.POST['id']).update(feedback_text_response=request.POST['feedback_text_response'])
        success = 'Feedback response posted'
        feedback = Feedback.objects.all()
        return render(request, 'sendfeedbackresponse.html', {'feedback':feedback,'success':success})
    feedback = Feedback.objects.all()
    return render(request, 'sendfeedbackresponse.html', {'feedback':feedback})
def finalizeBooking(request):
    pass

def updateCarCondition(request):
    pass
