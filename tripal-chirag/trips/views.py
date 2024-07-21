from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import redirect, get_object_or_404, render
from .models import Location, Transport, Trip, Participant, Request
from django.utils import timezone

from datetime import datetime, date, time

# Create your views here.


@login_required(login_url='login')
def trips(request):
    if request.method == 'POST':
        start_location = request.POST['start']
        end_location = request.POST['end']
        transport_name = request.POST['transport']
        fare = request.POST['fare']
        curr_date = request.POST['date']
        curr_time = request.POST['time']
        curr_date = datetime.strptime(curr_date, '%Y-%m-%d').date()
        curr_time = datetime.strptime(curr_time, '%H:%M').time()

        print(start_location, end_location, transport_name, fare, curr_date, curr_time)

        user = User.objects.get(id=request.user.id)
        journeys = Participant.objects.filter(user=user)
        upcoming_trips = [journey.trip for journey in journeys]
        for trip in upcoming_trips:
            if not isinstance(curr_date, date):
                curr_date = datetime.strptime(curr_date, '%Y-%m-%d').date()
            if not isinstance(curr_time, time):
                curr_time = datetime.strptime(curr_time, '%H:%M').time()

            curr_trip_datetime = timezone.make_aware(
                datetime.combine(curr_date, curr_time))
            prev_trip_datetime = timezone.make_aware(
                datetime.combine(trip.date, trip.time))

            if curr_trip_datetime == prev_trip_datetime:
                messages.error(
                    request, 'Trip at the same time already exists!')
                return redirect('trip_search')

        # Get or create start location
        start, _ = Location.objects.get_or_create(name=start_location)

        # Get or create end location
        end, _ = Location.objects.get_or_create(name=end_location)

        # Get or create transport
        transport, _ = Transport.objects.get_or_create(name=transport_name)

        created_by = get_object_or_404(User, id=request.user.id)
        admin = created_by

        trip = Trip(
            start=start, end=end, transport=transport, created_by=created_by,
            fare=fare, date=curr_date, time=curr_time, admin=admin
        )
        trip.save()
        participant = Participant(trip=trip, user=created_by)
        participant.save()
        messages.success(request, 'Your trip has been created!')
        return redirect('dashboard')
    else:
        return redirect('trip_search')


@login_required(login_url='login')
def trips_details(request, trip_id):
    trip = get_object_or_404(Trip, id=trip_id)
    participants = Participant.objects.filter(trip=trip) if trip else []
    participant_names = [' '.join(
        [participant.user.first_name, participant.user.last_name]) for participant in participants]

    context = {
        'trip': trip,
        'participants': participant_names,
    }
    return render(request, 'trip/trip_detail.html', context)


@login_required(login_url='login')
def trips_by_user(request, username):
    user = get_object_or_404(User, username=username)
    trips = Trip.objects.filter(admin=user)
    context = {
        'user': user,
        'trips': trips,
    }
    return render(request, 'trip/trips_by_user.html', context)


@login_required(login_url='login')
def search(request):
    start = request.GET.get('start', '')
    end = request.GET.get('end', '')
    created_by = request.GET.get('created_by', '')
    date = request.GET.get('date', '')
    if start == '' and end == '' and created_by == '' and date == '':
        search_results = []
    else:
        filters = {}
        if start:
            filters['start__name__icontains'] = start
        if end:
            filters['end__name__icontains'] = end
        if created_by:
            filters['created_by__username__icontains'] = created_by
        if date:
            filters['date__icontains'] = date

        search_results = Trip.objects.filter(**filters)
        if len(search_results) == 0:
            messages.info(request, 'No such trips found!')

    locations = Location.objects.all()
    data = {'results': search_results, 'locations': locations}
    return render(request, 'trip/trip_search.html', data)


@login_required(login_url='login')
def requests_made_to_trip(request, trip_id):
    trip = get_object_or_404(Trip, id=trip_id)
    curr_user = User.objects.get(id=request.user.id)
    if trip.admin != curr_user and trip.created_by != curr_user:
        messages.error(request, 'Only admins and the trip creator can see requests made to a trip!')
        return redirect('dashboard')
    requests = Request.objects.filter(trip=trip)
    context = {
        'requests': requests
    }
    return render(request, 'requests/requests_on_trip.html', context)


