from . import app
from flask import request, jsonify, render_template
from .kmeans import KMeansClustering
import numpy as np

# Global variables to keep the state of the clustering
kmeans = None
X = None

# Home route to render the main page
@app.route('/')
def index():
    return render_template('index.html')

# Endpoint to generate a new dataset and perform clustering
@app.route('/generate', methods=['POST'])
def generate_data():
    global kmeans, X
    X = np.random.rand(100, 2)  # 100 data points with 2 features
    init_method = request.json.get('init_method', 'random')
    kmeans = KMeansClustering(n_clusters=3, init_method=init_method)
    kmeans.fit(X)
    clusters = kmeans.predict(X).tolist()
    centroids = kmeans.centroids.tolist()
    return jsonify({'data': X.tolist(), 'clusters': clusters, 'centroids': centroids})

# Endpoint to perform a single step of the clustering process
@app.route('/step', methods=['POST'])
def step_clustering():
    global kmeans, X
    if kmeans and X is not None:
        kmeans.fit_step(X)
        clusters = kmeans.predict(X).tolist()
        centroids = kmeans.centroids.tolist()
        return jsonify({'data': X.tolist(), 'clusters': clusters, 'centroids': centroids})
    else:
        return jsonify({'error': 'Clustering not initialized'}), 400

# Endpoint to run the clustering until convergence
@app.route('/converge', methods=['POST'])
def converge_clustering():
    global kmeans, X
    if kmeans and X is not None:
        kmeans.fit(X)
        clusters = kmeans.predict(X).tolist()
        centroids = kmeans.centroids.tolist()
        return jsonify({'data': X.tolist(), 'clusters': clusters, 'centroids': centroids})
    else:
        return jsonify({'error': 'Clustering not initialized'}), 400

# Reset endpoint to clear current state (if needed for future use)
@app.route('/reset', methods=['POST'])
def reset_clustering():
    global kmeans, X
    kmeans = None
    X = None
    return jsonify({'message': 'Clustering reset successfully'})
