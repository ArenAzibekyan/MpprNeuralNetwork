from django.http import JsonResponse
from django import forms
# нейронка
from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation
from keras.optimizers import RMSprop
from keras.datasets import mnist
from keras.utils import np_utils
import tensorflow as tf
# конвертация фотки
import io
from PIL import Image
import numpy as np


#
# модель нейросети
model = None
graph = None
weight = None


# распознать фотку
# форма
class recognizeDigitForm(forms.Form):
    digitPhoto = forms.ImageField()
# вьюха
def recognizeDigit(request):
    if request.method == 'POST':
        form = recognizeDigitForm(request.POST, request.FILES)
        if form.is_valid():
            global model, graph
            if model:
                X_recognize = imgToArray(request.FILES['digitPhoto'].read())
                X_recognize = X_recognize.reshape(1, 70)
                with graph.as_default():
                    Y_recognize = model.predict(X_recognize, batch_size=128, verbose=0)
                    return JsonResponse({'ok': True,
                                         'values': Y_recognize.tolist()})
            return JsonResponse({'ok': False,
                                 'error': 'neural network model isn\'t created'})
        return JsonResponse({'ok': False,
                             'error': 'form data validation error'})
    return JsonResponse({'ok': False,
                         'error': 'send method must be POST'})


# обучить одну цифру
# форма
class learnDigitForm(forms.Form):
    digitPhoto = forms.ImageField()
    value = forms.CharField()
    epochCount = forms.CharField()
# вьюха
def learnDigit(request):
    if request.method == 'POST':
        form = learnDigitForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                value = int(request.POST['value'])
                epochCount = int(request.POST['epochCount'])
            except:
                return JsonResponse({'ok': False,
                                     'error': 'form data validation error'})
            else:
                global model, graph, weight
                if not model:
                    graph = tf.get_default_graph()
                    model = createModel()
                    weight = model.get_weights()
                with graph.as_default():
                    X_train = imgToArray(request.FILES['digitPhoto'].read())
                    X_train = X_train.reshape(1, 70)
                    Y_train = [0] * 10
                    Y_train[value] = 1
                    Y_train = np.array(Y_train)
                    Y_train = Y_train.reshape(1, 10)
                    print(X_train.shape[0], 'train sample')
                    # обучение
                    model.fit(X_train, Y_train,
                              batch_size=128, epochs=epochCount,
                              verbose=2)
                return JsonResponse({'ok': True})
        return JsonResponse({'ok': False,
                             'error': 'form data validation error'})
    return JsonResponse({'ok': False,
                         'error': 'send method must be POST'})


#
# обучить всю базу мнист
def learnMnist(request):
    # только get-запрос
    if request.method == 'GET':
        # требуемое имя параметра
        if 'epochCount' in request.GET:
            epochCount = request.GET['epochCount']
            # требуемый тип
            try:
                epochCount = int(epochCount)
            except:
                return JsonResponse({'ok': False,
                                     'error': 'GET params validation error'})
            else:
                global model, graph, weight
                if not model:
                    graph = tf.get_default_graph()
                    model = createModel()
                    weight = model.get_weights()
                with graph.as_default():
                    # заготовленная база мниста
                    (X_train, y_train), (X_test, y_test) = mnist.load_data()
                    # удаление лишнего с фоток
                    print('cropping mnist digits')
                    X_train = np.array([mnistDigitCrop(mnistDigit) for mnistDigit in X_train])
                    X_test = np.array([mnistDigitCrop(mnistDigit) for mnistDigit in X_test])
                    # требуемый формат
                    X_train = X_train.reshape(60000, 70)
                    X_test = X_test.reshape(10000, 70)
                    # вывод размерности перед обучением
                    print(X_train.shape[0], 'train samples')
                    print(X_test.shape[0], 'test samples')
                    # 10 классов на выход
                    Y_train = np_utils.to_categorical(y_train, 10)
                    Y_test = np_utils.to_categorical(y_test, 10)
                    # обучение
                    model.fit(X_train, Y_train,
                              batch_size=128, epochs=epochCount,
                              verbose=2,
                              validation_data=(X_test, Y_test))
                return JsonResponse({'ok': True})
        return JsonResponse({'ok': False,
                             'error': 'GET params validation error'})
    return JsonResponse({'ok': False,
                         'error': 'send method must be GET'})


#
# сбросить состояние обучения
def resetTrain(request):
    if request.method == 'GET':
        global model, graph, weight
        if model:
            print('Reset train -> setting initial weights')
            with graph.as_default():
                model.set_weights(weight)
            return JsonResponse({'ok': True})
        return JsonResponse({'ok': False,
                             'error': 'neural network model isn\'t created'})
    return JsonResponse({'ok': False,
                         'error': 'send method must be GET'})


#
# создать модель нейросети
def createModel():
    np.random.seed(1337)
    # создание модели
    model = Sequential()
    # 70 на вход
    model.add(Dense(40, input_shape=(70,)))
    model.add(Activation('relu'))
    model.add(Dropout(0.2))
    # 40 скрытый
    model.add(Dense(40))
    model.add(Activation('relu'))
    model.add(Dropout(0.2))
    # 10 на выход
    model.add(Dense(10))
    model.add(Activation('softmax'))
    # Use rmsprop to do the gradient descent see http://www.cs.toronto.edu/~tijmen/csc321/slides/lecture_slides_lec6.pdf
    # and http://cs231n.github.io/neural-networks-3/#ada
    rms = RMSprop()
    # The function to optimize is the cross entropy between the true label and the output (softmax) of the model
    model.compile(loss='categorical_crossentropy', optimizer=rms, metrics=["accuracy"])
    return model


#
# получить numpy массив на 784 элемента из фотки
def imgToArray(bin):
    img = Image.open(io.BytesIO(bin))
    img = img.crop(img.getbbox())
    img = img.resize((7, 10), Image.ANTIALIAS)
    alphas = [(t[3] / 255) for t in img.getdata()]
    array = np.array(alphas, np.float32)
    return array


#
# обрезать лишнее и кропнуть с разрешением 7 на 10
def mnistDigitCrop(mnistDigit):
    data = [(0, 0, 0, alpha) for row in mnistDigit.tolist() for alpha in row]
    img = Image.new('RGBA', (28, 28))
    img.putdata(data)
    img = img.crop(img.getbbox())
    img = img.resize((7, 10), Image.ANTIALIAS)
    alphas = [(t[3] / 255) for t in img.getdata()]
    array = np.array(alphas, np.float32)
    return array