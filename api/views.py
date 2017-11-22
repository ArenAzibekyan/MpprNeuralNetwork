from django.http import JsonResponse


# Create your views here.
def recognizePhoto(request):
    if request.method == 'POST':
        if 'myFile' in request.FILES:
            file = request.FILES['myFile']
            type = file.name.split('.')[-1]
            if type == 'png':
                # нейронка здеся
                return JsonResponse({'ok': True})
            return JsonResponse({'ok': False,
                                 'error': 'type must be png'})
        return JsonResponse({'ok': False,
                             'error': 'file must be selected'})
    return JsonResponse({'ok': False,
                         'error': 'send method must be POST'})


def recordFile(file):
    with open('static/name.png', 'wb+') as dest:
        for chunk in file.chunks():
            dest.write(chunk)