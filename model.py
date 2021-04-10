from abc import ABC, abstractmethod
import extract_funtions
import numpy as np



class Model(ABC):


    @abstractmethod
    def train_model(self) -> None:
        pass

    @abstractmethod
    def approx_genres(self, track_path) -> list:
        pass

    def extrakt_features(self, audioTrackPath):
        return extract_funtions.extrakt_features(audioTrackPath)

    def count_distance(self, track_features, genres_features):
        distanceArray = np.zeros(genres_features.shape)
        for row_ind, feature in enumerate(genres_features):
            for x in range(len(feature)):
                dist = (track_features[x] - feature[x])
                distanceArray[row_ind][x] = (abs(dist))
        return distanceArray