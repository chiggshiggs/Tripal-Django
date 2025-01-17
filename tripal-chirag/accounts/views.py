from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from trips.models import Location, Transport, Participant, Request,Trip

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            messages.success(request, 'You are now logged in.')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid login credentials')
            return redirect('login')
    else:
        return render(request, 'accounts/login.html')

def register(request):
    if request.method == 'POST':
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists!')
                return redirect('register')
            elif not email.endswith("@itbhu.ac.in"):
                messages.error(request, 'User is not an IIT BHU student')
                return redirect('register')
            else:
                if User.objects.filter(email=email).exists():
                    messages.error(request, 'Email already in use!')
                    return redirect('register')
                else:
                    user = User.objects.create_user(first_name=firstname, last_name=lastname, email=email, username=username, password=password)
                    auth.login(request, user)
                    messages.success(request, 'You are now logged in.')
                    return redirect('dashboard')
                    # user.save()
                    # messages.success(request, 'You are registered successfully.')
                    # return redirect('login')
        else:
            messages.error(request, 'Passwords do not match')
            return redirect('register')
    else:
        return render(request, 'accounts/register.html')

@login_required(login_url = 'login')
def dashboard(request):
    locations = Location.objects.all()
    transports = Transport.objects.all()
    #requests - user can see his pending outgoing requests
    

    user = User.objects.get(id=request.user.id)
    trips = Trip.objects.all()
    
    journeys = Participant.objects.filter(user=user)
    upcoming_trips = [journey.trip for journey in journeys]
    data = {
        'locations': locations,
        'transports': transports,
        'upcoming_trips': upcoming_trips,
        'user': user,
        'trips': trips
    }
    return render(request, 'accounts/dashboard.html', data)

def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        return redirect('login')
    return redirect('login')
