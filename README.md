# eigenstuff-calculator


# Eigenstuff Calculator

##  Project Overview
**What this is:** A full-stack web application designed to simplify complex Linear Algebra computations.  
**Brief description:** The Eigenstuff Calculator is a cloud-hosted tool that provides a user-friendly interface for matrix operations, backed by a powerful Python mathematical engine.  
**Problem it solves:** Manually calculating eigenvalues and eigenspaces for matrices larger than $2 \times 2$ is time-consuming and prone to arithmetic errors. This tool automates the process with high precision.  
**What the program computes:** It solves the characteristic equation:

$$
\det(A - \lambda I) = 0
$$

to find eigenvalues and determines the basis vectors for the corresponding eigenspaces.  
**Example Content:** For an input matrix of `[[2, 0], [0, 2]]`, the application correctly identifies a single eigenvalue of `2` and its associated basis vectors `[1, 0]` and `[0, 1]`.

##  System Requirements
**User Needs:** A modern web browser (Chrome, Firefox, Safari, or Edge) and an active internet connection to access the public URL.  
**Python Version:** Python 3.8 or higher (required for local development/hosting).  
**Required Libraries:** `NumPy` (for core linear algebra computations), `Flask` (to serve the web application), `Flask-CORS` (to handle cross-origin requests), `Gunicorn` (to run the production server on Render).  
**OS Compatibility:** Fully cross-platform (Windows, macOS, Linux, Android, iOS) because it runs in a browser.

##  Installation / Setup
**Cloning the Project:** Download the source files (`app.py`, `index.html`, `requirements.txt`, `Procfile`) from your GitHub repository.  
**Installing Dependencies:**
```bash
pip install -r requirements.txt
Folder Structure:

bash
Copy code
/eigenstuff-calculator
├── app.py           # Backend logic
├── index.html       # Frontend UI
├── requirements.txt # Package list
└── Procfile         # Deployment instructions
 How to Run the Program
Locally:

Open your terminal/command prompt

Navigate to the project folder

Execute the following command:

bash
Copy code
python app.py
Open index.html in your browser

Publicly:

Visit the deployed Render URL: https://eigenstuff-calculator.onrender.com

Startup Behavior:

Upon visiting the site, the Python backend initializes

The frontend automatically generates a default $n \times n$ input grid

 User Interface Guide
Matrix Input Area: A dynamic grid where you can type numbers. Default size: $n \times n$.
Select Size: Use the dropdown menu to change dimensions (up to $5 \times 5$). The grid updates instantly.
Compute Button: A blue button below the grid. Click to send your matrix to the server for calculation.
Results Section: Displays calculated eigenvalues ($\lambda$) and their corresponding basis vectors. Values are rounded to whole numbers for clarity.

Quick Steps:

Enter your values into the white boxes

Press the Compute button

Review the results in the gray boxes at the bottom
**Cloning the Project:**  
Download the source files (`app.py`, `index.html`, `requirements.txt`, `Procfile`) from your GitHub repository.

**Installing Dependencies:**  
```bash
pip install -r requirements.txt
