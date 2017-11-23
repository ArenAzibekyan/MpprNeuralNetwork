from django.http import JsonResponse
from PIL import Image
import io


#Function to convert image to array or list
def imageToCsv(file):
    img = file.read()
    img = Image.open(io.BytesIO(img))
    rawPixels = list(img.getdata())
    pixels = [1 if (sum(rgb[:3]) / 3) > 127 else 0 for rgb in rawPixels]
    return pixels



# Create your views here.
def recognizePhoto(request):
    if request.method == 'POST':
        if 'myFile' in request.FILES:
            file = request.FILES['myFile']
            type = file.name.split('.')[-1]
            if type == 'png':
                l = imageToCsv(file)
                print(l)
                return JsonResponse({'ok': True})
            return JsonResponse({'ok': False,
                                 'error': 'type must be png'})
        return JsonResponse({'ok': False,
                             'error': 'file must be selected'})
    return JsonResponse({'ok': False,
                         'error': 'send method must be POST'})


def learnDigit(request):
    if request.method == 'POST':
        data = request.POST
        print(data)
        file = request.FILES
        return JsonResponse({'ok': True})
    return JsonResponse({'ok': False,
                         'error': 'send method must be POST'})


def learnMnist(request):
    return JsonResponse({'mnist': 'epta'})