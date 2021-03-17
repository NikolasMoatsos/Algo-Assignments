import argparse,sys
from collections import deque 

# This creates the graph form a given file.
def CreateGraph(input_filename):
    g = {}
    with open(input_filename) as graph_input:
        for line in graph_input:
            nodes = [int(x) for x in line.split()]
            if nodes[0] not in g:
                g[nodes[0]] = []
            if nodes[1] not in g:
                g[nodes[1]] = []
            g[nodes[0]].append(nodes[1])
            g[nodes[1]].append(nodes[0])
    return g

# This removes a node from the graph.
def RemoveFromGraph(node,g):
    for i in g[node]:
        g[i].remove(node)
    del g[node]
    return g 

# This computes every nodes grade.
def ComputeAdjencieSum(g):
    nodes_sum = {i : len(g[i]) for i in g}
    return nodes_sum       

# This adjusts the grades when a node has been removed.
def AdjustSum(node,nodes_sum,g):
    del nodes_sum[node]
    for i in g[node]:
        nodes_sum[i] -= 1
    return nodes_sum

# This adjust the influence when a node has been removed
def AdjustInfluence(node,change_nodes,nodes_sum,nodes_influence,g):
    del nodes_influence[node]
    for i in change_nodes:
        nodes_influence[i] = ComputeInfluence(i,nodes_sum,g)
    return nodes_influence

# This finds the nodes of thita ball and ball.
def BallNodes(node,radius,thita,g):
    q = deque()
    inqueue = {i: False for i in g}
    visited = {i: False for i in g}
    q.appendleft(node)
    inqueue[node] = True
    r = 0
    last_neighbor = q[0]
    if not thita:
        all_nodes = []
    while r < radius:
        c = q.pop()
        inqueue[c] = False
        visited[c] =True
        for j in g[c]:
            if not visited[j] and not inqueue[j]:
                q.appendleft(j)
                if not thita:
                    all_nodes.append(j)
                inqueue[j] = True
        if len(q) == 0:
            break
        # If the last node of the checking radius has been checked, increase radius.
        elif c == last_neighbor:
            r +=1
            last_neighbor = q[0]
    if thita:
        return q
    else:    
        return all_nodes            

# This computes the influence of a node.
def ComputeInfluence(node,nodes_sum,g):
    ball_nodes = BallNodes(node,radius,True,g)
    ball_sum = 0
    for i in ball_nodes:
        ball_sum += nodes_sum[i] - 1
    influence = (nodes_sum[node] - 1) * ball_sum
    return influence 

# This computes the influence for all the nodes of a graph.
def NodesInfluence(nodes_sum,g):
    nodes_influence = {}
    for i in g:
        nodes_influence[i] = ComputeInfluence(i,nodes_sum,g)
    return nodes_influence 

# This finds the smallest key with the max value. 
def FindMax(max,dict):
    max_key = sys.maxsize
    for i in dict:
        if dict[i] == max and i < max_key:
            max_key = i
    return max_key

# Algorithm A
def Algorith_A():
    # Graph for the algorithm.
    g = CreateGraph(input_filename)
    # Compute the grades.
    nodes_sum = ComputeAdjencieSum(g)
    for n in range (num_nodes):
        # Find the node to be removed.
        max_node = FindMax(max(nodes_sum.values()),nodes_sum)
        print(max_node, nodes_sum[max_node])
        # Adjust the grades.
        nodes_sum = AdjustSum(max_node,nodes_sum,g)
        # Adjust the graph
        g = RemoveFromGraph(max_node,g)

# Algorithm B
def Algorith_B():
    # Graph for the algorithm.
    g = CreateGraph(input_filename)
    # Compute the grades and then the influences.
    nodes_sum = ComputeAdjencieSum(g)
    nodes_influence = NodesInfluence(nodes_sum,g)
    for n in range (num_nodes):
        # Find the node to be removed.
        max_node =  FindMax(max(nodes_influence.values()),nodes_influence)
        print(max_node, nodes_influence[max_node])
        # Adjust the grades.
        nodes_sum = AdjustSum(max_node,nodes_sum,g)
        # Find the nodes to adjust their influence.
        change_nodes = BallNodes(max_node,radius + 1,False,g)
        # Adjust the graph
        g = RemoveFromGraph(max_node,g)
        # Adjust the influences.
        nodes_influence = AdjustInfluence(max_node,change_nodes,nodes_sum,nodes_influence,g)

# Parse command line arguments.
parser = argparse.ArgumentParser()
parser.add_argument("num_nodes", type=int,
                    help="number of nodes need to be removed")
parser.add_argument("input_filename",help="name of the input file")
parser.add_argument("-c", help="do algorithm 1",
                    action="store_true")
parser.add_argument("-r", type=int, help="do algorithm 2")               
args = parser.parse_args()
num_nodes = args.num_nodes
input_filename = args.input_filename
# Execute algorithm 1.
if args.c:
    Algorith_A()
# Execute algorithm 2.
if args.r:
    radius = args.r
    Algorith_B()