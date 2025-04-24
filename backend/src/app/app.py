from flask import Flask, render_template, request, jsonify
import networkx as nx
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import io
import base64
import json

class CairoTransportationGraph:
    # The full class implementation from before goes here
    # I've abbreviated it to focus on the Flask integration
    def __init__(self):
        self.nodes = {}
        self.existing_roads = []
        self.potential_roads = []
        self.metro_lines = []
        self.bus_routes = []
        self.traffic_data = {}
        self.transport_demand = {}
        
    def load_from_csv(self, neighborhoods_file, facilities_file, existing_roads_file, 
                      potential_roads_file, traffic_file, metro_file, bus_file, demand_file):
        """Load all data from CSV files"""
        try:
            # Load neighborhood data
            neighborhoods_df = pd.read_csv(neighborhoods_file)
            for _, row in neighborhoods_df.iterrows():
                self.nodes[row['id']] = {
                    'name': row['name'],
                    'type': row['type'],
                    'x': row['x'],
                    'y': row['y'],
                    'population': row['population'],
                    'is_facility': False
                }
            
            # Load facilities data
            facilities_df = pd.read_csv(facilities_file)
            for _, row in facilities_df.iterrows():
                self.nodes[row['id']] = {
                    'name': row['name'],
                    'type': row['type'],
                    'x': row['x'],
                    'y': row['y'],
                    'is_facility': True
                }
            
            # Load existing roads data
            roads_df = pd.read_csv(existing_roads_file)
            for _, row in roads_df.iterrows():
                self.existing_roads.append((
                    row['from_id'],
                    row['to_id'],
                    row['distance_km'],
                    row['capacity'],
                    row['condition']
                ))
            
            # Load potential roads data
            potential_df = pd.read_csv(potential_roads_file)
            for _, row in potential_df.iterrows():
                self.potential_roads.append((
                    row['from_id'],
                    row['to_id'],
                    row['distance_km'],
                    row['capacity'],
                    row['construction_cost']
                ))
            
            # Load traffic data
            traffic_df = pd.read_csv(traffic_file)
            for _, row in traffic_df.iterrows():
                road_key = (row['from_id'], row['to_id'])
                if road_key not in self.traffic_data:
                    self.traffic_data[road_key] = {}
                self.traffic_data[road_key][row['time_of_day']] = row['volume']
            
            # Load metro lines data
            metro_df = pd.read_csv(metro_file)
            for _, row in metro_df.iterrows():
                self.metro_lines.append((
                    row['line_id'],
                    row['from_id'],
                    row['to_id'],
                    row['travel_time_minutes']
                ))
            
            # Load bus routes data
            bus_df = pd.read_csv(bus_file)
            for _, row in bus_df.iterrows():
                self.bus_routes.append((
                    row['route_id'],
                    row['from_id'],
                    row['to_id'],
                    row['travel_time_minutes']
                ))
            
            # Load transport demand data
            demand_df = pd.read_csv(demand_file)
            for _, row in demand_df.iterrows():
                demand_key = (row['from_id'], row['to_id'])
                self.transport_demand[demand_key] = row['daily_trips']
            
            print(f"Successfully loaded data with {len(self.nodes)} nodes and {len(self.existing_roads)} existing roads.")
        except Exception as e:
            print(f"Error loading data: {e}")
        
    # All other methods from before go here
    
    def get_graph_image_base64(self, include_potential=False):
        """Return the graph visualization as a base64 encoded image"""
        plt.figure(figsize=(12, 10))
        G = self.build_networkx_graph(include_potential)
        
        # Create visualization (similar to visualize() method)
        pos = {node: (self.nodes[node]['x'], self.nodes[node]['y']) for node in G.nodes()}
        
        # Draw nodes with different colors (abbreviated code)
        residential = [n for n in G.nodes() if not self.nodes[n]['is_facility'] and self.nodes[n]['type'] == 'Residential']
        business = [n for n in G.nodes() if not self.nodes[n]['is_facility'] and self.nodes[n]['type'] == 'Business']
        mixed = [n for n in G.nodes() if not self.nodes[n]['is_facility'] and self.nodes[n]['type'] == 'Mixed']
        other_districts = [n for n in G.nodes() if not self.nodes[n]['is_facility'] and self.nodes[n]['type'] not in ['Residential', 'Business', 'Mixed']]
        facilities = [n for n in G.nodes() if self.nodes[n]['is_facility']]
        
        nx.draw_networkx_nodes(G, pos, nodelist=residential, node_color='green', node_size=300, label='Residential')
        nx.draw_networkx_nodes(G, pos, nodelist=business, node_color='red', node_size=300, label='Business')
        nx.draw_networkx_nodes(G, pos, nodelist=mixed, node_color='purple', node_size=300, label='Mixed')
        nx.draw_networkx_nodes(G, pos, nodelist=other_districts, node_color='gray', node_size=300, label='Other Districts')
        nx.draw_networkx_nodes(G, pos, nodelist=facilities, node_color='blue', node_size=200, label='Facilities', node_shape='s')
        
        # Draw existing edges
        existing_edges = [(u, v) for u, v, d in G.edges(data=True) if d['type'] == 'existing']
        nx.draw_networkx_edges(G, pos, edgelist=existing_edges, width=1.5)
        
        # Draw potential edges if requested
        if include_potential:
            potential_edges = [(u, v) for u, v, d in G.edges(data=True) if d['type'] == 'potential']
            nx.draw_networkx_edges(G, pos, edgelist=potential_edges, width=1.5, edge_color='red', style='dashed')
        
        # Add labels
        labels = {node: node for node in G.nodes()}
        nx.draw_networkx_labels(G, pos, labels, font_size=8)
        
        plt.title('Greater Cairo Transportation Network')
        plt.legend()
        plt.axis('off')
        plt.tight_layout()
        
        # Save plot to a bytes buffer and convert to base64 for HTML embedding
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
        plt.close()
        
        return image_base64
    
    def get_all_nodes_json(self):
        """Return all nodes as JSON for the frontend"""
        return {
            node_id: {
                'name': data['name'],
                'type': data['type'],
                'x': data['x'],
                'y': data['y'],
                'population': data.get('population', 0),
                'is_facility': data['is_facility']
            } for node_id, data in self.nodes.items()
        }
    
    def get_all_edges_json(self, include_potential=False):
        """Return all edges as JSON for the frontend"""
        edges = []
        
        # Add existing roads
        for from_id, to_id, distance, capacity, condition in self.existing_roads:
            edges.append({
                'from': from_id,
                'to': to_id,
                'distance': distance,
                'capacity': capacity,
                'condition': condition,
                'type': 'existing'
            })
        
        # Add potential roads if requested
        if include_potential:
            for from_id, to_id, distance, capacity, cost in self.potential_roads:
                edges.append({
                    'from': from_id,
                    'to': to_id,
                    'distance': distance,
                    'capacity': capacity,
                    'cost': cost,
                    'type': 'potential'
                })
        
        return edges

