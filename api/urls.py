from django.conf.urls import url
from .views import recognizePhoto, learnDigit, learnMnist, teach


app_name = 'api'

urlpatterns = [
    url(r'^recognizePhoto', recognizePhoto, name='recognizePhoto'),
    url(r'^learnDigit', learnDigit, name='learnDigit'),
    url(r'^learnMnist', learnMnist, name='learnMnist'),
    url(r'^teach', teach, name='teach')
]