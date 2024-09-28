# Makefile for KMeans Clustering Visualization Project
# Makefile for KMeans Clustering Visualization Project

# Install dependencies listed in requirements.txt
install:
		pip install -r requirements.txt

# Run the Flask application on localhost:3000
run:
		flask --app app run --host=0.0.0.0 --port=3000




