from tensorflow import keras
from keras.layers import Dense, Dropout, Flatten
from keras.models import Sequential
from keras.callbacks import CSVLogger
from sklearn.model_selection import train_test_split
from PIL import Image
from numpy import asarray
import os
import json

# set to true and specify model version number if you want to load a model
loadModel = False
modelNum = 4

# read model version from txt file
# if not loadModel:
#     with open('modelVersion.txt') as f:
#         modelNum = f.read()
#         f.close()

# iterate model number
if not loadModel:
    modelNum = str(int(modelNum) + 1)

print("Model version: ", modelNum)

# data should be 5 concatenated vectors of size 13 for each possible node
# additionally append a size 13 vector for the previous room, and a scalar to denote the depth
# data members are size 1 + (5 + 1) * 14 = 79
data = []
for d in list(open('data.txt')):
    array = json.loads(d.strip())
    # print(array)
    data.append(array)

data = asarray(data)
labels = asarray([json.loads(y.strip()) for y in list(open('labels.txt'))])
print(len(data), len(labels))
print(type(data), type(labels))
print(data.shape, labels.shape)
# Split the data
x_train, x_test, y_train, y_test = train_test_split(data, labels, test_size=0.2, shuffle=False)

try:
    if loadModel and "model" + str(modelNum) + ".keras" in os.listdir(os.getcwd()):
        #Load from a saved state
        model = keras.models.load_model("model" + modelNum + ".keras")
    else:
        # Combine layers
        layers = [keras.Input(shape=(99,), dtype="int64"),
                    # keras.layers.Dense(8, activation='relu'),
                    keras.layers.Dense(128, activation='relu'),
                    keras.layers.Dense(64, activation='relu'),
                    keras.layers.Dense(5, activation='softmax')]

        # Create and compile the model
        model = keras.Sequential(layers)

        # Compile the model
        model.compile(optimizer='adam',
                    loss=keras.losses.SparseCategoricalCrossentropy(from_logits=True),
                    metrics=['accuracy'])

    # Log training outputs
    log_file = "model" + str(modelNum) + ".log"
    print("Logging to: ", log_file)
    if not loadModel:
        csv_logger = CSVLogger(log_file, separator=',', append=True)
    else:
        csv_logger = CSVLogger(log_file, separator=',', append=False)

    # Training the model
    train_acc = model.fit(x_train, y_train, epochs=10).history['accuracy'][-1]
    test_acc = model.evaluate(x_test, y_test)[1]
    print("Training Accuracy:", train_acc)
    print("Testing Accuracy:", test_acc)

    model.save("model" + str(modelNum) + ".keras")

    # write new model number to file
    if not loadModel:
        with open('modelVersion.txt', 'w') as f:
            f.write(modelNum)
            f.close()

except KeyboardInterrupt:
    model.save("model" + str(modelNum) + ".keras")
    if not loadModel:
        with open('modelVersion.txt', 'w') as f:
            f.write(modelNum)
            f.close()