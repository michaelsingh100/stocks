from django.urls import path

from . import views




def trigger_error(request):
    division_by_zero = 1 / 0

urlpatterns = [
    path('', views.index, name='index'),
    path('sentry-debug/', trigger_error)
]
