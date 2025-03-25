import networkx as nx
import csv
import os

def read_gr_file(filepath):
    """Parses a .gr file into a NetworkX DiGraph"""
    G = nx.DiGraph()
    with open(filepath, 'r') as file:
        for line in file:
            if line.startswith('a'):
                _, tail, head, weight = line.strip().split()
                G.add_edge(tail, head, weight=float(weight))
    return G

def solve_dijkstra(graph, source='1'):
    """Solves single-source shortest paths using Dijkstra's algorithm"""
    distances, predecessors = nx.single_source_dijkstra(graph, source=source)
    return distances, predecessors

def write_results_to_csv(output_path, distances, predecessors):
    """Writes the results to a CSV file"""
    with open(output_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Node', 'Distance', 'Predecessor'])
        for node in sorted(distances, key=lambda x: int(x)):
            pred = predecessors.get(node, None)
            writer.writerow([node, distances[node], pred])

def process_all_graphs(input_dir, output_dir):
    """Processes all .gr files in input_dir and writes results to output_dir"""
    os.makedirs(output_dir, exist_ok=True)

    for filename in os.listdir(input_dir):
        if filename.endswith('.gr'):
            print(f"Processing {filename}...")
            input_path = os.path.join(input_dir, filename)
            graph = read_gr_file(input_path)
            distances, predecessors = solve_dijkstra(graph, source='1')
            output_filename = filename.replace('.gr', '_dijkstra_results.csv')
            output_path = os.path.join(output_dir, output_filename)
            write_results_to_csv(output_path, distances, predecessors)
            print(f"Results saved to {output_path}")

# Example usage
if __name__ == "__main__":
    input_dir = 'data'       # Folder with .gr files
    output_dir = 'results'     # Where to save the output .csv files
    process_all_graphs(input_dir, output_dir)
