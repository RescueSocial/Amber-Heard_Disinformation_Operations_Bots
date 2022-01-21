from django.urls import path
from .views import NlutextView

urlpatterns = [
    path('', NlutextView.as_view()),
]
