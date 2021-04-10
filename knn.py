import os
import numpy as np
from model import Model


class KNN(Model):

    def __init__(self, bd_path, genre_features):
        self._genres_features = genre_features
        self._bd_path = bd_path
        self._bestK = 3
        if os.path.getsize("bestK.txt") > 0:
            with open("bestK.txt", 'rb') as f:
                self._bestK = int(f.readline())
            f.close()
        else:
            with open("bestK.txt", 'w') as f:
                f.write(str(self.get_best_k()))
            f.close()

    def train_model(self) -> None:
        self._bestK = self.get_best_k()
        with open("bestK.txt", 'wb') as f:
            f.write(self._bestK)
        f.close()

    def approx_genres(self, track_path) -> list:
        probs = self.count_p(self.count_lable_distance_array(self.extrakt_features(track_path)), self._bestK)
        return probs

    def count_lable_distance_array(self, track_features):
        distanceArray = self.count_distance(track_features, self._genres_features)
        labelsDistanceArray = np.zeros(self._genres_features.shape)
        for column_ind in range(self._genres_features.shape[1]):
            column = distanceArray[:, column_ind].tolist()
            sortedIndexes = np.argsort(column)
            for row_ind in range(self._genres_features.shape[0]):
                labelsDistanceArray[row_ind][column_ind] = sortedIndexes[row_ind]

        return labelsDistanceArray

    def count_p(self, labelsDistanceArray, k):
        prob = []
        rows = labelsDistanceArray[:k]  # only rows we are interested
        labelIdexes = list(range(labelsDistanceArray.shape[0]))
        for lable in labelIdexes:
            eq = 0
            for row_ind, lableTable in enumerate(rows):
                for lab in lableTable:
                    if (lable == lab):
                        eq += 1
            prob.append(eq / rows.size)

        return prob

    def get_best_k(self):
        bestKs = []
        dirnames = []
        for base, dirs, files in os.walk(self._bd_path):
            for directorie in dirs:
                dirnames.append(directorie)

        genreCount = 0
        for dir in dirnames:

            for base, dirs, files in os.walk(self._bd_path + "/" + dir):
                ks = [1, 2, 3, 4, 5, 6]
                bestProb = 0
                bestk = 1
                for k in ks:
                    allprobs = []
                    for file in files:
                        oneTrackFeatures = self.extrakt_features(self._bd_path + "/" + dir + "/" + file)
                        probs = self.count_p(self.count_lable_distance_array(oneTrackFeatures), k)
                        allprobs.append(probs[genreCount])
                    if np.mean(allprobs) > bestProb:
                        bestk = k
                        bestProb = np.mean(allprobs)

            genreCount += 1
            bestKs.append(bestk)
            print("doc :" + str(dir) + " best k " + str(bestk) + " with average " + str(round(bestProb * 100, 1)) + "%")

        return round(np.mean(bestKs))
