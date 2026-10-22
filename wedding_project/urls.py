from django.urls import path
from wedding import views

urlpatterns = [
    path("", views.invitation, name="invitation"),
    path("rsvp/submit/", views.submit_rsvp, name="submit_rsvp"),
    # Enter this private path manually. Configure RSVP_VIEW_TOKEN in hosting env vars.
    path("private-rsvp/<str:token>/", views.private_rsvp_list, name="private_rsvp_list"),
]
