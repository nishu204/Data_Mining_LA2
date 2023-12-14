import numpy as np

class DBSCAN:
    def __init__(self, eps, min_samples):
        self.eps = eps
        self.min_samples = min_samples
        self.labels = None

    def fit(self, X):
        self.labels = np.full(X.shape[0], -1)  # -1 denotes noise, initialize with noise

        cluster_id = 0
        for i in range(X.shape[0]):
            if self.labels[i] != -1:  # Already assigned to a cluster
                continue

            neighbors = self._get_neighbors(X, i)

            if len(neighbors) < self.min_samples:
                self.labels[i] = -1  # Mark as noise
            else:
                self._expand_cluster(X, i, neighbors, cluster_id)
                cluster_id += 1

    def _get_neighbors(self, X, index):
        neighbors = []
        for i in range(X.shape[0]):
            if np.linalg.norm(X[index] - X[i]) < self.eps:
                neighbors.append(i)
        return neighbors

    def _expand_cluster(self, X, index, neighbors, cluster_id):
        self.labels[index] = cluster_id
        i = 0
        while i < len(neighbors):
            current_index = neighbors[i]
            if self.labels[current_index] == -1:
                self.labels[current_index] = cluster_id

            if self.labels[current_index] is None:
                self.labels[current_index] = cluster_id
                current_neighbors = self._get_neighbors(X, current_index)

                if len(current_neighbors) >= self.min_samples:
                    neighbors += current_neighbors

            i += 1