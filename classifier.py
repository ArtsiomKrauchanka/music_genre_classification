from knn import KNN
from bayes import Bayes
from model import Model
import os
import numpy as np


class Classifier:

    def __init__(self):
        if os.path.getsize("bd_path.txt") > 0:
            with open("bd_path.txt", 'rb') as f:
                self._bd_path = f.readline()
            f.close()
        self._genre_features = np.load('genres_features.npy')
        self._knn = KNN(self._bd_path, self._genre_features)
        self._bayes = Bayes(self._bd_path, self._genre_features)
        self._genres = np.load('genres.npy')

    def change_db(self, path):
        self._bd_path = path
        with open("bd_path.txt", 'w') as f:
            f.write(path)
        f.close()
        # self._genres, self._genre_features = extract_funtions.extrakt_features_for_genres(self._bd_path)
        # np.save('genres.npy', self._genres)
        # np.save("genres_features.npy", self._genre_features)
        self._knn = KNN(self._bd_path, self._genre_features)
        self._bayes = Bayes(self._bd_path, self._genre_features)
        #self._knn.train_model()
        self._bayes.train_model()

    def interpret_approx_array(self, track_path, model: Model):
        genres = []
        probabilities = []
        probs = model.approx_genres(track_path)
        probssort = np.argsort(probs)
        probssort = np.flip(probssort, 0)
        for i in probssort:
            genres.append(self._genres[i])
            probabilities.append(round(probs[i] * 100, 2))
        return genres, probabilities  # od największych do najmniejszych

    def approximate(self, track_path, mode) -> (list, list):
        if mode == "knn":
            return self.interpret_approx_array(track_path, self._knn)
        if mode == "bayes":
            return self.interpret_approx_array(track_path, self._bayes)
        return list(), list()

    def get_db_name(self):
        return self._bd_path
