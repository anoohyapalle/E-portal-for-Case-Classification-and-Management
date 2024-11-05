from fuzzywuzzy import process
import PyPDF2
from django.shortcuts import redirect, render
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from client.models import Booking
from lawyer.models import CaseType

court_case_classifications = [
    "Theft Incidents",
    "Lawbreaker Cases",
    "Violence Matters",
    "Assault Situations",
    "Substance Abuse Offenses",
    "Property Damage Cases",
    "Fraud Instances",
    "Disorderly Conduct Matters"
]


@login_required
@never_cache
def home(request):
    most_similar_case = False
    lawyers = False
    flag = False
    if request.method == "POST":
        pdf_file = request.FILES['pdf_file']
        pdf_text = extract_pdf_text(pdf_file)
        most_similar_case = find_most_similar_case(pdf_text)
        most_similar_case = most_similar_case[0]
        lawyers = CaseType.objects.filter(case=most_similar_case)
        if len(lawyers) == 0:
            flag = True

    return render(request, 'client/index.html', {"court_case_classifications": court_case_classifications, "most_similar_case": most_similar_case, "lawyers": lawyers, "flag": flag})

def extract_pdf_text(pdf_file):
    pdf_text = ""
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    for page_num in range(len(pdf_reader.pages)):
        pdf_text += pdf_reader.pages[page_num].extract_text()
    return pdf_text


def find_most_similar_case(pdf_text):
    similarity_scores = process.extractBests(pdf_text, court_case_classifications)
    most_similar_case, similarity_score = similarity_scores[0]
    return most_similar_case, similarity_score


@login_required
@never_cache
def book_now(request, id):
    if request.method == "POST":
        mobile_number = request.POST.get("mobile_number")
        lawyer = User.objects.get(id=id)
        
        booking = Booking.objects.create(
            lawyer=lawyer,
            client=request.user.username,
            phone_number=mobile_number
        )

    return redirect('client_home')