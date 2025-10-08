from flask import Flask, render_template, request, jsonify
import subprocess
import os

app = Flask(__name__)

BUILDINGS = [
    {"id": "Library", "name": "Library", "x": 150, "y": 100},
    {"id": "StudentCenter", "name": "Student Center", "x": 300, "y": 120},
    {"id": "EngineeringBuilding", "name": "Engineering Building", "x": 150, "y": 250},
    {"id": "ScienceHall", "name": "Science Hall", "x": 350, "y": 200},
    {"id": "AdminOffice", "name": "Administration Office", "x": 250, "y": 350},
    {"id": "Cafeteria", "name": "Cafeteria", "x": 450, "y": 180},
    {"id": "Gymnasium", "name": "Gymnasium", "x": 450, "y": 300},
    {"id": "DormA", "name": "Dormitory A", "x": 550, "y": 380},
    {"id": "DormB", "name": "Dormitory B", "x": 550, "y": 450},
    {"id": "MainGate", "name": "Main Gate", "x": 450, "y": 500}
]

CONNECTIONS = [
    {"from": "Library", "to": "StudentCenter", "weight": 150},
    {"from": "Library", "to": "EngineeringBuilding", "weight": 200},
    {"from": "StudentCenter", "to": "ScienceHall", "weight": 100},
    {"from": "StudentCenter", "to": "Cafeteria", "weight": 80},
    {"from": "EngineeringBuilding", "to": "ScienceHall", "weight": 120},
    {"from": "EngineeringBuilding", "to": "AdminOffice", "weight": 180},
    {"from": "ScienceHall", "to": "AdminOffice", "weight": 90},
    {"from": "ScienceHall", "to": "Gymnasium", "weight": 200},
    {"from": "AdminOffice", "to": "Cafeteria", "weight": 150},
    {"from": "Cafeteria", "to": "Gymnasium", "weight": 100},
    {"from": "Gymnasium", "to": "DormA", "weight": 130},
    {"from": "Gymnasium", "to": "DormB", "weight": 140},
    {"from": "DormA", "to": "MainGate", "weight": 160},
    {"from": "DormB", "to": "MainGate", "weight": 150},
    {"from": "StudentCenter", "to": "MainGate", "weight": 300}
]

@app.route('/')
def index():
    return render_template('index.html', buildings=BUILDINGS)

@app.route('/api/buildings')
def get_buildings():
    return jsonify(BUILDINGS)

@app.route('/api/connections')
def get_connections():
    return jsonify(CONNECTIONS)

@app.route('/api/find_path', methods=['POST'])
def find_path():
    if not request.is_json:
        return jsonify({"error": "Content-Type must be application/json"}), 400
    
    data = request.json
    if not data:
        return jsonify({"error": "Invalid JSON payload"}), 400
    
    start = data.get('start')
    end = data.get('end')
    
    if not start or not end:
        return jsonify({"error": "Missing start or end building"}), 400
    
    if not os.path.exists('./pathfinder'):
        return jsonify({"error": "Pathfinder executable not found. Please compile pathfinder.c first."}), 500
    
    try:
        result = subprocess.run(
            ['./pathfinder', 'campus_graph.txt', start, end],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        if result.returncode != 0:
            return jsonify({"error": "Pathfinding failed", "details": result.stderr}), 500
        
        output_lines = result.stdout.strip().split('\n')
        
        if output_lines[0] == "NO_PATH":
            return jsonify({"path": None, "distance": None})
        
        distance = int(output_lines[0])
        path = output_lines[1].split(',')
        
        return jsonify({
            "path": path,
            "distance": distance
        })
    
    except subprocess.TimeoutExpired:
        return jsonify({"error": "Pathfinding timeout"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
