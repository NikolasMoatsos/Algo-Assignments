from collections import deque
import sys , argparse


def CreateDominoes() :
    u = []
    for i in range(0,10) :
        for j in range(0,i + 1) :
            for n in range(1,7) :
                u.append(((i,j),n))
    return u

def CreateTableau(result,U) :
    v = []
    for i in result :
        if i in U :
            v.append((i,result[i]))
    return v

def FinalResult(result,V) :
    f_result = {}
    for i in result :
        if i in V :
            f_result[i] = result[i]
    return f_result

def DominoeCosts(U,V,greyscale):
    costs = {}
    for u in U :
        for v in V :
            normal = (greyscale[v][0] - u[0][0])**2 + (greyscale[v][1] - u[0][1])**2
            reverse = (greyscale[v][0] - u[0][1])**2 + (greyscale[v][1] - u[0][0])**2
            if reverse < normal :
                costs[(u,v)] = (reverse,True)
                costs[(v,u)] = (reverse,True)

            else :
                costs[(u,v)] = (normal,False)
                costs[(v,u)] = (normal,False)
    return costs

def CreatePortraitGraph() :
    g ={}
    u = []
    for i in range(30) :
        for j in range(22) :
            g[(i,j)] = []
            if (i + j) % 2 == 0 :
                u.append((i,j))
            if i - 1 >= 0 :
                g[(i,j)].append((i -1,j))
            if j - 1 >= 0 :
                g[(i,j)].append((i,j - 1))
            if j + 1 < 22 :
                g[(i,j)].append((i,j + 1))
            if i + 1 < 30 :
                g[(i,j)].append((i+1,j))
    return u,g

def ReadPortraitCosts(g) :
    grey = {}
    greyscale = {}
    c = open(INPUT_FILE, 'r')
    lines = c.readlines()
    i = 0
    for line in lines :
        j = 0
        for col in line.split() :
            grey[(i,j)] = int(col)
            j += 1
        i += 1
    costs = {}
    for i in g :
        for j in g[i] :
            costs[(i,j)] = (grey[i] - grey[j])**2
            greyscale[(i,j)] = (grey[i],grey[j])
    return costs,greyscale


def ReadCosts() :
    U=[]
    V=[]
    costs = {}
    c = open(COSTS_FILE, 'r')
    lines = c.readlines()
    i = 1
    for line in lines :
        U.append((i,0))
        j = 1
        for col in line.split() :
            if i == 1 :
                V.append((0,j))
            costs[i,j] = int(col)
            j += 1 
        i+=1
    return U,V,costs

def CreateGraph(U,V) :
    g = {}
    for i in U :
        g[i] = [v for v in V]
    for i in V :
        g[i] = [u for u in U]
    return g

def AdjustCosts(costs) :
    new_costs = {}
    m = max(costs.values())
    for i in costs :
        new_costs[i] = (-1)*costs[i] + m
    return new_costs

def GetPath(pred,v) :
    path = []
    while v != -1 :
        path.append(v)
        v = pred[v]
    return path

def IsPerfectMatching(matching) :
    perf = True
    for i in matching :
        if matching[i] == None :
            perf = False
            break
    return perf

def FindFirstUnmatched(matching,U) :
    for u in U :
        if matching[u] == None :
            return u

def ComputeDelta(g,odd_nodes,even_nodes,costs,prices,final) :
    min = sys.maxsize
    for u in even_nodes :
        for v in g[u] :
            if v not in odd_nodes :
                if  ASSIGNMENT :
                    c = costs[(u[0],v[1])] - prices[u] - prices[v]
                else :
                    if final :
                        c = costs[(u,v)][0] - prices[u] - prices[v]
                    else :
                        c = costs[(u,v)] - prices[u] - prices[v]
                if c < min :
                    min = c
    return min

