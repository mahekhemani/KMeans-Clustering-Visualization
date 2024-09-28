import numpy as np

class KMeansClustering:
    def __init__(self, n_clusters=3, init_method='random', max_iters=100):
        self.n_clusters = n_clusters
        self.init_method = init_method
        self.max_iters = max_iters
        self.centroids = None
        self.current_iter = 0  # Track the current iteration for step-through functionality
        self.converged = False

    def fit(self, X):
        # Initialize centroids
        self.centroids = self._initialize_centroids(X)
        for _ in range(self.max_iters):
            self.current_iter += 1
            # Assign clusters
            clusters = self._assign_clusters(X)
            # Update centroids
            new_centroids = self._update_centroids(X, clusters)
            # Check for convergence
            if np.all(self.centroids == new_centroids):
                self.converged = True
                break
            self.centroids = new_centroids

    def fit_step(self, X):
        """Perform one iteration (step) of the clustering process."""
        if self.converged or self.current_iter >= self.max_iters:
            return  # Stop if already converged or reached max iterations

        # Assign clusters
        clusters = self._assign_clusters(X)
        # Update centroids
        new_centroids = self._update_centroids(X, clusters)
        # Check for convergence
        if np.all(self.centroids == new_centroids):
            self.converged = True
        self.centroids = new_centroids
        self.current_iter += 1

    def _initialize_centroids(self, X):
        # Initialization logic (random, farthest-first, kmeans++)
        if self.init_method == 'random':
            indices = np.random.choice(X.shape[0], self.n_clusters, replace=False)
            return X[indices]
        elif self.init_method == 'farthest-first':
            centroids = [X[np.random.choice(X.shape[0])]]
            for _ in range(1, self.n_clusters):
                distances = np.min([np.linalg.norm(X - c, axis=1) for c in centroids], axis=0)
                centroids.append(X[np.argmax(distances)])
            return np.array(centroids)
        elif self.init_method == 'kmeans++':
            centroids = [X[np.random.choice(X.shape[0])]]
            for _ in range(1, self.n_clusters):
                distances = np.min([np.linalg.norm(X - c, axis=1) for c in centroids], axis=0)
                probabilities = distances / np.sum(distances)
                centroids.append(X[np.random.choice(X.shape[0], p=probabilities)])
            return np.array(centroids)
        else:
            raise ValueError("Unknown initialization method")

    def _assign_clusters(self, X):
        # Compute distances between points and centroids
        distances = np.array([np.linalg.norm(X - centroid, axis=1) for centroid in self.centroids])
        # Assign clusters based on nearest centroid
        return np.argmin(distances, axis=0)

    def _update_centroids(self, X, clusters):
        # Recompute centroids based on the mean of assigned points
        return np.array([X[clusters == k].mean(axis=0) for k in range(self.n_clusters)])

    def predict(self, X):
        # Predict the nearest cluster for each data point
        clusters = self._assign_clusters(X)
        return clusters
