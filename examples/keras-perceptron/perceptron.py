import tensorflow as tf
import wandb

# logging code
run = wandb.init()
config = run.config

# load data
(X_train, y_train), (X_test, y_test) = tf.keras.datasets.mnist.load_data()
img_width = X_train.shape[1]
img_height = X_train.shape[2]

### Change1
### Adding this section finetune the model and give more accurate outputs
#normalize data
X_train = X_train.astype('float32') / 255
X_test = X_test.astype('float32') / 255


# one hot encode outputs
y_train = tf.keras.utils.to_categorical(y_train)
y_test = tf.keras.utils.to_categorical(y_test)
labels = [str(i) for i in range(10)]

num_classes = y_train.shape[1]

### Change2
### Adding more layers
# create model
model = tf.keras.models.Sequential()
model.add(tf.keras.layers.Flatten(input_shape=(img_width, img_height)))
model.add(tf.keras.layers.Dense(50, activation='relu'))
model.add(tf.keras.layers.Dense(100, activation='relu'))
model.add(tf.keras.layers.Dense(200, activation='relu'))
model.add(tf.keras.layers.Dense(400, activation='relu'))
model.add(tf.keras.layers.Dense(50, activation='relu'))
model.add(tf.keras.layers.Dense(num_classes, activation='softmax'))
model.compile(loss='categorical_crossentropy', optimizer='adam',
              metrics=['accuracy'])

# Fit the model
model.fit(X_train, y_train, epochs=10, validation_data=(X_test, y_test),
          callbacks=[wandb.keras.WandbCallback(data_type="image", labels=labels, save_model=False)])
