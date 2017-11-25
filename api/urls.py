from django.conf.urls import url
from . import views
# нейронка
from keras.datasets import mnist
from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation
from keras.optimizers import RMSprop
from keras.utils import np_utils


app_name = 'api'

urlpatterns = [
    url(r'^recognizeDigit', views.recognizeDigit, name='recognizeDigit'),
    url(r'^learnDigit', views.learnDigit, name='learnDigit'),
    url(r'^learnMnist\?epochCount=(?P<epochCount>[0-9]+)$', views.learnMnist, name='learnMnist')
]


# создать модель
def createModel():
    # создание модели
    model = Sequential()
    # добавление слоев
    model.add(Dense(512, input_shape=(784,)))
    model.add(Activation('relu'))
    model.add(Dropout(0.2))
    model.add(Dense(512))
    model.add(Activation('relu'))
    model.add(Dropout(0.2))
    model.add(Dense(10))
    model.add(Activation('softmax'))
    # Use rmsprop to do the gradient descent see http://www.cs.toronto.edu/~tijmen/csc321/slides/lecture_slides_lec6.pdf
    # and http://cs231n.github.io/neural-networks-3/#ada
    rms = RMSprop()
    # The function to optimize is the cross entropy between the true label and the output (softmax) of the model
    model.compile(loss='categorical_crossentropy', optimizer=rms, metrics=["accuracy"])
    return model


# создание модели при первичном запуске
neuralNetwork = createModel()







def niga():
    batch_size = 128  # Number of images used in each optimization step
    nb_classes = 10  # One class per digit
    nb_epoch = 1  # Number of times the whole data is used to learn

    (X_train, y_train), (X_test, y_test) = mnist.load_data()

    # Flatten the data, MLP doesn't use the 2D structure of the data. 784 = 28*28
    X_train = X_train.reshape(60000, 784)
    X_test = X_test.reshape(10000, 784)

    # Make the value floats in [0;1] instead of int in [0;255]
    X_train = X_train.astype('float32')
    X_test = X_test.astype('float32')
    X_train /= 255
    X_test /= 255

    # Display the shapes to check if everything's ok
    print(X_train.shape[0], 'train samples')
    print(X_test.shape[0], 'test samples')

    # convert class vectors to binary class matrices (ie one-hot vectors)
    Y_train = np_utils.to_categorical(y_train, nb_classes)
    Y_test = np_utils.to_categorical(y_test, nb_classes)

    # Define the model achitecture
    model = Sequential()
    model.add(Dense(512, input_shape=(784,)))
    model.add(Activation('relu'))
    model.add(Dropout(0.2))
    model.add(Dense(512))
    model.add(Activation('relu'))
    model.add(Dropout(0.2))
    model.add(Dense(10))
    model.add(Activation('softmax'))

    # Use rmsprop to do the gradient descent see http://www.cs.toronto.edu/~tijmen/csc321/slides/lecture_slides_lec6.pdf
    # and http://cs231n.github.io/neural-networks-3/#ada
    rms = RMSprop()
    # The function to optimize is the cross entropy between the true label and the output (softmax) of the model
    model.compile(loss='categorical_crossentropy', optimizer=rms, metrics=["accuracy"])

    # Make the model learn
    model.fit(X_train, Y_train,
              batch_size=batch_size, nb_epoch=nb_epoch,
              verbose=2)

    # Evaluate how the model does on the test set
    score = model.evaluate(X_test, Y_test, verbose=0)

    print('Test score:', score[0])
    print('Test accuracy:', score[1])