# Initialize Flask application
app = Flask(__name__)

# Create and load the graph (do this at startup)
cairo_graph = CairoTransportationGraph()

@app.route('/')
def index():
    """Render the main page"""
    # Get the graph visualization
    include_potential = request.args.get('potential', 'false').lower() == 'true'
    graph_image = cairo_graph.get_graph_image_base64(include_potential=include_potential)
    
    # Get all node names for the dropdown selection
    node_options = []
    for node_id, data in cairo_graph.nodes.items():
        node_options.append({
            'id': node_id,
            'name': data['name'],
            'type': data['type']
        })
    
    return render_template('index.html', 
                           graph_image=graph_image, 
                           node_options=sorted(node_options, key=lambda x: x['name']))

@app.route('/find_path', methods=['POST'])
def find_path():
    """API endpoint to find paths between locations"""
    data = request.get_json()
    start_id = data.get('start_id')
    end_id = data.get('end_id')
    mode = data.get('mode', 'distance')  # 'distance' or 'time'
    time_of_day = data.get('time_of_day', 'morning')
    
    if mode == 'distance':
        path_result = cairo_graph.find_shortest_path(start_id, end_id)
    else:  # time-based
        path_result = cairo_graph.compute_travel_time(start_id, end_id, time_of_day=time_of_day)
    
    if path_result:
        return jsonify({
            'success': True,
            'path': path_result['path'],
            'path_names': path_result['path_names'],
            'distance': path_result.get('distance', path_result.get('total_distance_km')),
            'time': path_result.get('total_time_minutes', None)
        })
    else:
        return jsonify({
            'success': False,
            'message': 'No path found between these locations'
        })

