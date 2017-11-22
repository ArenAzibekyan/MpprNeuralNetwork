from django.conf.urls import url
from .views import recognizePhoto


app_name = 'api'

urlpatterns = [
    url(r'^recognizePhoto', recognizePhoto, name='recognizePhoto')
]