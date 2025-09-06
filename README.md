🌀 Maze Solver using BFS (Flask Web App)
📌 Overview

This project is a web-based maze-solving application built with Python Flask.
It uses the Breadth-First Search (BFS) algorithm to compute the shortest path in a maze.
The app allows users to upload or generate maze inputs and then visualizes the traversal process step by step, highlighting the final shortest path.

🎯 Features

✅ Upload maze dataset or use sample mazes

✅ Implements BFS algorithm for shortest path

✅ Real-time visualization of traversal & solution

✅ Flask-based web interface for user interaction

✅ Extensible for AI/robotics navigation use cases

🛠️ Tech Stack

Backend: Python, Flask

Algorithm: Breadth-First Search (BFS)

Libraries: NumPy, Matplotlib

Frontend: HTML, CSS (Flask templates)

Dataset: Kaggle Maze Dataset

📂 Project Structure
maze-solver-flask/
│── static/              # CSS, JS, images
│── templates/           # HTML templates
│── app.py               # Main Flask application
│── bfs_solver.py        # BFS algorithm implementation
│── utils.py             # Helper functions
│── requirements.txt     # Dependencies
│── README.md            # Project documentation

🚀 Installation & Usage

Clone the repository:

git clone https://github.com/your-username/maze-solver-flask.git
cd maze-solver-flask


Create a virtual environment & activate:

python -m venv venv
source venv/bin/activate   # On Linux/Mac
venv\Scripts\activate      # On Windows


Install dependencies:

pip install -r requirements.txt


Run the Flask app:

python app.py


Open in browser:

http://127.0.0.1:5000/

🔮 Future Improvements

Support for DFS / A algorithms*

Deploy app on Heroku / Render / Vercel

Interactive maze editor inside the UI

Multi-agent pathfinding support