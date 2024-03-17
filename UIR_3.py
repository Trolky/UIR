class Node:
    def __init__(self, state):
        self.state = state
        self.parent = None
        self.left = None
        self.right = None



def depth_first_search(root):
    stack = [root]
    visited = set()
    while stack:
        node = stack.pop()
        if node.state == ((), (), (3, 2, 1)):
            return node
        visited.add(node.state)
        children = generate_children(node,visited)
        for child in children:
            if child.state not in visited:
                visited.add(child.state)
                stack.append(child)
    return None
def generate_children(parent, visited_states):
    children = []
    possible_moves = hanoi_possible_moves(parent.state)
    for move in possible_moves:
        if move not in visited_states:
            child_state = apply_move(parent.state, move)
            child_node = Node(child_state)
            child_node.parent = parent

            if parent.left is None:
                parent.left = child_node
            elif parent.left is not None:
                parent.right = child_node

            children.append(child_node)
    return children

def breadth_first_search(root):
    queue = [root]
    visited = set()
    while queue:
        node = queue.pop(0)
        if node.state == ((), (), (3, 2, 1)):
            return node
        visited.add(node.state)
        children = generate_children(node, visited)
        for child in children:
            if child.state not in visited:
                visited.add(child.state)
                queue.append(child)
    return None



def hanoi_possible_moves(state):
    num_rods = len(state)
    possible_moves = []

    for source in range(num_rods):
        for dest in range(num_rods):
            if source != dest and is_valid_move(state[source], state[dest]):
                possible_moves.append((source, dest))

    return possible_moves


def apply_move(state, move):
    source, dest = move
    new_state = [list(rod) for rod in state] #copy current state
    disk = new_state[source].pop() #removes top disk
    new_state[dest].append(disk) #append disk on new rod
    return tuple(tuple(rod) for rod in new_state) #converts to tuple



# Check if move is valid
def is_valid_move(source, dest):
    if not source:
        return False
    elif not dest:
        return True
    else:
        return source[-1] < dest[-1]  # Only smaller disks can be placed on larger ones

if __name__ == "__main__":
    states_path = []
    initial_state = ((3,2,1), (), ())
    root = Node(initial_state)
    moves = hanoi_possible_moves(initial_state)
    dfs_result = depth_first_search(root)

    print("DFS: ")
    while dfs_result.parent is not None:
        states_path.append(dfs_result.state)
        dfs_result = dfs_result.parent
    states_path = reversed(states_path)
    print(initial_state)
    for i in states_path:
        print(i)

    print("\nBFS: ")
    root_bfs = Node(initial_state)
    bfs_result = breadth_first_search(root_bfs)
    states_path_bfs = []
    while bfs_result.parent is not None:
        states_path_bfs.append(bfs_result.state)
        bfs_result = bfs_result.parent
    states_path_bfs = reversed(states_path_bfs)
    print(initial_state)
    for i in states_path_bfs:
        print(i)

