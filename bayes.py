import os
import numpy as np
from model import Model


class Bayes(Model):

    def __init__(self, bd_path, genre_features):
        self._genres_features = genre_features
        self._bd_path = bd_path
        self._average_distance = []
        if os.path.getsize('average_distance.npy') > 0:
            self._average_distance = np.load('average_distance.npy')
        else:
            self.train_model()
        self._prob_genres_feature_array = []
        if os.path.getsize('prob_genres_feature_array.npy') > 0:
            self._prob_genres_feature_array = np.load('prob_genres_feature_array.npy')
        else:
            self.train_model()

    def train_model(self) -> None:
        self._average_distance = self.average_distance_genres()
        np.save('average_distance.npy', self._average_distance)
        self._prob_genres_feature_array = self.prob_genres_feature()
        np.save('prob_genres_feature_array.npy', self._prob_genres_feature_array)

    def approx_genres(self, track_path) -> list:
        probs_bayes = self.bayes_prob(
            self.prob_track_features_belong_to_genre(track_path))
        return probs_bayes

    def average_distance_genres(self):
        dirnames = []
        for base, dirs, files in os.walk(self._bd_path):
            for directorie in dirs:
                dirnames.append(directorie)

        av_dist_genres_array = np.zeros((len(dirnames), 24))
        av_dist_genres_array_index = 0
        for dir in dirnames:
            for base, dirs, files in os.walk(self._bd_path + "/" + dir):
                dist_genre_array = np.zeros((len(files), 24))
                rowInd = 0
                for file in files:
                    oneTrackFeatures = self.extrakt_features(self._bd_path + "/" + dir + "/" + file)
                    dist_array = self.count_distance(oneTrackFeatures, self._genres_features)  # genres x 24
                    for x in range(24):
                        dist_genre_array[rowInd][x] = dist_array[av_dist_genres_array_index][x]
                    print(str(rowInd + 1) + "% of " + str(dir) + " genre done")
                    rowInd += 1
                for x in range(24):
                    av_dist_genres_array[av_dist_genres_array_index][x] = np.mean(dist_genre_array[:, x])
                av_dist_genres_array_index += 1

        return av_dist_genres_array

    def prob_genres_feature(self):

        dirnames = []
        for base, dirs, files in os.walk(self._bd_path):
            for directorie in dirs:
                dirnames.append(directorie)

        prob_genres_features_array = np.zeros((len(dirnames), 24))
        prob_genres_features_index = 0
        for dir in dirnames:
            for base, dirs, files in os.walk(self._bd_path + "/" + dir):
                belong_one_genre_features_array = np.zeros((len(files), 24))
                rowInd = 0
                for file in files:
                    oneTrackFeatures = self.extrakt_features(self._bd_path + "/" + dir + "/" + file)
                    track_dist_array = self.count_distance(oneTrackFeatures, self._genres_features)
                    for x in range(24):
                        isBelong = 0
                        if (self._average_distance[prob_genres_features_index][x] >=
                                track_dist_array[prob_genres_features_index][x]):
                            isBelong = 1
                        belong_one_genre_features_array[rowInd][x] = isBelong

                    print(str(rowInd + 1) + "% of " + str(dir) + " genre done")
                    rowInd += 1
                for x in range(24):
                    prob_genres_features_array[prob_genres_features_index][x] = np.sum(
                        belong_one_genre_features_array[:, x]) / len(belong_one_genre_features_array[:, x])
                prob_genres_features_index += 1

        return prob_genres_features_array

    def prob_track_features_belong_to_genre(self, track_path):
        track_features = self.extrakt_features(track_path)
        dist_array = self.count_distance(track_features, self._genres_features)
        is_belong_feature_to_genres = np.zeros(self._average_distance.shape)
        prob_track_features_belong_to_genres_array = np.zeros(self._average_distance.shape)

        for row_ind, av_dist_feature_array in enumerate(self._average_distance):
            for x in range(24):
                isBelong = 0
                if (self._average_distance[row_ind][x] >=
                        dist_array[row_ind][x]):
                    isBelong = 1
                is_belong_feature_to_genres[row_ind][x] = isBelong

        for row_ind, is_belong_feature_to_genre in enumerate(is_belong_feature_to_genres):
            for x in range(24):
                if is_belong_feature_to_genre[x] == 1:
                    prob_track_features_belong_to_genres_array[row_ind][x] = self._prob_genres_feature_array[row_ind][
                        x]
                else:
                    prob_track_features_belong_to_genres_array[row_ind][x] = 1 - \
                                                                             self._prob_genres_feature_array[row_ind][
                                                                                 x]

        return prob_track_features_belong_to_genres_array

    def bayes_prob(self, prob_track_features_belong_to_genres_array):
        prob_class = 1 / prob_track_features_belong_to_genres_array.shape[0]
        prob_feature = 1 / 2
        prob = []
        for row_ind, prob_track_features_belong_to_genre in enumerate(prob_track_features_belong_to_genres_array):
            bayes_genre_features_prob = []
            for x in range(24):
                feature_prob_in_class = prob_track_features_belong_to_genre[x]
                bayes_features_prob = ((feature_prob_in_class * prob_class) / prob_feature)
                bayes_genre_features_prob.append(bayes_features_prob)
            prob.append(np.mean(bayes_genre_features_prob))
        return prob  # size = len(genres)
