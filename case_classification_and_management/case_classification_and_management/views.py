from django.shortcuts import render, redirect
from django.views.decorators.cache import never_cache
from django.contrib.auth import authenticate, logout, login as auth_login
from django.contrib.auth.models import User
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

@never_cache
def home(request):
    return render(request, "default/index.html", {"active": True})

@never_cache
def login(request):
    if request.method == 'POST':
        user = authenticate(request, username=request.POST.get("username"), password=request.POST.get("password"))

        if user is not None:
            auth_login(request, user)  

            if user.is_staff: 
                return redirect("lawyer_home")
            
            return redirect("client_home")
        
        else:
            return render(request, 'default/login.html', {'error_message': True, "l_active": True})

    return render(request, "default/login.html", {"l_active": True})

@never_cache
def logout_default(request):
    logout(request)
    return redirect('home')


def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        choose = request.POST.get("lawyer_or_client", "Client")
        case_value = request.POST.get("case_values")
        print("case:", case_value)

        if User.objects.filter(username=username).exists():
            return render(request, "default/register.html", {"r_active": True, "court_cases": court_case_classifications, "error_message": True})

        user = User.objects.create_user(username=username, password=password)

        if choose == "Lawyer":
            user.is_staff = True
            user.save()
            case = CaseType.objects.create(case=case_value, lawyer=user)
            authenticated_user = authenticate(request, username=username, password=password) 
            auth_login(request, authenticated_user)  
            return redirect("lawyer_home")
        else:
            authenticated_user = authenticate(request, username=username, password=password) 
            auth_login(request, authenticated_user)  
            return redirect("client_home")

    return render(request, "default/register.html", {"r_active": True, "court_cases": court_case_classifications})