# eigenstuff-calculator


# Eigenstuff Calculator 🧮

###  Project Overview
The **Eigenstuff Calculator** is a full-stack web application developed as a specialized Linear Algebra tool to streamline the calculation of eigenvalues and their corresponding eigenspace bases. Designed for academic use, the program solves the characteristic equation $\det(A - \lambda I) = 0$ for any square matrix up to a $5 \times 5$ dimension, providing a user-friendly alternative to tedious manual computations. By integrating a Python-based mathematical engine with a responsive web interface, the application allows students and educators to input matrix values through a dynamic grid and receive instant, accurate results rounded to whole numbers. This tool effectively bridges the gap between complex theoretical concepts and practical computation, making the exploration of linear transformations more accessible.

---

###  System Requirements
* **User Needs:** A modern web browser (Chrome, Firefox, Safari, or Edge) and an active internet connection.
* **Python Version:** Python 3.8 or higher (for local development).
* **Required Libraries:** * `NumPy`: For core linear algebra computations.
    * `Flask`: To serve the web application.
    * `Flask-CORS`: To handle cross-origin requests.
    * `Gunicorn`: To run the production server on Render.
* **OS Compatibility:** Fully cross-platform (Windows, macOS, Linux, Android, iOS) as it is a web-based tool.

---

###  Installation / Setup
To prepare the program for local use:
1. **Clone the Project:** Download the source files (`app.py`, `index.html`, `requirements.txt`, and `Procfile`) from this repository.
2. **Install Dependencies:** Open your terminal in the project folder and run:
   ```bash
   pip install -r requirements.txt
Folder Structure:

app.py: Backend Flask server & mathematical logic.

index.html: Frontend user interface & JavaScript.

requirements.txt: List of Python dependencies.

Procfile: Instructions for cloud deployment.

### How to Run the Program
To run locally:

Open your terminal or command prompt.

Navigate to the project directory.

Execute the command: python app.py

Open the index.html file in your preferred web browser.

To access the live version: Visit the public URL: https://eigenstuff-calculator.onrender.com (Note: If the site takes a moment to load, the free server is simply "waking up").

###  User Interface Guide
Matrix Input Area: A dynamic grid where you can type your numerical values.

Select Size: Click the dropdown menu to choose a matrix size from 2x2 up to 5x5. The grid updates automatically.

Compute Button: Press the blue "Compute" button to send your data to the Python engine.

Output Section: Results appear below the button in gray boxes, showing the calculated Eigenvalues (λ) and the Basis Vectors for each Eigenspace.

Simple Steps: 1. Enter your matrix values. 2. Click the "Compute" button. 3. Review the results displayed at the bottom.
