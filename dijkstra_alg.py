import networkx as nx
import csv
import os
import matplotlib.pyplot as plt
from scipy import optimize



def read_gr_file(filepath):
    G = nx.DiGraph()
    with open(filepath, 'r') as file:
        for line in file:
            if line.startswith('a'):
                _, tail, head, weight = line.strip().split()
                G.add_edge(tail, head, weight=float(weight))
    return G

def solve_dijkstra(graph, source='1'):
    distances, predecessors = nx.single_source_dijkstra(graph, source=source)
    return distances, predecessors

def results_to_csv(output_path, distances, predecessors):
    with open(output_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Node', 'Distance', 'Predecessor'])
        for node in sorted(distances, key=lambda x: int(x)):
            pred = predecessors.get(node, None)
            writer.writerow([node, distances[node], pred])


def process_all_graphs(input_dir, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    for filename in os.listdir(input_dir):
        if filename.endswith('.gr'):
            print(f"Processing {filename}...")
            input_path = os.path.join(input_dir, filename)
            graph = read_gr_file(input_path)
            distances, predecessors = solve_dijkstra(graph, source='1')
            output_filename = filename.replace('.gr', '_dijkstra_results.csv')
            output_path = os.path.join(output_dir, output_filename)
            results_to_csv(output_path, distances, predecessors)
            print(f"Results saved to {output_path}")

            #TODO: plots commented out: rome99.gr would not plot in a reasonable amount of time
            # plt.figure(figsize=(10, 8))
            # pos = nx.kamada_kawai_layout(graph)  # Save layout to use for drawing
            # edge_labels = nx.get_edge_attributes(graph, 'weight')
            # nx.draw(graph, pos, with_labels=True, node_color='lightblue',
            #         edge_color='gray', node_size=500, font_size=8)
            # nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels, font_size=6)
            # plt.title("Graph Visualization")
            # graph_out_name = filename.replace('.gr', '_graph.png')
            # graph_out_path = os.path.join(output_dir, graph_out_name)
            # plt.savefig(graph_out_path, format='png', dpi=300)
            # plt.close()
            # print(f"Graph image saved to {graph_out_path}")


# Example usage
if __name__ == "__main__":
    input_dir = 'data'
    output_dir = 'results'
    process_all_graphs(input_dir, output_dir)


