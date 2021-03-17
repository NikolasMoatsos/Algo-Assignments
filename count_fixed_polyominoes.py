import sys,pprint

# The class with the "different polyomino" counter.
class Counter:
    def __init__(self):
        self.count = 0
    # Methods for add and return.
    def AddOne(self):
        self.count += 1
    def ValueOf(self):
        return self.count

# This checks if "i" is a neighbor of the parts of "p", except "u".
def Neighbors(i,p): 
    f = False
    for j in p[:-1]:
        if i in g[j]:
            f = True
            break
    return f

# The method with the algorithm for the count of fixed polyominoes.
def CountFixedPolyominoes(g,untried,n,p,c):
    while untried:
        u = untried.pop()
        p.append(u)
        if len(p) == n:
            c.AddOne()
        else:
            new_neighbors = []
            for i in g[u]:
                if i not in untried and i not in p and  not Neighbors(i,p) :
                        new_neighbors.append(i)
            new_untried = []
            new_untried.extend(untried)
            new_untried.extend(new_neighbors)
            CountFixedPolyominoes(g,new_untried,n,p,c)
        p.remove(u)
    return c.ValueOf()

# This creates the graph.
def CreateGraph(n):
    g = {}
    for x in range(-(n - 2),n):
        for y in range(0,n):
            if (abs(x) + abs(y)) < n:
                if (y > 0 or (y == 0 and x >= 0)):
                    g[(x,y)] = []
                    # Check and append the neighbors of each node.
                    if (abs(x+1) + abs(y)) < n and (y > 0 or (y == 0 and x+1 >= 0)):
                        g[(x,y)].append((x+1,y))
                    if (abs(x) + abs(y+1)) < n and (y+1 > 0 or (y+1 == 0 and x >= 0)):
                        g[(x,y)].append((x,y+1))
                    if (abs(x-1) + abs(y)) < n and (y > 0 or (y == 0 and x-1 >= 0)):
                        g[(x,y)].append((x-1,y))
                    if (abs(x) + abs(y-1)) < n and (y-1 > 0 or (y-1 == 0 and x >= 0)):
                        g[(x,y)].append((x,y-1))
            else:
                break
    return g

print_g = False
# Check the command line arguments.
if sys.argv[1] == "-p":
    print_g = True
    n = int(sys.argv[2])
else:
    n = int(sys.argv[1])
# Create the graph.
g = CreateGraph(n)
# Check and print the graph.
if print_g:
    pprint.pprint(g)
# Initialize the parameters of the algorithm.
untried = [(0,0)]
p = []
c = Counter()
# Run the algorithm and print the result.
print(CountFixedPolyominoes(g,untried,n,p,c))