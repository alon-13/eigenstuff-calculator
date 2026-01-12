from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np

app = Flask(__name__)
CORS(app)  # Allows the frontend to talk to the backend

@app.route('/compute', methods=['POST'])
def compute():
    try:
        data = request.json
        matrix_data = data.get('matrix')
        
        # Convert to NumPy array
        matrix = np.array(matrix_data, dtype=float)
        
        if matrix.shape[0] != matrix.shape[1]:
            return jsonify({"error": "Matrix must be square"}), 400
        
        # Calculate Eigenvalues and Eigenvectors
        # eigenvalues: 1D array
        # eigenvectors: 2D array where columns are the vectors
        eigenvalues, eigenvectors = np.linalg.eig(matrix)
        
        results = []
        for i in range(len(eigenvalues)):
            results.append({
                "eigenvalue": round(complex(eigenvalues[i]).real, 4), 
                "eigenvector": [round(val, 4) for val in eigenvectors[:, i]]
            })
            
        return jsonify({"results": results})

    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True, port=5000)
