from django.shortcuts import render, redirect
from django.db import IntegrityError
from django.contrib.auth.hashers import make_password, check_password
from .models import User, Session, Destination
import uuid

def index(request):
    destinationsList = Destination.objects.filter(public=1)
    recentDestinations = max(len(destinationsList)-5, 0)
    destinations = destinationsList[recentDestinations:]
    return render(request, "destinationApp/homepage.html", {"destinations": destinations})

def createAccountPage(request):
    return render(request, "destinationApp/createAccount.html")

def createAccount(request):
    context = {}
    params = request.POST
    name = params.get("name")
    email = params.get("email")
    password = params.get("password")
    context['name'] = name
    context['email'] = email
    context['password'] = password
    if name == "" or email == "" or password == "":
        context['message'] = 'Please ensure that no fields are empty.'
        return render(request, "destinationApp/createAccount.html", context, status=400)
    elif not '@' in email:
        context['message'] = 'Please ensure that your email is valid.'
        return render(request, "destinationApp/createAccount.html", context, status=400)
    elif len(password) <= 7 or not (any(char in "0123456789" for char in password)):
        context['message'] = 'Please ensure that your password has at least 8 characters and 1 number in it.'
        return render(request, "destinationApp/createAccount.html", context, status=400)

    passwordHash = make_password(password)
    newUser = User(
        name=name.title(),
        email=email.lower(),
        passwordHash=passwordHash
    )
    try:
        newUser.save()
    except IntegrityError:
        context['message'] = 'This email is already asscociated with another account.'
        return render(request, "destinationApp/createAccount.html", context, status=400)
    response = redirect("/destinations")
    sessionToken = uuid.uuid4()
    response.set_cookie("sessionId", sessionToken)
    createSession(newUser.id, sessionToken)
    return response

def signInPage(request):
    return render(request, "destinationApp/signIn.html")

def signIn(request):
    context = {}
    params = request.POST
    email = params.get("email").lower()
    password = params.get("password")
    user = User.objects.filter(email=email).first()
    print(f"USER: {user}")
    if user is None:
        context['message'] = 'Either this email is not associated with an account, or the password is incorrect.'
        return render(request, "destinationApp/signIn.html", context, status=404)
    else:
        if not check_password(password, user.passwordHash):
            print(f"CHECK PASSWORD: {check_password(password, user.passwordHash)}")
            context['message'] = 'Either this email is not associated with an account, or the password is incorrect.'
            return render(request, "destinationApp/signIn.html", context, status=404)
        else:
            sessionToken = uuid.uuid4()
            createSession(user.id, sessionToken)
    response = redirect("/destinations")
    response.set_cookie("sessionId", sessionToken)
    return response


def destinations(request):
    context = {}
    if request.method == "GET":
        currUser = request.user.get("userObj")
        userDestinations = Destination.objects.filter(userId=currUser)
        return render(request, "destinationApp/destinations.html", {"destinations": userDestinations})
    else:
        params = request.POST
        destinationName = params.get("destinationName")
        review = params.get("review")
        rating = params.get("rating")
        public = 0 if params.get("public") is None else 1

        context['destinationName'] = destinationName
        context['review'] = review
        context['rating'] = rating
        context['public'] = 'yes' if public == 1 else None

        if destinationName == "" or review == "" or rating == "":
            context['message'] = 'Please ensure that no fields are empty.'
            return render(request, "destinationApp/newDestination.html", context, status=400)
        else:
            currUser = request.user.get("userObj")
            newDestination = Destination(
                name=destinationName,
                review=review,
                rating=int(rating),
                public=public,
                userId=currUser
            )
            newDestination.save()
        return redirect('/destinations')



def sessionDestroy(request):
    sessionToken = request.COOKIES.get('sessionId')
    print(sessionToken)
    Session.objects.get(token=sessionToken).delete()
    response = redirect("/")
    response.delete_cookie("sessionId")
    return response

def createSession(userId, sessionToken):
    newSession = Session(
        userId = userId,
        token = sessionToken
    )
    newSession.save()

def addDestination(request):
    return render(request, "destinationApp/newDestination.html")

def editDestination(request, id):
    context = {}
    destinationId = id
    currUser = request.user.get("userObj")
    destination = Destination.objects.filter(id=destinationId).first()
    if destination is None or destination.userId != currUser:
        context['message'] = 'Either this is not a valid destination or you do not own this destination'
        return render(request, "destinationApp/newDestination.html", context, status=404)
    else:
        if request.method == "GET":
            context['destinationName'] = destination.name
            context['review'] = destination.review
            context['rating'] = destination.rating
            context['public'] = 'yes' if destination.public == 1 else None
            context['link'] = f'/destinations/{id}/'
            print(context)
            return render(request, "destinationApp/newDestination.html", context)
        else:
            params = request.POST
            destinationName = params.get("destinationName")
            review = params.get("review")
            rating = params.get("rating")
            public = 0 if params.get("public") is None else 1

            context['destinationName'] = destinationName
            context['review'] = review
            context['rating'] = rating
            context['public'] = 'yes' if public == 1 else None

            if destinationName == "" or review == "" or rating == "":
                context['message'] = 'Please ensure that no fields are empty.'
                return render(request, "destinationApp/newDestination.html", context, status=400)
            else:
                destination.name = destinationName
                destination.review = review
                destination.rating = rating
                destination.public = public
                destination.save()
                return redirect('/destinations')

def destroyDestination(request, id):
    context = {}
    destinationId = id
    currUser = request.user.get("userObj")
    destination = Destination.objects.filter(id=destinationId).first()
    if destination is None or destination.userId != currUser:
        context['message'] = 'Either this is not a valid destination or you do not own this destination'
        return render(request, "destinationApp/newDestination.html", context, status=404)       
    else:
        destination.delete()
        return redirect('/destinations')

