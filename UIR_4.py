import networkx as nx
import heapq


def heuristic(node, heuristic_values):
    if(heuristic_values == None):
        return 0
    return heuristic_values[node]

def astar(graph, start, end):

    # Priority queue to store nodes to be explored
    open_list = [(0, start)]  # (f_cost, node)
    # Dictionary to store the cost to reach a node, from starting node
    g_costs = {start: 0}
    # Dictionary to store the parent node of each node, to reconstruct path from start to end
    parents = {start: None}

    while open_list:
        # Pop node with lowest f_cost from the priority queue
        current_cost, current_node = heapq.heappop(open_list)

        if current_node == end: #Check if current node is goal node, if yes reconstruct the path
            path = []
            while current_node is not None:
                path.append(current_node)
                current_node = parents[current_node]
            return path[::-1]

        for neighbor in graph.neighbors(current_node):#Explore all neighbors
            #Calculate g_cost from start node to neighbor node
            tentative_g_cost = g_costs[current_node] + graph[current_node][neighbor].get("weight", 1)

            #check if we haven't encountered this neighbor before
            if neighbor not in g_costs or tentative_g_cost < g_costs[neighbor]:
                # Update g_costs and f_costs
                g_costs[neighbor] = tentative_g_cost
                f_cost = tentative_g_cost + heuristic(neighbor, heuristic_values)
                heapq.heappush(open_list, (f_cost, neighbor))
                parents[neighbor] = current_node

    # If no path is found
    return None

def loadGraph(filename):
    graph = nx.Graph()
    fread = open(filename,"r")
    heuristic_values = {}


    fread.readline()
    start = fread.readline().strip('\n')
    fread.readline()
    end = fread.readline().strip('\n')
    fread.readline()

    line = fread.readline().strip('\n')
    while line != "vzdusna vzdalenost od cile:":
        graph.add_node(line[0])
        pairs = line.split(";")[1:]
        for pair in pairs:
            key, value = pair.split("=")
            graph.add_edge(line[0], key, weight=int(value))
        line = fread.readline().strip('\n')
    line = fread.readline().strip('\n')
    while line:
        key, value = line.split("=")
        heuristic_values[key] = int(value)
        line = fread.readline().strip('\n')
    heuristic_values[end] = 0
    return graph, heuristic_values, start, end

if __name__ == "__main__":

    graph, heuristic_values,start,end = loadGraph("cv4_vstup_test.txt")
    path = astar(graph,start,end)
    print(path)
