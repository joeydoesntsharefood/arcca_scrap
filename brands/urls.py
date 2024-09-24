from django.urls import path
from . import views

urlpatterns = [
	path('get-data', views.view, name='get_data'),
]
