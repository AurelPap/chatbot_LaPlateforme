import random
import json
import pickle
import numpy as np

import nltk
from nltk.stem import WordNetLemmatizer

import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Activation, Dropout
from tensorflow.keras.optimizers import SGD
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint

lemmatizer = WordNetLemmatizer()

intents = json.loads(open('data/intents.json').read())

words = []
question = []
documents = []
ignore_letters = ["?", "!", ".", ","]

for intent in intents['intents'] :
    for pattern in intent["tags"]:
        word_list = nltk.word_tokenize(pattern)
        words.extend(word_list)
        documents.append((word_list, intent['question']))
        if intent['question'] not in question :
            question.append(intent['question'])

words = [lemmatizer.lemmatize(word) for word in words if word not in ignore_letters]

words = sorted(set(words))

# flattened = []
# for item in question:
#     if isinstance(item, list):
#         for element in item:
#             if element not in flattened:
#                 flattened.append(element)
#     else:
#         if item not in flattened:
#             flattened.append(item)

# print(flattened)
question = sorted(set(question))

pickle.dump(words, open("models/words.pkl", "wb"))
pickle.dump(question, open("models/question.pkl", "wb"))

training = []
output_empty = [0] * len(question)

for document in documents:
    bag = []
    word_tags = document[0]
    word_tags = [lemmatizer.lemmatize(word.lower()) for word in word_tags]
    for word in words:
        bag.append(1) if word in word_tags else bag.append(0)

    output_row = list(output_empty)
    output_row[question.index(document[1])] = 1
    training.append([bag, output_row])

random.shuffle(training)

training = np.array(training, dtype=object)

train_x = list(training[:, 0])
train_y = list(training[:, 1])

model = Sequential()
model.add(Dense(128, input_shape=(len(train_x[0]),), activation = "relu"))
model.add(Dropout(0.5))
model.add(Dense(64, activation="relu"))
model.add(Dropout(0.5))
model.add(Dense(len(train_y[0]), activation="softmax"))
print(model.summary())

# sgd = SGD(learning_rate=0.01, decay=1e-6, momentum=0.9, nesterov=True)
sgd = tf.keras.optimizers.legacy.SGD(learning_rate=0.01, decay=1e-6, momentum=0.9, nesterov=True)
model.compile(loss="categorical_crossentropy", optimizer=sgd, metrics=["accuracy"])

# Define callbacks
early_stopping = EarlyStopping(monitor='accuracy', patience=100, restore_best_weights=True)
checkpoint = ModelCheckpoint('best_model.h5', monitor='accuracy', save_best_only=True, mode='min', verbose=1)

# Train the model with callbacks
h = model.fit(np.array(train_x), np.array(train_y),
              epochs=500000,
              batch_size=5,
              verbose=1,
              callbacks=[early_stopping, checkpoint])


model.save("models/chatbot_model.h5", h)
print("Done training.")
