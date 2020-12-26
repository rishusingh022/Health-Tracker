from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from .models import *

# Create your views here.
from django.urls import reverse


def index(request):
    return render(request, "healthtracker/index.html")

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "healthtracker/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "healthtracker/login.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def checkhealth(request):
    if request.method == 'POST':
        regnumber = request.POST["regnumber"]
        try:
            patient = Patients.objects.get(RegNumber=regnumber)
        except Patients.DoesNotExist:
            patient = None
        if patient != None:
            data = PatientsStatus.objects.filter(Patient=patient).order_by('-Time')
        else:
            data = []
        return render(request, "healthtracker/patientprofile.html", {
            "data": data
        })
    else:
        return render(request, "healthtracker/chekhealth.html")



def addpatient(request):
    if request.method == 'POST':
        fname = request.POST['fname']
        lname = request.POST['lname']
        gender = request.POST['gender']
        roomnumber = request.POST['rnumber']
        state = request.POST['state']
        streeadd = request.POST['streetaddress']
        newpateints = Patients(
            FirstName=fname,
            LastName=lname,
            RoomNo=roomnumber,
            Gender=gender,
            Address=f"{streeadd}, {state}"
        )
        newpateints.save()
        print("new patient added")
        return render(request, "healthtracker/addpatient.html", {
            "message": "patient Added"
        })
    else:
        return render(request, "healthtracker/addpatient.html")


def addpateintdata(request):
    if request.method == 'POST':
        regnumber = request.POST['regnumber']
        pulserate = request.POST['pulserate']
        temperature = request.POST['temperature']
        patient = Patients.objects.get(RegNumber=regnumber)
        data = PatientsStatus(Patient=patient, PulseRate=pulserate, Temperature=temperature)
        data.save()
        print(f"Status Updated of {patient.FirstName}")
        return render(request, "healthtracker/adddata.html", {
            "message": f"Status updated!"
        })
    else:
        return render(request, "healthtracker/adddata.html")


def pateintsdataapi(request):
    if request.method == 'GET':
        patients = Patients.objects.all()
        return JsonResponse([patient.serialize() for patient in patients], safe=False)
    else:
        return JsonResponse({"message": "GET method required"})
