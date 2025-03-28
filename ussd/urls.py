from django.urls import path # type: ignore
from .views import ussd_view
app_name = "ussd"

# urlpatterns = [
#     path('ussd', index),
# ]

urlpatterns = [
    path('ussd/', ussd_view, name="ussd_view"),
]