# -*- coding: utf-8 -*-
"""SimpleXml.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1ZLBNKY4Cile4EZslasgQ0z9hMf4rZJBv
"""

import tensorflow as tf
import numpy as np # for multidimensional arrays

# Word index
word_index = {}
word_index["<PAD>"] = 0
# word_index["<START>"] = 1
word_index["<UNK>"] = 2  # unknown
# word_index["<UNUSED>"] = 3

word_index["."] = 4
word_index["validationxml"] = 5
word_index["document"] = 6
word_index["displayxml"] = 7
word_index["sheets"] = 8
word_index["sheet"] = 9
word_index["root"] = 10
word_index["node"] = 11
word_index["base"] = 12
word_index["dlitem"] = 13
word_index["member"] = 14
word_index["@X"] = 15
word_index["@Y"] = 16
word_index["@Z"] = 17
word_index

reverse_word_index = dict([(value, key) for (key, value) in word_index.items()])

train_xml_0 = "8.014999/8.014540/./validationxml/document/displayxml/sheets/sheet/document/root/node/base/base/node/base/base/dlitem/dlitem/dlitem/dlitem/dlitem/dlitem/member/@Z"
train_xml_1 = "8.014999/8.014540/./validationxml/document/displayxml/sheets/sheet/document/root/node/base/base/node/base/base/dlitem/dlitem/dlitem/dlitem/dlitem/dlitem/member/@X"
train_xml_2 = "8.014999/8.014540/./validationxml/document/displayxml/sheets/sheet/document/root/base/base/node/base/base/dlitem/dlitem/dlitem/dlitem/dlitem/dlitem/member/@Z"
train_xml_3 = "8.014999/8.014540/./validationxml/document/displayxml/sheets/sheet/document/root/base/base/node/base/base/dlitem/dlitem/dlitem/dlitem/dlitem/dlitem/member/@X"

test_xml_0 = "8.014999/8.014540/./validationxml/document/displayxml/sheets/sheet/document/root/node/base/base/base/node/base/base/dlitem/dlitem/dlitem/dlitem/dlitem/dlitem/member/@Z"
test_xml_1 = "8.014999/8.014540/./validationxml/document/displayxml/sheets/sheet/document/root/node/base/base/base/node/base/base/dlitem/dlitem/dlitem/dlitem/dlitem/dlitem/member/@X"

# Convert each test xml array to values from 0.0-1.0
def xml_to_input_arr(xml_str):
  arr_xml = xml_str.split('/')
  pads = [0] * (42 - len(arr_xml))
  
  word_values = []
  for index, name in enumerate(arr_xml):
    if index > 1: # skip baseline and compare values
      word_values.append(word_index[name])
      
  word_values.extend(pads)
  
  np_word_values = np.array(word_values, dtype=np.uint8)
  
  np_word_bits = np.unpackbits(np_word_values)
  
  
  np_word_bits = np_word_bits.astype(float) # convert values to float
  np_word_bits = np.insert(np_word_bits, 0, float(arr_xml[1])/10.0) # hack for now
  np_word_bits = np.insert(np_word_bits, 0, float(arr_xml[0])/10.0) # hack for now
  
  return np_word_bits

# Initialize data
train_data = np.ndarray(shape = (4,1,322))
train_data[0] = [xml_to_input_arr(train_xml_0)]
train_data[1] = [xml_to_input_arr(train_xml_1)]
train_data[2] = [xml_to_input_arr(train_xml_2)]
train_data[3] = [xml_to_input_arr(train_xml_3)]

train_labels = np.ndarray(shape = (4,))
train_labels[0] = 1
train_labels[1] = 0
train_labels[2] = 1
train_labels[3] = 0

test_data = np.ndarray(shape = (6,1,322))
test_data[0] = [xml_to_input_arr(train_xml_0)]
test_data[1] = [xml_to_input_arr(train_xml_1)]
test_data[2] = [xml_to_input_arr(train_xml_2)]
test_data[3] = [xml_to_input_arr(train_xml_3)]
test_data[4] = [xml_to_input_arr(test_xml_0)]
test_data[5] = [xml_to_input_arr(test_xml_1)]

test_labels = np.ndarray(shape = (6,))
test_labels[0] = 1
test_labels[1] = 0
test_labels[2] = 1
test_labels[3] = 0
test_labels[4] = 1
test_labels[5] = 0

model = tf.keras.models.Sequential([
  tf.keras.layers.Flatten(input_shape=(1, 322)),
  tf.keras.layers.Dense(50, activation=tf.nn.relu),
  tf.keras.layers.Dropout(0.2),
  tf.keras.layers.Dense(2, activation=tf.nn.softmax)
])

model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

# Our train_data is very short (just 4 items). We need lot of epochs to get somewhere
model.fit(train_data, train_labels, epochs=100)

# See final loss and accuracy
model.evaluate(test_data, test_labels)

# Review data
predictions = model.predict(test_data)
for index, test_data_item in enumerate(test_data):
  print("Test_data index: " + str(index) , "Label: " + str(test_labels[index]),  "Prediction: " + str(predictions[index]), "Max Prediction: " + str(np.argmax(predictions[index])))