from django.urls import path, include
from . import views

urlpatterns = [
path('projects/digit_detector/', views.detect_numb_mainPage,name="digit_detector_Page"),
path('projects/digit_detector/output/', views.detect_numb_process,name="get_data")]
