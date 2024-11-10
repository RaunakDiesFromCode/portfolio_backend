from django.shortcuts import redirect, render
from .models import *
from rest_framework import generics
from .models import reviewForm
from .serializers import reviewFormSerializer
import requests
import os


class ReviewList(generics.ListAPIView):
    queryset = reviewForm.objects.all()
    serializer_class = reviewFormSerializer


# Create your views here.

def home(request):

    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        print(name, email, message)
        reviewForm.objects.create(name=name, email=email, message=message)
        return redirect('thankyou')

    return render(request, 'index.html')

def thankyou(request):

    return render(request, 'thankyou.html')


def getRepostData(request):
    import os
    import requests
    from django.shortcuts import render
    from django.http import JsonResponse

    token = os.getenv('GITHUB_BEARER_TOKEN')

    if not token:
        print("Error: GitHub token is not configured.")
        return render(request, 'thankyou.html', {'data': None})

    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github.v3+json"
    }

    try:
        response = requests.get(
            'https://api.github.com/user/repos?visibility=public', headers=headers)

        print(f"Status Code: {response.status_code}")
        print(f"Response Content: {response.content}")

        if response.status_code == 200:
            data = response.json()
            return render(request, 'githubtest.html', {'data': data})
        else:
            print(f"GitHub API Error: {
                  response.status_code} - {response.text}")
            return render(request, 'githubtest.html', {'data': None})

    except requests.exceptions.RequestException as e:
        print(f"Request Error: {e}")
        return render(request, 'githubtest.html', {'data': None})
