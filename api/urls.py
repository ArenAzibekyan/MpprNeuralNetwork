from django.conf.urls import url
from .views import uploadPhoto


app_name = 'api'

urlpatterns = [
    url(r'^uploadPhoto', uploadPhoto, name='uploadPhoto')
]