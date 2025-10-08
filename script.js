
// Fetch buildings and connections from Flask API
let buildings = [];
let connections = [];
let currentPath = null;

async function init() {
    const canvas = document.getElementById('campus-map');
    const ctx = canvas.getContext('2d');
    
    // Fetch data from Flask
    const buildingsRes = await fetch('/api/buildings');
    buildings = await buildingsRes.json();
    
    const connectionsRes = await fetch('/api/connections');
    connections = await connectionsRes.json();
    
    drawMap(ctx);
}

function drawMap(ctx) {
    // Clear canvas
    ctx.clearRect(0, 0, 700, 500);
    
    // Draw connections (paths)
    ctx.strokeStyle = '#ddd';
    ctx.lineWidth = 2;
    connections.forEach(conn => {
        const from = buildings.find(b => b.id === conn.from);
        const to = buildings.find(b => b.id === conn.to);
        if (from && to) {
            ctx.beginPath();
            ctx.moveTo(from.x, from.y);
            ctx.lineTo(to.x, to.y);
            ctx.stroke();
        }
    });
    
    // Highlight path if exists
    if (currentPath) {
        ctx.strokeStyle = '#667eea';
        ctx.lineWidth = 4;
        for (let i = 0; i < currentPath.length - 1; i++) {
            const from = buildings.find(b => b.id === currentPath[i]);
            const to = buildings.find(b => b.id === currentPath[i + 1]);
            if (from && to) {
                ctx.beginPath();
                ctx.moveTo(from.x, from.y);
                ctx.lineTo(to.x, to.y);
                ctx.stroke();
            }
        }
    }
    
    // Draw buildings
    buildings.forEach(building => {
        const isInPath = currentPath && currentPath.includes(building.id);
        ctx.fillStyle = isInPath ? '#667eea' : '#4CAF50';
        ctx.beginPath();
        ctx.arc(building.x, building.y, 8, 0, 2 * Math.PI);
        ctx.fill();
        
        // Draw labels
        ctx.fillStyle = '#333';
        ctx.font = '12px Arial';
        ctx.fillText(building.name, building.x + 12, building.y + 4);
    });
}

// Handle path finding
document.getElementById('find-path-btn').addEventListener('click', async () => {
    const start = document.getElementById('start-building').value;
    const end = document.getElementById('end-building').value;
    
    if (!start || !end) {
        alert('Please select both start and end buildings');
        return;
    }
    
    const response = await fetch('/api/find_path', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ start, end })
    });
    
    const data = await response.json();
    
    if (data.error) {
        alert(data.error);
        return;
    }
    
    if (data.path) {
        currentPath = data.path;
        document.getElementById('distance').textContent = data.distance;
        document.getElementById('path').textContent = data.path.map(id => 
            buildings.find(b => b.id === id).name
        ).join(' → ');
        document.getElementById('result').classList.remove('hidden');
    } else {
        alert('No path found');
        currentPath = null;
        document.getElementById('result').classList.add('hidden');
    }
    
    const canvas = document.getElementById('campus-map');
    drawMap(canvas.getContext('2d'));
});

// Initialize on page load
init();
