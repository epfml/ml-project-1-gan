import numpy as np
from random import randint
import random


class SMOTE(object):
    def __init__(self, distance="euclidean", dims=512, k=5, sampling_strategy=1.0):
        super(SMOTE, self).__init__()
        self.newindex = 0
        self.k = k
        self.dims = dims
        self.distance_measure = distance
        self.sampling_strategy = sampling_strategy

    def populate(self, N, i, nnarray, min_samples, k):
        while N:
            nn = randint(0, k - 2)

            diff = min_samples[nnarray[nn]] - min_samples[i]
            gap = random.uniform(0, 1)

            self.synthetic_arr[self.newindex, :] = min_samples[i] + gap * diff

            self.newindex += 1

            N -= 1

    def k_neighbors(self, euclid_distance, k):
        nearest_idx = np.zeros((euclid_distance.shape[0], k), dtype=np.int64)

        for i in range(euclid_distance.shape[0]):
            idxs = np.argsort(euclid_distance[i])
            nearest_idx[i, :] = idxs[1 : k + 1]

        return nearest_idx

    def find_k(self, X, k):
        euclid_distance = np.zeros((X.shape[0], X.shape[0]), dtype=np.float32)

        for i in range(len(X)):
            dif = (X - X[i]) ** 2
            dist = np.sqrt(dif.sum(axis=1))
            euclid_distance[i] = dist

        return self.k_neighbors(euclid_distance, k)

    def generate(self, min_samples, N, k):
        """
        Returns (N/100) * n_minority_samples synthetic minority samples.
        Parameters
        ----------
        min_samples : numpy_array-like, shape = [n_minority_samples, n_features]
            Holds the minority samples
        N : percentage of new synthetic samples:
            n_synthetic_samples = N/100 * n_minority_samples. Can be < 100.
        k : int. Number of nearest neighbors.
        Returns
        -------
        S : Synthetic samples. array,
            shape = [(N/100) * n_minority_samples, n_features].
        """
        T = min_samples.shape[0]
        self.synthetic_arr = np.zeros((int(N / 100 * T), self.dims))
        N = int(N / 100)
        if self.distance_measure == "euclidean":
            indices = self.find_k(min_samples, k)
        for i in range(indices.shape[0]):
            self.populate(N, i, indices[i], min_samples, k)
        self.newindex = 0
        return self.synthetic_arr

    def fit_generate(self, X, y):
        # get occurrence of each class
        unique_classes = np.unique(y)
        print(unique_classes)
        class_counts = np.array([np.sum(y == c) for c in unique_classes])
        print(class_counts)
        dominant_class = unique_classes[np.argmax(class_counts)]
        dominant_class_count = class_counts[np.argmax(class_counts)]

        X_resampled, y_resampled = X.copy(), y.copy()

        for class_label in unique_classes:
            print(class_label)
            if class_label != dominant_class:
                # calculate the amount of synthetic data to generate
                N = (
                    (dominant_class_count - class_counts[class_label])
                    * self.sampling_strategy
                    * 100
                    / class_counts[class_label]
                )
                candidates = X[y == class_label]
                xs = self.generate(candidates, N, self.k)
                X_resampled = np.concatenate((X, xs), axis=0)
                ys = np.ones(xs.shape[0]) * class_label
                y_resampled = np.concatenate((y, ys), axis=0)

        return X_resampled, y_resampled


class RandomUnderSampler:
    def __init__(self, sampling_strategy="auto", random_state=None):
        self.sampling_strategy = sampling_strategy
        self.random_state = random_state

    def fit_resample(self, X, y):
        if self.random_state is not None:
            np.random.seed(self.random_state)

        unique_classes, class_counts = np.unique(y, return_counts=True)
        min_class = unique_classes[np.argmin(class_counts)]
        maj_class = unique_classes[np.argmax(class_counts)]

        min_count = class_counts[np.argmin(class_counts)]
        maj_count = class_counts[np.argmax(class_counts)]

        if self.sampling_strategy == "auto":
            ratio = float(maj_count) / min_count
        else:
            ratio = float(self.sampling_strategy)

        if ratio >= 1.0:
            return X, y  # No need to undersample

        num_samples_to_keep = int(maj_count * ratio)

        maj_indices = np.where(y == maj_class)[0]
        min_indices = np.where(y == min_class)[0]

        if num_samples_to_keep >= len(maj_indices):
            return X, y  # No need to undersample

        selected_maj_indices = np.random.choice(
            maj_indices, size=num_samples_to_keep, replace=False
        )
        combined_indices = np.concatenate([selected_maj_indices, min_indices])

        X_resampled = X[combined_indices]
        y_resampled = y[combined_indices]

        return X_resampled, y_resampled