@app.route('/traffic_analysis')
def traffic_analysis():
    """API endpoint for traffic congestion analysis"""
    time_of_day = request.args.get('time', 'morning')
    congestion = cairo_graph.analyze_traffic_congestion(time_of_day=time_of_day)
    
    # Format results for the frontend
    results = []
    for (from_id, to_id), ratio in congestion.items():
        from_name = cairo_graph.nodes[from_id]['name']
        to_name = cairo_graph.nodes[to_id]['name']
        congestion_level = "High" if ratio > 0.8 else "Medium" if ratio > 0.5 else "Low"
        
        results.append({
            'from_id': from_id,
            'to_id': to_id,
            'from_name': from_name,
            'to_name': to_name,
            'ratio': ratio,
            'level': congestion_level
        })
    
    return jsonify({
        'success': True,
        'time_of_day': time_of_day,
        'results': sorted(results, key=lambda x: x['ratio'], reverse=True)
    })

@app.route('/transport_suggestions')
def transport_suggestions():
    """API endpoint for public transport improvement suggestions"""
    suggestions = cairo_graph.suggest_public_transport_improvements()
    return jsonify({
        'success': True,
        'suggestions': suggestions
    })

@app.route('/graph_data')
def graph_data():
    """Return graph data in JSON format for interactive frontend visualization"""
    include_potential = request.args.get('potential', 'false').lower() == 'true'
    
    return jsonify({
        'nodes': cairo_graph.get_all_nodes_json(),
        'edges': cairo_graph.get_all_edges_json(include_potential)
    })

