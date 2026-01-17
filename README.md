# eigenstuff-calculator


# Eigenstuff Calculator

## Project Overview

**What this is:**  
A full-stack web application designed to simplify complex Linear Algebra computations.

**Brief description:**  
The Eigenstuff Calculator is a cloud-hosted tool that provides a user-friendly interface for matrix operations, backed by a powerful Python mathematical engine.

**Problem it solves:**  
Manually calculating eigenvalues and eigenspaces for matrices larger than $2 \times 2$ is time-consuming and prone to arithmetic errors. This tool automates the process with high precision.

**What the program computes:**  
It solves the characteristic equation:

$$
\det(A - \lambda I) = 0
$$

to find eigenvalues and determines the basis vectors for the corresponding eigenspaces.

**Example Content:**  
For an input matrix of `[[2, 0], [0, 2]]`, the application correctly identifies a single eigenvalue of `2` and its associated basis vectors `[1, 0]` and `[0, 1]`.

---

##  System Requirements

**User Needs:**  
- A modern web browser (Chrome, Firefox, Safari, or Edge)  
- An active internet connection to access the public URL

**Python Version:**  
- Python 3.8 or higher (required for local development/hosting)

**Required Libraries:**  
- `NumPy`: For core linear algebra computations  
- `Flask`: To serve the web application  
- `Flask-CORS`: To handle cross-origin requests  
- `Gunicorn`: To run the production server on Render

**OS Compatibility:**  
- Fully cross-platform (Windows, macOS, Linux, Android, iOS) because it runs in a browser

---

## Installation / Setup

**Cloning the Project:**  
Download the source files (`app.py`, `index.html`, `requirements.txt`, `Procfile`) from your GitHub repository.

**Installing Dependencies:**  
```bash
pip install -r requirements.txt
