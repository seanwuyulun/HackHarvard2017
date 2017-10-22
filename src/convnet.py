import pandas as pd
from keras.models import Model, Sequential
from keras.layers import Input, Dense, TimeDistributed, LSTM, Dropout, Activation  
from keras.layers import Convolution2D, MaxPooling2D, Flatten
from keras.layers.normalization import BatchNormalization
from keras.layers.advanced_activations import ELU
from keras.callbacks import ModelCheckpoint
from keras import backend
from keras.utils import np_utils
from hackeras import dataset_shuffle, 


def process(filename):                                                                           
     f = open(filename,'r')
     data = []                                          
     for line in f.readlines():                              
         data.append(int(line[11:14]))
     return data

sd = process('saarthaktemp.txt')
ed = process('seantemp.txt')
dd = process('davidtemp.txt')
nd = process('noonetemp.txt')

dataset = {}
dataset[0]=[dd[i:i+200] for i in range(0,len(dd),200)]
dataset[1]=[sd[i:i+200] for i in range(0,len(sd),200)]
dataset[2]=[ed[i:i+200] for i in range(0,len(ed),200)]
dataset[3]=[nd[i:i+200] for i in range(0,len(nd),200)]

def one_hot(classid, classes):
    idx = classes.index(classid)
    vec = np.zeros(len(class_names))
    vec[idx] = 1
    return vec

data = dataset_shuffle(dataset, one_hot)

model = Sequential()
model.add(Convolution2D(32, 3, 3, input_shape=(1,data['train'][0].shape[0],data['train'][0].shape[1])))
model.add(BatchNormalization(axis=1, mode=2))
model.add(Activation('relu'))

for layer in range(6):
    model.add(Convolution2D(32,3,3))
    model.add(BatchNormalization(axis=1))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2,2)))
    model.add(Dropout(0.2))

model.add(Flatten())
model.add(Dense(128))
model.add(Activation('relu'))
model.add(Dropout(0.2))
model.add(Dense(classes.shape[0]))
model.add(Activation("softmax"))

model.compile(loss='categorical_crossentropy', optimizer='adam')
model.summary()

model.fit(data['train'], batch_size=128, nb_epoch=100, validation=data['validation'])
model.evaluate(data['test'])

