# Collaborative GIS Map

## Setup Instructions
1. Install dependencies: `pip install Flask Flask-SocketIO shapely pyproj`.
2. Start the Flask server: `python app.py`.
3. Open `map.html` to view the frontend in a browser.

## Technical Decisions
- **Flask-SocketIO** was chosen for WebSocket support with Flask.
- **Leaflet.js** allows easy integration of map layers and drawing tools.

## Known Limitations
- Accuracy of area calculations may vary due to projection differences.
- Real-time updates are optimized for small-scale use because it's run on local.

## Future Improvements
- Enhance error handling and user session management.
- Improve layer-switching smoothness with optimized transformations.



