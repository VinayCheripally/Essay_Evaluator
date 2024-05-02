from django.shortcuts import render,redirect
from django.contrib.auth import get_user_model
from django.contrib.auth import logout,authenticate,login
from datetime import datetime 
from django.db import IntegrityError
from openai import OpenAI
User = get_user_model()
api_key = "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"
client = OpenAI(api_key=api_key)


def home(request):
    return render(request,"home.html")

def logout_view(request):
    logout(request)
    return redirect("/")

def login(request):
    if request.method=='POST':
        username = request.POST['username']
        password = request.POST['password']
        try:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                context = {'error': 'Invalid username or password'}
                return render(request, 'login.html', context)
        except Exception:
            return "helo"
    return render(request,'login.html')

def essayevaluator(request):
    if request.user.is_anonymous:
        return redirect("login")
    if  request.method == "POST":
        essay = request.POST['essay']
        title = request.POST['title']
        response_rating = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
        {
        "role": "system",
        "content": "Please rate the following essay out of 10, taking into account the following criteria: clarity of argument, organization, use of evidence, and grammar and spelling. Please provide a number from 1-10, with 10 being the highest possible score.Just give me the score , nothing more.Here is the title and content of the essay:"
        },
        {
        "role": "user",
        "content": f"Title:{title} , Content:{essay}"
        }
        ],
        max_tokens=1024,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
        )
        response_errors = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
        {
        "role": "system",
        "content": "Please provide me with the count of spelling errors in the essay. I will be looking for common errors such as 'teh' instead of 'the', 'recieve' instead of 'receive', and 'definately' instead of 'definitely'. Here is the essay. Just provide me the number of errors you find, nothing else."
        },
        {
        "role": "user",
        "content": essay
        }
        ],
        max_tokens=1024,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
        )
        response_yes_or_no = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
        {
        "role": "system",
        "content": "Please provide me with a yes or no answer to the following question: Does the content of the essay directly relate to the title provided? Ignore any tangential connections or loosely related ideas. Just provide a simple yes or no, nothing else. Here is the title and content:"
        },
        {
        "role": "user",
        "content": f"Title:{title} , Content:{essay}"
        }
        ],
        max_tokens=1024,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
        )
        context = {'rating': response_rating.choices[0].message.content,'count':response_errors.choices[0].message.content,'related':response_yes_or_no.choices[0].message.content}
        return render(request,"essay_evaluator.html",context)
    return render(request,"essay_evaluator.html")

def signup(request):
    if request.method=='POST':
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']
        first_name = request.POST['firstname'],
        last_name = request.POST['lastname']
        try:
            new_user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            is_staff = False,
            is_active = True,
            date_joined = datetime.now()
            )
        except IntegrityError:
            context = {'error': 'User with same username already exists so use a new username'}
            return render(request,"signup.html",context)
        new_user.save()
        return redirect('login')
    return render(request,"signup.html")