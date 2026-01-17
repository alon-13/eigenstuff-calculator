from flask import Flask, request, jsonify, render_template
import numpy as np

app = Flask(__name__)

def rref(matrix, tol=1e-10):
    """
    Compute the Reduced Row Echelon Form (RREF) of a matrix.
    """
    m, n = matrix.shape
    rref_matrix = matrix.copy().astype(float)
    pivot_cols = []
    row = 0
    
    for col in range(n):
        # Find pivot
        pivot_row = None
        for i in range(row, m):
            if abs(rref_matrix[i, col]) > tol:
                pivot_row = i
                break
        
        if pivot_row is None:
            continue
        
        # Add to pivot columns
        pivot_cols.append(col)
        
        # Swap rows if needed
        if pivot_row != row:
            rref_matrix[[row, pivot_row]] = rref_matrix[[pivot_row, row]]
        
        # Normalize pivot row
        pivot_value = rref_matrix[row, col]
        if abs(pivot_value) > tol:
            rref_matrix[row] = rref_matrix[row] / pivot_value
        
        # Eliminate other rows
        for i in range(m):
            if i != row and abs(rref_matrix[i, col]) > tol:
                factor = rref_matrix[i, col]
                rref_matrix[i] = rref_matrix[i] - factor * rref_matrix[row]
        
        row += 1
        if row >= m:
            break
    
    # Round small values to zero
    rref_matrix[np.abs(rref_matrix) < tol] = 0
    
    return rref_matrix, pivot_cols

def find_nullspace_basis_from_rref(rref_matrix, pivot_cols, n):
    """
    Find basis for nullspace from RREF form.
    """
    basis = []
    m, n_cols = rref_matrix.shape
    
    # Find free variables (columns that are not pivot columns)
    all_cols = set(range(n_cols))
    free_cols = sorted(list(all_cols - set(pivot_cols)))
    
    # For each free variable, find a basis vector
    for free_col in free_cols:
        basis_vector = np.zeros(n_cols)
        basis_vector[free_col] = 1
        
        # For each pivot row, set the value for the pivot variable
        for i, pivot_col in enumerate(pivot_cols):
            if i < m:  # Check if we have this row
                basis_vector[pivot_col] = -rref_matrix[i, free_col]
        
        basis.append(basis_vector)
    
    return basis

def compute_real_eigenvalues(matrix):
    """
    Compute only real eigenvalues of the matrix.
    """
    eigenvalues = np.linalg.eigvals(matrix)
    real_eigenvalues = []
    
    for val in eigenvalues:
        if abs(val.imag) < 1e-10:
            real_eigenvalues.append(val.real)
    
    return real_eigenvalues

def find_eigenspace_basis_rref(matrix, eigenvalue, tol=1e-8):
    """
    Find eigenspace basis for an eigenvalue using RREF.
    """
    n = matrix.shape[0]
    
    # Create A - λI
    A_minus_lambda_I = matrix - eigenvalue * np.eye(n)
    
    # Compute RREF
    rref_matrix, pivot_cols = rref(A_minus_lambda_I, tol)
    
    # Find nullspace basis from RREF
    basis = find_nullspace_basis_from_rref(rref_matrix, pivot_cols, n)
    
    return basis, rref_matrix, pivot_cols

def format_number(num):
    """
    Format number to remove trailing zeros and .0 if integer.
    """
    if abs(num - round(num)) < 1e-10:
        return round(num)
    else:
        # Round to 6 decimal places and remove trailing zeros
        formatted = f"{num:.6f}"
        return float(formatted.rstrip('0').rstrip('.') if '.' in formatted else formatted)

def format_vector(vec):
    """
    Format vector components.
    """
    return [format_number(x) for x in vec]

def format_rref_matrix(rref_matrix):
    """
    Format RREF matrix for JSON response.
    """
    result = []
    for row in rref_matrix:
        formatted_row = [format_number(x) for x in row]
        result.append(formatted_row)
    return result

@app.route('/')
def index():
    """Serve the HTML page."""
    return render_template('index.html')

@app.route('/compute-eigenspaces', methods=['POST'])
def compute_eigenspaces():
    """
    API endpoint that accepts a matrix and returns eigenvalues with eigenspace bases.
    """
    try:
        # Get JSON data
        data = request.json
        if not data or 'matrix' not in data:
            return jsonify({"error": "No matrix provided"}), 400
        
        matrix_data = data.get('matrix')
        
        # Convert to numpy array
        matrix = np.array(matrix_data, dtype=float)
        
        # Validate matrix
        if len(matrix.shape) != 2:
            return jsonify({"error": "Matrix must be 2-dimensional"}), 400
        
        if matrix.shape[0] != matrix.shape[1]:
            return jsonify({"error": "Matrix must be square"}), 400
        
        n = matrix.shape[0]
        if n > 5:
            return jsonify({"error": "Matrix size must be ≤ 5"}), 400
        
        # Compute real eigenvalues
        eigenvalues = compute_real_eigenvalues(matrix)
        
        if not eigenvalues:
            return jsonify({
                "message": "No real eigenvalues found",
                "matrix_size": n,
                "eigenvalues": [],
                "eigenspaces": []
            })
        
        # Group eigenvalues (within tolerance)
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
        
        # Compute eigenspace for each unique eigenvalue
        for eigenval in unique_eigenvalues:
            basis, rref_matrix, pivot_cols = find_eigenspace_basis_rref(matrix, eigenval)
            
            # Format basis vectors
            formatted_basis = []
            for vec in basis:
                # Check if vector is not all zeros
                if not np.allclose(vec, 0, atol=1e-8):
                    formatted_basis.append(format_vector(vec))
            
            # Get free variables
            all_cols = set(range(n))
            free_cols = sorted(list(all_cols - set(pivot_cols)))
            
            eigenspace_info = {
                "eigenvalue": format_number(eigenval),
                "geometric_multiplicity": len(formatted_basis),
                "basis": formatted_basis,
                "rref_details": {
                    "A_minus_lambda_I": format_rref_matrix(matrix - eigenval * np.eye(n)),
                    "rref": format_rref_matrix(rref_matrix),
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
                        "Av": format_vector(Av),
                        "lambda_v": format_vector(lambda_v),
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
    app.run(debug=True)
