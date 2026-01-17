from flask import Flask, request, jsonify, render_template
import numpy as np
import os

app = Flask(__name__)

def rref(matrix, tol=1e-10):
    """Compute Reduced Row Echelon Form."""
    m, n = matrix.shape
    A = matrix.copy().astype(float)
    pivot_cols = []
    row = 0
    
    for col in range(n):
        # Find pivot
        pivot_row = None
        for i in range(row, m):
            if abs(A[i, col]) > tol:
                pivot_row = i
                break
        
        if pivot_row is None:
            continue
        
        pivot_cols.append(col)
        
        # Swap rows if needed
        if pivot_row != row:
            A[[row, pivot_row]] = A[[pivot_row, row]]
        
        # Normalize pivot row
        pivot_value = A[row, col]
        if abs(pivot_value) > tol:
            A[row] = A[row] / pivot_value
        
        # Eliminate other rows
        for i in range(m):
            if i != row and abs(A[i, col]) > tol:
                factor = A[i, col]
                A[i] = A[i] - factor * A[row]
        
        row += 1
        if row >= m:
            break
    
    # Round small values to zero
    A[np.abs(A) < tol] = 0
    return A, pivot_cols

def find_nullspace_basis_from_rref(rref_matrix, pivot_cols, n):
    """Find nullspace basis from RREF."""
    basis = []
    m, n_cols = rref_matrix.shape
    
    # Find free variables
    all_cols = set(range(n_cols))
    free_cols = sorted(list(all_cols - set(pivot_cols)))
    
    # Construct basis vectors
    for free_col in free_cols:
        basis_vector = np.zeros(n_cols)
        basis_vector[free_col] = 1
        
        # Solve for pivot variables
        for i, pivot_col in enumerate(pivot_cols):
            if i < m:
                basis_vector[pivot_col] = -rref_matrix[i, free_col]
        
        basis.append(basis_vector)
    
    return basis

def compute_real_eigenvalues(matrix):
    """Compute only real eigenvalues."""
    eigenvalues = np.linalg.eigvals(matrix)
    real_eigenvalues = []
    
    for val in eigenvalues:
        if abs(val.imag) < 1e-10:
            real_eigenvalues.append(val.real)
    
    return real_eigenvalues

def find_eigenspace_basis_rref(matrix, eigenvalue, tol=1e-8):
    """Find eigenspace basis using RREF."""
    n = matrix.shape[0]
    A_minus_lambda_I = matrix - eigenvalue * np.eye(n)
    
    # Compute RREF
    rref_matrix, pivot_cols = rref(A_minus_lambda_I, tol)
    
    # Find nullspace basis
    basis = find_nullspace_basis_from_rref(rref_matrix, pivot_cols, n)
    
    return basis, rref_matrix, pivot_cols

def format_number(num):
    """Format number for display."""
    if abs(num - round(num)) < 1e-10:
        return round(num)
    else:
        # Round to 6 decimal places
        return float(f"{num:.6f}")

@app.route('/')
def index():
    """Serve the main HTML page."""
    return render_template('index.html')

@app.route('/compute-eigenspaces', methods=['POST'])
def compute_eigenspaces():
    """API endpoint for computing eigenspaces."""
    try:
        # Get JSON data
        data = request.json
        if not data or 'matrix' not in data:
            return jsonify({"error": "No matrix provided"}), 400
        
        matrix_data = data.get('matrix')
        matrix = np.array(matrix_data, dtype=float)
        
        # Validate matrix
        if len(matrix.shape) != 2:
            return jsonify({"error": "Matrix must be 2-dimensional"}), 400
        
        if matrix.shape[0] != matrix.shape[1]:
            return jsonify({"error": "Matrix must be square"}), 400
        
        n = matrix.shape[0]
        if n > 5:
            return jsonify({"error": "Matrix size must be ≤ 5"}), 400
        
        # Compute eigenvalues
        eigenvalues = compute_real_eigenvalues(matrix)
        
        if not eigenvalues:
            return jsonify({
                "matrix_size": n,
                "eigenvalues": [],
                "eigenspaces": []
            })
        
        # Group unique eigenvalues
        unique_eigenvalues = []
        for val in eigenvalues:
            if not any(abs(val - u) < 1e-8 for u in unique_eigenvalues):
                unique_eigenvalues.append(val)
        
        # Prepare response
        response = {
            "matrix_size": n,
            "eigenvalues": [format_number(val) for val in unique_eigenvalues],
            "eigenspaces": []
        }
        
        # Compute eigenspaces
        for eigenval in unique_eigenvalues:
            basis, rref_matrix, pivot_cols = find_eigenspace_basis_rref(matrix, eigenval)
            
            # Format basis vectors
            formatted_basis = []
            for vec in basis:
                if not np.allclose(vec, 0, atol=1e-8):
                    formatted_basis.append([format_number(x) for x in vec])
            
            # Get free variables
            all_cols = set(range(n))
            free_cols = sorted(list(all_cols - set(pivot_cols)))
            
            # Create eigenspace info
            eigenspace_info = {
                "eigenvalue": format_number(eigenval),
                "geometric_multiplicity": len(formatted_basis),
                "basis": formatted_basis,
                "rref_details": {
                    "A_minus_lambda_I": [[format_number(x) for x in row] 
                                        for row in (matrix - eigenval * np.eye(n))],
                    "rref": [[format_number(x) for x in row] for row in rref_matrix],
                    "pivot_columns": pivot_cols,
                    "free_variables": free_cols
                }
            }
            
            # Add verification
            verification = []
            for i, vec in enumerate(basis):
                if not np.allclose(vec, 0, atol=1e-8):
                    Av = matrix @ vec
                    lambda_v = eigenval * vec
                    is_correct = np.allclose(Av, lambda_v, atol=1e-8)
                    verification.append({
                        "basis_vector_index": i,
                        "Av": [format_number(x) for x in Av],
                        "lambda_v": [format_number(x) for x in lambda_v],
                        "is_correct": bool(is_correct)
                    })
            
            eigenspace_info["verification"] = verification
            response["eigenspaces"].append(eigenspace_info)
        
        return jsonify(response)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({"status": "healthy", "service": "eigenspace-calculator"})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
