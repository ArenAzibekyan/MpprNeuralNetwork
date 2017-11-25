from django.conf.urls import url
from .views import learnDigit, learnMnist, recognizeDigit, resetTrain


app_name = 'api'

urlpatterns = [
    url(r'^recognizeDigit', recognizeDigit, name='recognizeDigit'),
    url(r'^learnDigit', learnDigit, name='learnDigit'),
    url(r'^learnMnist', learnMnist, name='learnMnist'),
    url(r'^resetTrain$', resetTrain, name='resetTrain')
]