def AugmentingPathBFS(g,node,matching,costs,prices,final) :
    q = deque()
    inqueue = {i: False for i in g}
    visited = {i: False for i in g}
    pred = {i: -1 for i in g}
    q.appendleft(node)
    inqueue[node] = True
    q.appendleft(-1)
    level = 0
    even_nodes = set()
    odd_nodes = set()
    while len(q) > 1 :
        c = q.pop()
        if c == -1 :
            level += 1
            c = q.pop()
            q.appendleft(-1)
        inqueue[c] = False
        visited[c] = True
        if level % 2 == 0 :
            next_level_odd = True
            even_nodes.add(c)
        else :
            next_level_odd = False
            odd_nodes.add(c)
        for v in g[c] :
            if not ASSIGNMENT :
                if final :
                    cost = costs[(c,v)][0]
                else :
                    cost = costs[(c,v)]
            else :
                if next_level_odd :
                    cost = costs[(c[0],v[1])]
                else :
                    cost = costs[(v[0],c[1])]
            if not visited[v] and cost == prices[c] + prices[v] :
                if next_level_odd and matching[v] == None :
                    pred[v] = c
                    augmenting_path = GetPath(pred,v)
                    return augmenting_path,odd_nodes,even_nodes  
                if ((next_level_odd and matching[c] != v) or (not next_level_odd and matching[c] == v)) and not inqueue[v] :
                    q.appendleft(v)
                    inqueue[v] = True
                    pred[v] = c
    return None,odd_nodes,even_nodes

def Hungarian(g,costs,final,U) :
    prices = {i: 0 for i in g}
    matching = {i: None for i in g}
    while not IsPerfectMatching(matching) :
        node = FindFirstUnmatched(matching,U)
        augmenting_path,odd_nodes,even_nodes = AugmentingPathBFS(g,node,matching,costs,prices,final)
        if augmenting_path != None :
            i = 0
            while i < len(augmenting_path) - 1 :
                matching[augmenting_path[i]] = augmenting_path[i + 1]
                matching[augmenting_path[i + 1]] = augmenting_path[i]
                i += 2
        else :
            delta = ComputeDelta(g,odd_nodes,even_nodes,costs,prices,final)
            for u in even_nodes :
                prices[u] += delta
            for v in odd_nodes :
                prices[v] -= delta
    return matching

def WriteTilesInFile(result) :
    f = open(TILING_FILE,"w")
    c = 1
    for i in result :
        f.write(str(i[0]))
        f.write(" ")
        f.write(str(i[1]))
        if not c == len(result) :
            f.write("\n")
            c += 1

def WriteDominoesInFile(result,costs) :
    f = open(DOMINOES_FILE,"w")
    c = 1 
    for i in result :
        if costs[(i,result[i])][1] :
            f.write(str(i))
            f.write(" : ")
            f.write(str((result[i][0][1],result[i][0][0])))
            if not c == len(result) :
                f.write("\n")
            c += 1
        else :
            f.write(str(i))
            f.write(" : ")
            f.write(str(result[i][0]))
            if not c == len(result) :
                f.write("\n")
            c += 1

def Portraits() :
    final = False
    U,g = CreatePortraitGraph()
    costs,greyscale = ReadPortraitCosts(g)
    rev_costs = AdjustCosts(costs)
    result = Hungarian(g,rev_costs,final,U)
    sum = 0
    for i in result :
        if i in U :
            sum += costs[(i,result[i])]
    print(sum)
    new_U = CreateDominoes()
    new_V = CreateTableau(result,U)
    WriteTilesInFile(new_V)
    new_g = CreateGraph(new_U,new_V)
    new_costs = DominoeCosts(new_U,new_V,greyscale)
    final = True
    result2 = Hungarian(new_g,new_costs,final,new_U)
    sum = 0
    for i in result2 :
        if i in new_U :
            sum += new_costs[(i,result2[i])][0]
    print(sum)
    f_result = FinalResult(result2,new_V)
    WriteDominoesInFile(f_result,new_costs)

def Examples() :
    final = False
    U,V,costs = ReadCosts()
    g = CreateGraph(U,V)
    if MAXIMIZE :
        new_costs = AdjustCosts(costs)
        result = Hungarian(g,new_costs,final,U)
    else :
        result = Hungarian(g,costs,final,U)
    sum = 0
    c = 1
    for i in result :
        if i in U :
            sum += costs[(i[0],result[i][1])]
            if c != len(result)/2 :
                print(result[i][1] - 1, end=" ")
                c += 1
            else :
                print(result[i][1] - 1)
    print(sum)


parser = argparse.ArgumentParser()
parser.add_argument("-a","--assignment",help="costs file",action= "store_true")
parser.add_argument("-m","--maximize",action='store_true', help="find max cost")
parser.add_argument("input_file",help="input file")
parser.add_argument("-t","--tiling_file",help="test file")
parser.add_argument("-d","--dominoes_file",help="output file")
args = parser.parse_args()
ASSIGNMENT = args.assignment
COSTS_FILE = args.input_file
MAXIMIZE = args.maximize
INPUT_FILE = args.input_file
DOMINOES_FILE = args.dominoes_file
TILING_FILE = args.tiling_file

if ASSIGNMENT  :
    Examples()
else :
    Portraits()