@login_required(login_url='login')
def get_requests_by_user(request):
    user = User.objects.get(id=request.user.id)
    requests = Request.objects.filter(created_by=user)
    context = {
        'user': user,
        'requests': requests
    }
    return render(request, 'requests/requests_by_user.html', context)


@login_required(login_url='login')
def accept_request(request, request_id):
    req = Request.objects.get(pk=request_id)
    curr_user = User.objects.get(id=request.user.id)
    if curr_user == req.trip.admin or curr_user == req.trip.created_by:
        participant = Participant(trip=req.trip, user=req.created_by)
        participant.save()
        req.delete()
        return redirect('dashboard')
    else:
        messages.error('Only admins or creator can accept requests')
        return redirect('dashboard')


@login_required(login_url='login')
def reject_request(request, request_id):
    req = Request.objects.get(pk=request_id)
    curr_user = User.objects.get(id=request.user.id)
    if curr_user == req.trip.admin or curr_user == req.trip.created_by:
        req.delete()
        return redirect('trips_by_user')
    else:
        messages.error('Only admins or creator can accept requests')
        return redirect('dashboard')


@login_required(login_url='login')
def request_a_trip(request, trip_id):
    if request.method == 'POST':
        description = request.POST['description']

        trip = get_object_or_404(Trip, id=trip_id)
        curr_trip_datetime = timezone.make_aware(
            datetime.combine(trip.date, trip.time))
        user = User.objects.get(id=request.user.id)
        journeys = Participant.objects.filter(user=user)
        upcoming_trips = [journey.trip for journey in journeys]
        for tr in upcoming_trips:
            prev_trip_datetime = timezone.make_aware(
                datetime.combine(tr.date, tr.time))
            if curr_trip_datetime == prev_trip_datetime:
                print('match found! -- redirecting')
                messages.error(
                    request, 'Trip at the same time already exists!')
                return redirect('trip_search')
        req = Request(
            trip=trip, created_by=user, description=description
        )
        req.save()
        messages.success(request, 'your request has been made successfully')
        return redirect('getrequests')
    else:
        user = request.user
        context = {
            'user': user,
            'trip_id': trip_id
        }
        return render(request, 'requests/make_request.html', context)


@login_required(login_url='login')
def change_admin(request, trip_id):
    if request.method == 'POST':
        trip = get_object_or_404(Trip, id=trip_id)
        new = request.POST['new_admin']
        new_admin = get_object_or_404(User, username=new)

        if request.user == trip.admin:

            trip.assign_admin(new_admin)
            return redirect('dashboard')
    else:
        trip = get_object_or_404(Trip, id=trip_id)
        participant = Participant.objects.filter(trip=trip)
        participants = [person.user for person in participant]
        user = get_object_or_404(User, id=request.user.id)
        context = {
            'user': user,
            'participants': participants,
            'trip': trip
        }
        return render(request, 'admins/select_admin.html', context)


@login_required(login_url='login')
def delete_trip(request, trip_id):
    trip = get_object_or_404(Trip, id=trip_id)
    user = get_object_or_404(User, id=request.user.id)
    participant_count = Participant.objects.filter(trip=trip).count()

    if user == trip.admin and participant_count < 2:
        trip.delete()
        messages.success(request, "The trip has been deleted.")
    else:
        messages.error(
            request, 'There are other participants in the trip!')
    return redirect('dashboard')


@login_required(login_url='login')
def remove_participant(request, trip_id):
    if request.method == 'POST':
        trip = get_object_or_404(Trip, id=trip_id)
        new = request.POST['remove_part']

        to_delete = get_object_or_404(User, username=new)
        participant = participant = Participant.objects.filter(
            trip=trip, user=to_delete)

        if request.user == trip.admin:

            participant.delete()
            return redirect('dashboard')
    else:
        trip = get_object_or_404(Trip, id=trip_id)
        participant = Participant.objects.filter(trip=trip)
        participants = [person.user for person in participant]
        user = get_object_or_404(User, id=request.user.id)
        context = {
            'user': user,
            'participants': participants,
            'trip': trip
        }
        return render(request, 'admins/remove_participant.html', context)
