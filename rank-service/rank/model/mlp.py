from tensorflow import keras

class MLPModel:
    def __init__(self) -> None:
        self.model = keras.models.load_model('mlp_model')

    def predict(self,xs):
        return self.model.predict(xs)