import os
import numpy as np
import librosa


def extrakt_features_for_genres(path):
    dirnames = []
    for base, dirs, files in os.walk(path):
        for directorie in dirs:
            dirnames.append(directorie)

    genres_features_array = np.zeros((len(dirnames), 24))
    genres_features_index = 0
    for dir in dirnames:
        for base, dirs, files in os.walk(path + "/" + dir):
            one_genre_features_array = np.zeros((len(files), 24))
            rowInd = 0
            for file in files:
                oneTrackFeatures = extrakt_features(path + "/" + dir + "/" + file)
                for row_ind, feature in enumerate(oneTrackFeatures):
                    one_genre_features_array[rowInd][row_ind] = feature
                print(str(rowInd + 1) + "% of " + str(dir) + " genre done")
                rowInd += 1
            for x in range(24):
                genres_features_array[genres_features_index][x] = np.mean(one_genre_features_array[:, x])
            genres_features_index += 1

    return dirnames, genres_features_array


def extrakt_features(track_path):
    y, sr = librosa.load(track_path, duration=30) # y - audio time series, sr - sample rate
    chroma_stft = librosa.feature.chroma_stft(y=y, sr=sr)
    spec_cent = librosa.feature.spectral_centroid(y=y, sr=sr)
    rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr)
    zerocr = librosa.feature.zero_crossing_rate(y)
    mfcc = librosa.feature.mfcc(y=y, sr=sr)
    features = [np.mean(chroma_stft), np.mean(spec_cent), np.mean(rolloff), np.mean(zerocr)]
    for mfccFeature in mfcc:
        features.append(np.mean(mfccFeature))
    return features
