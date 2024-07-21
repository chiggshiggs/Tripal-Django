from django.urls import path
from . import views

urlpatterns = [
    path('', views.trips, name="trips"),
    path('username=<str:username>/', views.trips_by_user, name="trips_by_user"),
    path('<int:trip_id>/', views.trips_details, name="trip_details"),
    path('requestsmad/<int:trip_id>',
         views.requests_made_to_trip, name="requestsmade"),
    path('allrequests', views.get_requests_by_user, name="getrequests"),
    path('search/', views.search, name="trip_search"),
    path('accept_request/<int:request_id>/',
         views.accept_request, name='accept_request'),
    path('reject_request/<int:request_id>/',
         views.reject_request, name='reject_request'),
    path('request/<int:trip_id>', views.request_a_trip, name='request'),
    path('change_admin/<int:trip_id>', views.change_admin, name='change_admin'),
    path('delete_trip/<int:trip_id>', views.delete_trip, name='delete_trip'),
    path('remove_participant/<int:trip_id>',
         views.remove_participant, name='remove_participant')
]