# Example HTML template (index.html) - would be placed in a templates folder
@app.route('/get_template')
def get_template():
    """This is just to show the template content, not for actual use"""
    template = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Cairo Transportation Network</title>
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css">
        <style>
            #map-container {
                border: 1px solid #ddd;
                margin-bottom: 20px;
            }
            .results-container {
                max-height: 400px;
                overflow-y: auto;
                border: 1px solid #ddd;
                padding: 15px;
                margin-bottom: 20px;
            }
        </style>
    </head>
    <body>
        <div class="container mt-4">
            <h1>Cairo Transportation Network</h1>
            
            <div class="row">
                <div class="col-md-8">
                    <div id="map-container">
                        <img src="data:image/png;base64,{{ graph_image }}" class="img-fluid" alt="Cairo Transportation Network">
                    </div>
                    
                    <div class="form-check mb-3">
                        <input class="form-check-input" type="checkbox" id="show-potential" 
                            {% if request.args.get('potential') == 'true' %}checked{% endif %}>
                        <label class="form-check-label" for="show-potential">
                            Show Potential Future Roads
                        </label>
                    </div>
                </div>
                
                <div class="col-md-4">
                    <div class="card mb-4">
                        <div class="card-header">
                            Find Route
                        </div>
                        <div class="card-body">
                            <form id="path-form">
                                <div class="mb-3">
                                    <label for="start-location" class="form-label">Start Location</label>
                                    <select class="form-select" id="start-location" required>
                                        <option value="">Select location...</option>
                                        {% for node in node_options %}
                                        <option value="{{ node.id }}">{{ node.name }} ({{ node.type }})</option>
                                        {% endfor %}
                                    </select>
                                </div>
                                
                                <div class="mb-3">
                                    <label for="end-location" class="form-label">End Location</label>
                                    <select class="form-select" id="end-location" required>
                                        <option value="">Select location...</option>
                                        {% for node in node_options %}
                                        <option value="{{ node.id }}">{{ node.name }} ({{ node.type }})</option>
                                        {% endfor %}
                                    </select>
                                </div>
                                
                                <div class="mb-3">
                                    <label class="form-label">Route Type</label>
                                    <div class="form-check">
                                        <input class="form-check-input" type="radio" name="route-type" id="shortest-distance" value="distance" checked>
                                        <label class="form-check-label" for="shortest-distance">
                                            Shortest Distance
                                        </label>
                                    </div>
                                    <div class="form-check">
                                        <input class="form-check-input" type="radio" name="route-type" id="fastest-time" value="time">
                                        <label class="form-check-label" for="fastest-time">
                                            Fastest Time
                                        </label>
                                    </div>
                                </div>
                                
                                <div class="mb-3" id="time-of-day-container" style="display:none;">
                                    <label for="time-of-day" class="form-label">Time of Day</label>
                                    <select class="form-select" id="time-of-day">
                                        <option value="morning">Morning Peak</option>
                                        <option value="afternoon">Afternoon</option>
                                        <option value="evening">Evening Peak</option>
                                        <option value="night">Night</option>
                                    </select>
                                </div>
                                
                                <button type="submit" class="btn btn-primary">Find Route</button>
                            </form>
                        </div>
                    </div>
                    
                    <div class="card mb-4">
                        <div class="card-header">
                            Analysis Tools
                        </div>
                        <div class="card-body">
                            <div class="d-grid gap-2">
                                <button id="traffic-analysis-btn" class="btn btn-outline-primary">Traffic Analysis</button>
                                <button id="transport-suggestions-btn" class="btn btn-outline-primary">Transport Suggestions</button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="row mt-4">
                <div class="col-12">
                    <div class="results-container" id="results-container">
                        <p class="text-muted">Select options above to see results here.</p>
                    </div>
                </div>
            </div>
        </div>
        
        <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
        <script>
            $(document).ready(function() {
                // Show/hide time of day selector
                $('input[name="route-type"]').change(function() {
                    if ($(this).val() === 'time') {
                        $('#time-of-day-container').show();
                    } else {
                        $('#time-of-day-container').hide();
                    }
                });
                
                // Show potential roads checkbox
                $('#show-potential').change(function() {
                    const checked = $(this).is(':checked');
                    window.location.href = '/?potential=' + checked;
                });
                
                // Find path form submission
                $('#path-form').submit(function(e) {
                    e.preventDefault();
                    const startId = $('#start-location').val();
                    const endId = $('#end-location').val();
                    const mode = $('input[name="route-type"]:checked').val();
                    const timeOfDay = $('#time-of-day').val();
                    
                    $.ajax({
                        url: '/find_path',
                        method: 'POST',
                        contentType: 'application/json',
                        data: JSON.stringify({
                            start_id: startId,
                            end_id: endId,
                            mode: mode,
                            time_of_day: timeOfDay
                        }),
                        success: function(response) {
                            if (response.success) {
                                let resultsHtml = '<h4>Route Found</h4>';
                                resultsHtml += '<p>From <strong>' + response.path_names[0] + '</strong> to <strong>' + 
                                              response.path_names[response.path_names.length - 1] + '</strong></p>';
                                
                                resultsHtml += '<p><strong>Path:</strong> ' + response.path_names.join(' → ') + '</p>';
                                resultsHtml += '<p><strong>Total Distance:</strong> ' + response.distance.toFixed(1) + ' km</p>';
                                
                                if (response.time !== null) {
                                    resultsHtml += '<p><strong>Estimated Travel Time:</strong> ' + response.time.toFixed(1) + ' minutes</p>';
                                }
                                
                                $('#results-container').html(resultsHtml);
                            } else {
                                $('#results-container').html('<div class="alert alert-warning">' + response.message + '</div>');
                            }
                        },
                        error: function() {
                            $('#results-container').html('<div class="alert alert-danger">Error finding route. Please try again.</div>');
                        }
                    });
                });
                
                // Traffic analysis button
                $('#traffic-analysis-btn').click(function() {
                    const timeOfDay = $('#time-of-day').val() || 'morning';
                    
                    $.ajax({
                        url: '/traffic_analysis',
                        method: 'GET',
                        data: {
                            time: timeOfDay
                        },
                        success: function(response) {
                            if (response.success) {
                                let resultsHtml = '<h4>Traffic Congestion Analysis - ' + 
                                    timeOfDay.charAt(0).toUpperCase() + timeOfDay.slice(1) + '</h4>';
                                
                                resultsHtml += '<table class="table table-striped">';
                                resultsHtml += '<thead><tr><th>From</th><th>To</th><th>Congestion Level</th><th>Ratio</th></tr></thead>';
                                resultsHtml += '<tbody>';
                                
                                response.results.forEach(function(item) {
                                    let rowClass = '';
                                    if (item.level === 'High') rowClass = 'table-danger';
                                    else if (item.level === 'Medium') rowClass = 'table-warning';
                                    
                                    resultsHtml += '<tr class="' + rowClass + '">';
                                    resultsHtml += '<td>' + item.from_name + '</td>';
                                    resultsHtml += '<td>' + item.to_name + '</td>';
                                    resultsHtml += '<td>' + item.level + '</td>';
                                    resultsHtml += '<td>' + item.ratio.toFixed(2) + '</td>';
                                    resultsHtml += '</tr>';
                                });
                                
                                resultsHtml += '</tbody></table>';
                                $('#results-container').html(resultsHtml);
                            }
                        },
                        error: function() {
                            $('#results-container').html('<div class="alert alert-danger">Error analyzing traffic. Please try again.</div>');
                        }
                    });
                });
                
                // Transport suggestions button
                $('#transport-suggestions-btn').click(function() {
                    $.ajax({
                        url: '/transport_suggestions',
                        method: 'GET',
                        success: function(response) {
                            if (response.success) {
                                let resultsHtml = '<h4>Public Transport Improvement Suggestions</h4>';
                                
                                if (response.suggestions.length === 0) {
                                    resultsHtml += '<p>No suggestions found - current public transport coverage appears adequate.</p>';
                                } else {
                                    resultsHtml += '<table class="table table-striped">';
                                    resultsHtml += '<thead><tr><th>From</th><th>To</th><th>Daily Demand</th><th>Suggestion</th></tr></thead>';
                                    resultsHtml += '<tbody>';
                                    
                                    response.suggestions.forEach(function(item) {
                                        resultsHtml += '<tr>';
                                        resultsHtml += '<td>' + item.from + '</td>';
                                        resultsHtml += '<td>' + item.to + '</td>';
                                        resultsHtml += '<td>' + item.demand + '</td>';
                                        resultsHtml += '<td>' + item.suggestion + '</td>';
                                        resultsHtml += '</tr>';
                                    });
                                    
                                    resultsHtml += '</tbody></table>';
                                }
                                
                                $('#results-container').html(resultsHtml);
                            }
                        },
                        error: function() {
                            $('#results-container').html('<div class="alert alert-danger">Error getting suggestions. Please try again.</div>');
                        }
                    });
                });
            });
        </script>
    </body>
    </html>
    """
    return template

if __name__ == '__main__':
    # Load your data at startup
    cairo_graph.load_from_csv(
        neighborhoods_file="D:\\IMPORTANT DATA\\AIU Computer Engineering\\CE Year 3\\Semester 2\\CSE112 Design & Analysis of Algorithms\\Project\\backend\data\\Neighborhoods and Districts.csv", 
        facilities_file="data/facilities.csv",
        existing_roads_file="data/existing_roads.csv",
        potential_roads_file="data/potential_roads.csv",
        traffic_file="data/traffic_data.csv",
        metro_file="data/metro_lines.csv",
        bus_file="data/bus_routes.csv",
        demand_file="data/transport_demand.csv"
    )
    
    app.run(debug=True)