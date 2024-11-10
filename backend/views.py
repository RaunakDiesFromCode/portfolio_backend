import os
from django.conf import settings
from django.shortcuts import redirect, render
import requests
from .models import *
from rest_framework import generics
from .models import *
from .serializers import reviewFormSerializer
import random
from django.core.mail import send_mail
from django.http import HttpResponse
from django.template.loader import render_to_string


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


def getReposData(request):

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
            randomData = random.sample(data, 3)
            return render(request, 'githubtest.html', {'data': randomData})
        else:
            print(f"GitHub API Error: {response.status_code} - {response.text}")
            return render(request, 'githubtest.html', {'data': None})

    except requests.exceptions.RequestException as e:
        print(f"Request Error: {e}")
        return render(request, 'githubtest.html', {'data': None})


def getRepos():

    token = os.getenv('GITHUB_BEARER_TOKEN')
    if not token:
        print("Error: GitHub token is not configured.")

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
            randomData = random.sample(data, 3)
            return randomData
        else:
            print(f"GitHub API Error: { response.status_code} - {response.text}")

    except requests.exceptions.RequestException as e:
        print(f"Request Error: {e}")

    return None


def send_email(request):

    repoDatas = getRepos()

    html_url = 'mailbody.html'

    # Replace with the recipient's email
    # recipient_email = [["raunakmanna43@gmail.com", "tautiksinharoy05@gmail.com"]]

    recipient_data = reviewForm.objects.all()

    try:
        # Log current settings for verification
        print(f"EMAIL_HOST: {settings.EMAIL_HOST}")
        print(f"EMAIL_PORT: {settings.EMAIL_PORT}")
        print(f"EMAIL_USE_TLS: {settings.EMAIL_USE_TLS}")
        print(f"EMAIL_USE_SSL: {settings.EMAIL_USE_SSL}")

        # Send the email

        for people in recipient_data:

            subject = "Hello from Django!"

            name = people.name

            message = render_to_string(html_url, {
                'name': name,
                'repoDatas': repoDatas,
            })

            send_mail(
                subject=subject,
                message='',
                html_message=message,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[people.email],
                fail_silently=False,
            )
        return HttpResponse(f"Email sent successfully to: {', '.join([recipient_data.email for recipient_data in recipient_data])}")

    except Exception as e:
        print(f"Error: {e}")  # Log error to console
        return HttpResponse(f"An error occurred: {e}", status=500)


def mail_body(request):
    repoDatas = getRepos()
    name = request.GET.get('name', 'Raunak')
    return render(request, 'mailbody.html', {'repoDatas': repoDatas, 'name': name})
