from django.shortcuts import render
from .models import Status
from .forms import StatusCreationForm
from django.contrib.auth.decorators import login_required


# # Create your views here.
# @login_required
# def new_status(request):
#     # POST submits data to be processed (e.g., from an HTML form) to the identified resource.
#     # The data is included in the body of the request.
#     # This may result in the creation of a new resource or the updates of existing resources or both.
#     if request.method == 'POST':



