from django.shortcuts import redirect, render
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required

from client.models import Booking
from lawyer.models import CaseType

court_case_classifications = [
    "Lawbreaker Cases",
    "Violence Matters",
    "Theft Incidents",
    "Assault Situations",
    "Substance Abuse Offenses",
    "Property Damage Cases",
    "Fraud Instances",
    "Disorderly Conduct Matters"
]


@login_required
@never_cache
def home(request):
    if request.method == "POST":
        case_ob = CaseType()
        case_ob.case = request.POST.get("case")
        case_ob.lawyer = request.user
        case_ob.save()
    user_cases = CaseType.objects.filter(lawyer=request.user)
    bookings = Booking.objects.filter(lawyer=request.user)
    available_cases = [case for case in court_case_classifications if case not in user_cases.values_list('case', flat=True)]
    return render(request, 'lawyer/index.html', {"court_case_classifications": available_cases, "user_cases": user_cases, "bookings": bookings})


@login_required
@never_cache
def done_booking(request, id):
    booking = Booking.objects.get(id=id)
    booking.delete()
    return redirect("lawyer_home")


@login_required
@never_cache
def remove_case_type(request, id):
    case = CaseType.objects.get(id=id)
    case.delete()
    return redirect("lawyer_home")