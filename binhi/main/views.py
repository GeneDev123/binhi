import json
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.conf import settings
import pandas as pd
import numpy as np

from .forms import CustomUserCreationForm, UserUpdateForm
from .models import CustomUser

from . import ai

def landing_page(request):
  context = {}
  return render(request, 'main/landing-page.html', context)

def user_login_and_register(request, login_or_register_param):
  if request.user.is_authenticated:
    return redirect('home')
  
  if request.method == 'POST':
    print(login_or_register_param)
    if login_or_register_param == 'login':
      form = AuthenticationForm(request, request.POST)
      if form.is_valid():
        user = form.get_user()
        login(request, user)
        return redirect('home')
    elif login_or_register_param == 'register':  
      form = CustomUserCreationForm(request.POST)
      if form.is_valid():
        user = form.save()
        login(request, user)
        return redirect('home')
  else:
    form = CustomUserCreationForm if login_or_register_param == 'register' else AuthenticationForm()

  return render(request, 'main/login-register.html', {'form': form, 'login_or_register': login_or_register_param})

def user_logout(request):
  logout(request)
  return redirect('home') 

@login_required(login_url='/accounts/login/') 
def home(request):
  base_dir = settings.BASE_DIR
  context = {}
  classify_output = "Analyze the Return on Investment (ROI) for a harvested crop in a specific month by leveraging a machine learning model trained on historical data. Classify whether the anticipated ROI is positive or negative based on the insights derived from the aforementioned model."

  with open( str(base_dir) + '/main/dataset/json/dataset.json', 'r') as file:
    data = json.load(file)
    dataset = data["dataset"]
  
  model_output = {}
  progress_output = ''

  # for classifier v2
  selected_crop = ''
  investment = ''
  selected_date = ''
  predicted_roi = ''
  total_return = ''
  model_score = ''
  terminal_progress = ''
  profit = [None]
  revenue = ''
  conclusion_output = ''

  if request.method == 'GET':
    
    form_name = request.GET.get('form_name')
    if form_name == 'roi-classify-form':

      print("ROI Predictor V1")
      selected_month = request.GET.get('selectedMonth')
      selected_crop = request.GET.get('selectedCrop')

      if selected_crop != None and selected_month != None:  
        classify_output, progress_output  = ai.classify({
          'month': selected_month,
          'crop': selected_crop,
        })

        print(classify_output)

    elif form_name == 'roi-classify-form-2':
      print("ROI Predictor V2")

      selected_crop = request.GET.get('selectedCrop')
      investment = request.GET.get('investment-php')
      selected_date = request.GET.get('selectedDate')
      year, month, day = selected_date.split('-')

      predicted_roi, total_return, model_score, terminal_progress, conclusion_output = ai.classify2(investment, month, year, selected_crop)
      predicted_roi = np.round(predicted_roi, 2)
      profit = np.round(total_return, 2)
      revenue = round(float(profit) + float(investment), 2)
     

  context = {
    'dataset': dataset,
    'model_output': model_output,
    'classify_output': classify_output,
    'progress_output': progress_output,

    # This is for classifier v2
    'selected_crop': selected_crop,
    'selected_date': selected_date,
    'investment': investment,
    'roi': predicted_roi,
    'profit': profit[0],
    'revenue': revenue,
    'model_score': model_score,
    'terminal_progress': terminal_progress,
    'conclusion_output': conclusion_output
  }
  return render(request, 'main/home.html', context)

def train_ai(request):
  base_dir = settings.BASE_DIR
  context = {}

  with open( str(base_dir) + '/main/dataset/json/dataset.json', 'r') as file:
    data = json.load(file)
    dataset = data["dataset"]

  try:
    model_output = ai.train_classifier(dataset)
    context = {'model_output': model_output, 'classify_output': "Training Complete."}  

  except:
    context = {}

  return JsonResponse(context, safe=False)

def train_ai_2(request):
  base_dir = settings.BASE_DIR
  context = {}

  data = pd.read_csv(str(base_dir) + "/main/dataset/csv/farm-gate-prices.csv")
  dataset = ai.get_dataset_linear_regression(data)
  
  try: 
    models, scores = ai.train_classifier2(dataset)
    context = {'model_output': scores, 'classify_output': "Training Complete."}  

  except:
    context = {}

  return JsonResponse(context, safe=False)
  
@login_required(login_url='/accounts/login/') 
def vegetable_recommendations(request):
  return render(request, 'main/vegetable_recommendations.html')

@login_required(login_url='/accounts/login/') 
def cultural_management_practices(request):
  return render(request, 'main/cultural_management_practices.html')

@login_required(login_url='/accounts/login/') 
def nutrient_management(request):
  return render(request, 'main/nutrient_management.html')

@login_required(login_url='/accounts/login/') 
def roi_analysis(request):
  return render(request, 'main/roi_analysis.html')