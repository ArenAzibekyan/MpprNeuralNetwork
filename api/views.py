from django.http import JsonResponse
from django import forms


# распознать фотку
# форма
class recognizeDigitForm(forms.Form):
    digitPhoto = forms.ImageField()
# вьюха
def recognizeDigit(request):
    if request.method == 'POST':
        form = recognizeDigitForm(request.POST, request.FILES)
        if form.is_valid():
            # нейронка
            return JsonResponse({'ok': True})
        return JsonResponse({'ok': False,
                             'error': 'form data validation error'})
    return JsonResponse({'ok': False,
                         'error': 'send method must be POST'})


# обучить одну цифру
# форма
class learnDigitForm(forms.Form):
    digitPhoto = forms.ImageField()
    value = forms.CharField()
# вьюха
def learnDigit(request):
    if request.method == 'POST':
        form = learnDigitForm(request.POST, request.FILES)
        if form.is_valid():
            # нейронка
            return JsonResponse({'ok': True})
        return JsonResponse({'ok': False,
                             'error': 'form data validation error'})
    return JsonResponse({'ok': False,
                         'error': 'send method must be POST'})


def learnMnist(request, epochCount):
    epochCount = int(epochCount)
    return JsonResponse({'count': epochCount})