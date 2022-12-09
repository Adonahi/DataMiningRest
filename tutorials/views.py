from django.shortcuts import render

from django.http.response import JsonResponse, HttpResponse
from rest_framework.parsers import JSONParser 
from rest_framework import status
 
from tutorials.models import Tutorial
from tutorials.serializers import TutorialSerializer
from rest_framework.decorators import api_view

import pandas as pd
import matplotlib.pyplot as plt 

# Create your views here.
@api_view(['GET', 'POST', 'DELETE'])
def tutorial_list(request):
    if request.method == 'GET':
        tutorials = Tutorial.objects.all()
        
        title = request.GET.get('title', None)
        if title is not None:
            tutorials = tutorials.filter(title__icontains=title)
        
        tutorials_serializer = TutorialSerializer(tutorials, many=True)
        return JsonResponse(tutorials_serializer.data, safe=False)
    elif request.method == 'POST':
        tutorial_data = JSONParser().parse(request)
        tutorial_serializer = TutorialSerializer(data=tutorial_data)
        if tutorial_serializer.is_valid():
            tutorial_serializer.save()
            return JsonResponse(tutorial_serializer.data, status=status.HTTP_201_CREATED) 
        return JsonResponse(tutorial_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
def analisis_list(request):
    if request.method == 'GET':
        tutorials = Tutorial.objects.all()
        
        title = request.GET.get('title', None)
        if title is not None:
            tutorials = tutorials.filter(title__icontains=title)
        
        tutorials_serializer = TutorialSerializer(tutorials, many=True)
        return JsonResponse(tutorials_serializer.data, safe=False)
    elif request.method == 'POST' and request.POST.get('vuelta') == '1':
        #data = request.POST
        df = pd.read_csv(request.FILES['file'].file)

        data = [
            str(df.to_html(classes="table table-hover table-dark table-responsive")),
            df.shape,
            str(df.dtypes),
            str(df.isnull().sum())
        ]
        return JsonResponse(data, safe=False)
    elif request.method == 'POST' and request.POST.get('vuelta') == '2':
        df = pd.read_csv(request.FILES['file'].file)
        df.hist(figsize=(14,14), xrot=45)
        response = HttpResponse(content_type="image/jpeg")
        plt.savefig(response, format="png")
        return response

