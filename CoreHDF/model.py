import tensorflow as tf
import tensorflow.keras as keras
import functools


def export_model(train_path, test_path, image_size, validation_split=0.2, labels='inferred', seed=42,
                 batch_size=32, epochs=10, export_path='thermal_model'):
    # TODO: maybe artificially increase the dataset size by image transformations
    train_ds = tf.keras.preprocessing.image_dataset_from_directory(
        train_path,
        subset='training',
        labels=labels,
        label_mode=tf.keras.losses.BinaryCrossentropy,
        validation_split=validation_split,
        image_size=image_size,
        seed=seed,
        batch_size=batch_size,
    )
    val_ds = tf.keras.preprocessing.image_dataset_from_directory(
        train_path,
        subset='validation',
        labels=labels,
        label_mode=tf.keras.losses.BinaryCrossentropy,
        validation_split=validation_split,
        image_size=image_size,
        seed=seed,
        batch_size=batch_size
    )
    test_ds = tf.keras.preprocessing.image_dataset_from_directory(
        test_path,
        labels=labels,
        label_mode=tf.keras.losses.BinaryCrossentropy,
        image_size=image_size,
        seed=seed,
        batch_size=batch_size
    )

    dataset_size = train_ds.cardinality()

    AUTOTUNE = tf.data.AUTOTUNE
    train_ds = train_ds.cache().shuffle(1000).prefetch(buffer_size=AUTOTUNE)
    val_ds = val_ds.cache().prefetch(buffer_size=AUTOTUNE)

    DefaultConv2D = functools.partial(keras.layers.Conv2D, kernel_size=3, strides=1, padding='same')

    # TODO: tune the model's hyperparameters
    model = keras.models.Sequential([
        keras.layers.experimental.preprocessing.Rescaling(scale=1. / 255, input_shape=image_size),
        DefaultConv2D(filters=64, kernel_size=7, input_shape=[image_size[0], image_size[1], 3]),
        keras.layers.MaxPool2D(pool_size=2),
        DefaultConv2D(filters=128),
        DefaultConv2D(filters=128),
        keras.layers.MaxPooling2D(pool_size=2),
        DefaultConv2D(filters=256),
        DefaultConv2D(filters=256),
        keras.layers.MaxPooling2D(pool_size=2),
        keras.layers.Flatten(),
        keras.layers.Dense(units=128, activation='relu'),
        keras.layers.Dropout(0.5),
        keras.layers.Dense(units=64, activation='relu'),
        keras.layers.Dropout(0.5),
        keras.layers.Dense(units=1, activation='sigmoid')
    ])

    model.compile(optimizer=keras.optimizers.Adam,
                  loss=keras.losses.BinaryCrossentropy,
                  metrics=keras.metrics.Accuracy)

    history = model.fit(train_ds,
                        steps_per_epoch=int(0.75 * dataset_size / batch_size),
                        validation_data=val_ds,
                        validation_steps=int(0.15, dataset_size / batch_size),
                        epochs=epochs)

    model.save(export_path)

    return history

