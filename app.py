from flask import Flask, request, jsonify, render_template, send_file
import cv2
import numpy as np
import base64
from heapq import heappush, heappop
from collections import defaultdict
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/solve', methods=['POST'])
def solve():
    try:
        file = request.files['file']
        img_bytes = file.read()
        nparr = np.frombuffer(img_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_GRAYSCALE)
        _, binary = cv2.threshold(img, 128, 255, cv2.THRESH_BINARY)
        solved = solve_maze(binary.copy())
        
        # Convert the solved maze to a PDF
        pdf_buffer = generate_pdf(solved)
        pdf_buffer.seek(0)
        
        # Encode the solved image for display
        _, buffer = cv2.imencode('.png', solved)
        img_str = base64.b64encode(buffer).decode()
        
        return jsonify({
            'solved_image': img_str,
            'pdf_url': '/download-pdf'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/download-pdf')
def download_pdf():
    try:
        return send_file('solved_maze.pdf', as_attachment=True)
    except Exception as e:
        return str(e), 500

def solve_maze(maze):
    height, width = maze.shape
    start = (1, 1)
    end = (height-2, width-2)
    
    # Initialize distances
    distances = defaultdict(lambda: float('inf'))
    distances[start] = 0
    previous = {}
    
    # Priority queue for Dijkstra's
    pq = [(0, start)]
    visited = set()
    
    while pq:
        dist, current = heappop(pq)
        
        if current == end:
            break
            
        if current in visited:
            continue
            
        visited.add(current)
        x, y = current
        
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            nx, ny = x + dx, y + dy
            neighbor = (nx, ny)
            
            if (0 <= nx < height and 0 <= ny < width and 
                maze[nx, ny] == 255 and neighbor not in visited):
                
                new_dist = dist + 1
                if new_dist < distances[neighbor]:
                    distances[neighbor] = new_dist
                    previous[neighbor] = current
                    heappush(pq, (new_dist, neighbor))
    
    # Reconstruct and highlight the path in red
    if end in previous:
        current = end
        while current in previous:
            x, y = current
            maze[x, y] = 50  # Mark path in red
            current = previous[current]
        maze[1, 1] = 50  # Mark start
        return maze
    
    raise ValueError("No solution found")

def generate_pdf(maze):
    # Convert the maze to a color image
    maze_color = cv2.cvtColor(maze, cv2.COLOR_GRAY2BGR)
    
    # Highlight the path in red
    maze_color[maze == 50] = [0, 0, 255]  # Red color
    
    # Save the image to a temporary file
    cv2.imwrite('temp_maze.png', maze_color)
    
    # Create a PDF
    pdf_buffer = BytesIO()
    c = canvas.Canvas(pdf_buffer, pagesize=letter)
    c.drawImage('temp_maze.png', 50, 50, width=500, height=500)
    c.save()
    
    # Save the PDF to a file
    with open('solved_maze.pdf', 'wb') as f:
        f.write(pdf_buffer.getvalue())
    
    return pdf_buffer

if __name__ == '__main__':
    app.run(debug=True)