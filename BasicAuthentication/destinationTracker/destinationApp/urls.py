from django.urls import path
from django.http import HttpResponse
from . import views

urlpatterns = [
    path("", views.index, name="Home Page"),
    path("users/new/", views.createAccountPage, name="Create Account Page"),
    path("users/", views.createAccount, name="Create Account"),
    path("sessions/new/", views.signInPage, name="Sign In Page"),
    path("sessions/", views.signIn, name="Sign In"),
    path("sessions/destroy/", views.sessionDestroy, name="Destroy Session"),
    path("destinations/", views.destinations, name="Destinations Page"),
    path("destinations/new/", views.addDestination, name="Add Destinations Page"),
    path("destinations/<int:id>/", views.editDestination, name="Edit Destinations Page"),
    path("destinations/<int:id>/destroy/", views.destroyDestination, name="Destroy Destination"),

]
