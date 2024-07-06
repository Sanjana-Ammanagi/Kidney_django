import os
import urllib.request as request
from zipfile import ZipFile
import tensorflow as tf
from pathlib import Path
from src.cnnClassifier.entity.config_entity import (prepareBaseModelConfig)
class PrepareBaseModel:
    def _init_(self, config: prepareBaseModelConfig):
        self.config = config

    
    def get_base_model(self):
        self.model = tf.keras.applications.vgg16.VGG16(
            input_shape=self.config.params_image_size,
            weights=self.config.params_weights,
            include_top=self.config.params_include_top
        )

        self.save_model(path=self.config.base_model_path, model=self.model)

    

    @staticmethod
    def _prepare_full_model(model, classes, freeze_all, freeze_till, learning_rate):
        if freeze_all:
            for layer in model.layers:
                model.trainable = False
        elif (freeze_till is not None) and (freeze_till > 0):
            for layer in model.layers[:-freeze_till]:
                model.trainable = False
        flatten_in = tf.keras.layers.Flatten()(model.output)
        dense_layer = tf.keras.layers.Dense(2056, activation='relu')(flatten_in)
        batch_norm = tf.keras.layers.BatchNormalization()(dense_layer)
        dropout_layer = tf.keras.layers.Dropout(0.4)(batch_norm)
        dense_layer2 = tf.keras.layers.Dense(1024, activation='relu')(dropout_layer)
        batch_norm = tf.keras.layers.BatchNormalization()(dense_layer2)
        dropout_layer = tf.keras.layers.Dropout(0.4)(batch_norm)
        prediction = tf.keras.layers.Dense(
            units=1,  #number of classes
            activation="sigmoid" #softmax
        )(dropout_layer)

        full_model = tf.keras.models.Model(
            inputs=model.input,
            outputs=prediction
        )

        full_model.compile(
            optimizer='adam',
            loss=tf.keras.losses.BinaryCrossentropy(), #SparseCate or Categorical
            metrics=["accuracy"]
        )

        full_model.summary()
        return full_model
    
    
    def update_base_model(self):
        self.full_model = self._prepare_full_model(
            model=self.model,
            classes=self.config.params_classes,
            freeze_all=True,
            freeze_till=None,
            learning_rate=self.config.params_learning_rate
        )

        self.save_model(path=self.config.updated_base_model_path, model=self.full_model)

    
        
    @staticmethod
    def save_model(path: Path, model: tf.keras.Model):
        model.save(path)