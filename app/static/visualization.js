// Get references to the plot and controls
const plotDiv = document.getElementById('visualization');
const initMethodSelect = document.getElementById('init-method');

// Function to plot data points and centroids
function plotData(data, centroids) {
    const dataTrace = {
        x: data.map(point => point[0]),
        y: data.map(point => point[1]),
        mode: 'markers',
        type: 'scatter',
        name: 'Data Points',
        marker: { size: 8, color: 'blue' }
    };

    const centroidTrace = {
        x: centroids.map(point => point[0]),
        y: centroids.map(point => point[1]),
        mode: 'markers',
        type: 'scatter',
        name: 'Centroids',
        marker: { size: 12, color: 'red', symbol: 'x' }
    };

    Plotly.newPlot(plotDiv, [dataTrace, centroidTrace]);
}

// Function to handle generating new data
async function generateData() {
    const initMethod = initMethodSelect.value;

    try {
        const response = await fetch('/generate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ init_method: initMethod })
        });

        if (response.ok) {
            const result = await response.json();
            plotData(result.data, result.centroids);
        } else {
            console.error('Failed to fetch data from the backend');
        }
    } catch (error) {
        console.error('Error:', error);
    }
}

// Function to step through the clustering process
async function stepThrough() {
    try {
        const response = await fetch('/step', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });

        if (response.ok) {
            const result = await response.json();
            plotData(result.data, result.centroids);
        } else {
            console.error('Failed to step through the clustering process');
        }
    } catch (error) {
        console.error('Error:', error);
    }
}

// Function to run the clustering until convergence
async function runToConvergence() {
    try {
        const response = await fetch('/converge', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });

        if (response.ok) {
            const result = await response.json();
            plotData(result.data, result.centroids);
        } else {
            console.error('Failed to run clustering to convergence');
        }
    } catch (error) {
        console.error('Error:', error);
    }
}

// Function to reset the visualization
function resetVisualization() {
    Plotly.newPlot(plotDiv, []); // Clear the plot
    fetch('/reset', { method: 'POST' }) // Optional: call reset endpoint
        .then(response => response.json())
        .then(data => console.log(data.message))
        .catch(error => console.error('Error:', error));
}

// Attach event listeners to buttons
document.getElementById('generate-data').addEventListener('click', generateData);
document.getElementById('step-through').addEventListener('click', stepThrough);
document.getElementById('run-to-convergence').addEventListener('click', runToConvergence);
document.getElementById('reset').addEventListener('click', resetVisualization);
