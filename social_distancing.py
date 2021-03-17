import math , sys , random , argparse , time

# Method to check if a circle hits the bounds. 
def BoundCrash(test_circle,r) :
    crash = False
    for i in BOUND :
        l2 = (i[0][0] - i[1][0])**2 + (i[0][1] - i[1][1])**2
        if l2 == 0 :
            d = math.sqrt((i[0][0] - test_circle[0])**2 + (i[0][1] - test_circle[1])**2)
        else :
            t = ((test_circle[0] - i[0][0])*(i[1][0] - i[0][0]) + (test_circle[1] - i[0][1])*(i[1][1] - i[0][1])) / l2
            t = max(0,min(1,t))
            px = i[0][0] + t*(i[1][0] - i[0][0])
            py = i[0][1] + t*(i[1][1] - i[0][1])
            d = math.sqrt((px - test_circle[0])**2 + (py - test_circle[1])**2)
        d = round(d,2)
        if d < r :
            crash = True
            break
    return crash

# Method to read the bounds from the boundary file.
def ReadBounds():
    bnd = []
    with open(BOUNDARY_FILE) as b :
       for line in b :
            coordinates = [float(x) for x in line.split()]
            bnd.append([(coordinates[0],coordinates[1]),(coordinates[2],coordinates[3])])
    return bnd

# Method to revive all the circles in the front.
def ReviveCircles(front_circles) :
    for i in front_circles :
        if front_circles[i][2] == False :
            front_circles[i][2] = True

# Method to check if at least one cirlce is alive.
def Alive(front_circles) :
    alive = False
    for i in front_circles :
        if front_circles[i][2] == True :
            alive = True
            break
    return alive

# Method to find the closest alive circle to the starting point. 
def FindClosestCircle(start_point,front_circles,circles):
    min = sys.maxsize
    for i in front_circles :
        if front_circles[i][2] == True :
            d = math.sqrt((i[0] - start_point[0])**2 + (i[1] - start_point[1])**2)
            d = round(d,2)
            if d < min :
                min = d
                Cm = i
            elif d == min :
                # check if the circle is older.
                if circles[i][1] < circles[Cm][1] :
                    min = d
                    Cm = i 
    return Cm

# Method to compute the tangential circle.
def ComputeCircle(Cm,Cn,r,circles):
    dx = Cn[0] - Cm[0]
    dy = Cn[1] - Cm[1]
    d = math.sqrt(dx**2 + dy**2)
    r1 = circles[Cm][0] + r
    r2 = circles[Cn][0] + r
    l = (r1**2 - r2**2 + d**2)/(2*d**2)
    e = math.sqrt(abs(r1**2/d**2 - l**2))
    kx = Cm[0] + l*dx - e*dy
    ky = Cm[1] + l*dy + e*dx
    kx = round(kx,2)
    ky = round(ky,2)
    return (kx,ky)

# Method to check if a circle hits another one.
def CircleCheck(circle,r,test_circle,circles) :
    d = math.sqrt((circle[0] - test_circle[0])**2 + (circle[1] - test_circle[1])**2)
    d = round(d,2)
    if d < (r + circles[circle][0])  :
        return True
    else :
        return False

# Method to delete the circles needed from the front.
def DeleteCircles(before,Cj,Cm,Cn,front_circles,deleted_stack = None):
    # initialize start and check circles.
    if before :
        start = Cj
        check = Cn
    else :
        start = Cm
        check = Cj
    f = False
    # the next circle of the starting.
    circle = front_circles[start][1]
    while not f:
        if circle == check :
            f = True
        else :
            # circle to be deleted.
            toDelete = circle
            if BOUNDARY_FILE :
                deleted_stack.append([toDelete,front_circles[toDelete][0],front_circles[toDelete][1],front_circles[toDelete][2]])
            # next circle to be checked.
            circle = front_circles[circle][1]
            # adjust previous and before indications of the circles needed.
            front_circles[front_circles[toDelete][0]][1] = circle
            front_circles[circle][0] = front_circles[toDelete][0]
            del front_circles[toDelete]

# Method to check if the new circle hits other circles of the front. 
def FindCj(Cm,Cn,test_circle,r,front_circles,circles) :
    # the previous circle of Cm.
    prev = front_circles[Cm][0]
    #the next circle of Cn.
    next = front_circles[Cn][1]
    f = False
    c = 1
    crash = False
    Cj = None
    before = None
    if (len(front_circles) - 2) % 2 == 0 :
        stop = (len(front_circles) - 2) / 2
    else :
        stop = (len(front_circles) - 2) // 2 + 1
    while not f :
        # see if we have checked more than the half.
        if c > stop :
            f = True
        # check if the next circle hits the new one.
        elif CircleCheck(next,r,test_circle,circles) :
            f  = True
            before = False
            Cj = next
            crash = True       
        # check if the previous circle hits the new one.
        elif CircleCheck(prev,r,test_circle,circles) :
            f = True
            before = True
            Cj = prev
            crash = True
        # go one step backwards and forward.
        prev = front_circles[prev][0]
        next = front_circles[next][1]
        c += 1
    return [Cj,before,crash]

# Method to return the deleted circles to the front.
def ReturnDeleted(deleted_stack,front_circles) :
    while deleted_stack :
        l = deleted_stack.pop()
        front_circles[l[0]] = [l[1],l[2],l[3]]
        front_circles[l[1]][1] = l[0]
        front_circles[l[2]][0] = l[0]

# Method to write the results in the output file.
def WriteInFile(circles) :
    f = open(OUTPUT_FILE,"w")
    c = 1 
    for i in circles:
        f.write('%.2f' % i[0])
        f.write(" ")
        f.write('%.2f' % i[1])
        f.write(" ")
        f.write(str(circles[i][0]))
        if  not c == len(circles) :
            f.write("\n")
        c += 1
    if BOUNDARY_FILE :
        c = 1
        with open(BOUNDARY_FILE) as b :
            lines = b.readlines()
        f = open(OUTPUT_FILE,"a")
        f.write("\n")
        for line in lines :
            for i in line.split() :    
                f.write(str(float(i)))
                f.write(" ")
            if  not c == len(lines) :
                f.write("\n")
            c += 1

def MainAlgorithm() :
    # starting point.
    start_point = (0,0)
    ''' dictionary with keys the coordinates of all the circles created and
    values a list with their radius and their number of insertion. '''
    circles = {}
    ''' dictionary with keys the coordinates of all the circles in the front and
    values a list with the coordintates of the previous,next circle and an alive boolean.'''
    front_circles = {}
    # intialize radius.
    r = RADIUS
    # use the seed if needed.
    if SEED :
        random.seed(SEED)
    # create random radius if needed.
    if MIN_RADIUS and MAX_RADIUS :
        r = random.randint(MIN_RADIUS,MAX_RADIUS)
    # initialize the first circle.
    circles[(0,0)] = [r,len(circles) + 1]
    # create random radius if needed.
    if MIN_RADIUS and MAX_RADIUS :
        r = random.randint(MIN_RADIUS,MAX_RADIUS)
    # initialize the second circle.
    circles[(r + circles[(0,0)][0],0)] = [r,len(circles) + 1]
    # initialize the two circles in the front.
    front_circles[(0,0)] = [(circles[(0,0)][0] + r,0),(circles[(0,0)][0] + r,0), True]
    front_circles[(r + circles[(0,0)][0],0)] = [(0,0),(0,0), True]
    # boolean to check if the next random radius must be generated.
    next = True
    # while there are alive circles continue inserting.
    while Alive(front_circles) :
        # check if we must instert a specific number of circles.
        if ITEMS :
            if len(circles) == ITEMS :
                break
        # compute Cm and Cj.
        Cm = FindClosestCircle(start_point,front_circles,circles)
        Cn = front_circles[Cm][1]
        # if there are bounds create copy of the current Cm and initialize a stack to append deleted circles.
        if BOUNDARY_FILE :
            deleted_stack = []
            unchanged_Cm = Cm
        # create random radius if needed.
        if MIN_RADIUS and MAX_RADIUS :
            if next :
                r = random.randint(MIN_RADIUS,MAX_RADIUS)
                next = False
        # compute the new circle.
        test_circle = ComputeCircle(Cm,Cn,r,circles)
        # check if the new circle hits an other in the front.
        info = FindCj(Cm,Cn,test_circle,r,front_circles,circles)
        crash = info[2]
        # while the new circle hits other circle(s).
        while crash :
            Cj = info[0]
            before = info[1]
            # delete the circles needed to continue the algorithm.   
            if BOUNDARY_FILE :
                DeleteCircles(before,Cj,Cm,Cn,front_circles,deleted_stack)
            else :
                DeleteCircles(before,Cj,Cm,Cn,front_circles)
            # adjust Cm or Cn.
            if before :
                Cm = Cj
            else :
                Cn = Cj
            # repeat computing the new circle.
            test_circle = ComputeCircle(Cm,Cn,r,circles)
            info = FindCj(Cm,Cn,test_circle,r,front_circles,circles)
            crash = info[2]
        if BOUNDARY_FILE :
            # check if the new circle hits the bounds.
            if BoundCrash(test_circle,r) :
                # return the deleted circles to the front.
                ReturnDeleted(deleted_stack,front_circles)
                # set the initial Cm tha was checked as not alive.
                front_circles[unchanged_Cm][2] = False
            else :
                # insert the new circle.
                circles[test_circle] = [r,len(circles) + 1]
                front_circles[test_circle] = [Cm,Cn, True]
                front_circles[Cm][1] = test_circle
                front_circles[Cn][0] = test_circle
                ReviveCircles(front_circles)
                next = True
        else :
            # insert the new circle.
            circles[test_circle] = [r,len(circles) + 1]
            front_circles[test_circle] = [Cm,Cn, True]
            front_circles[Cm][1] = test_circle
            front_circles[Cn][0] = test_circle
            next = True
    # print the number of the circles created.
    print(len(circles))
    WriteInFile(circles)

start = time.time()
# Parse the command line arguments.
parser = argparse.ArgumentParser()
parser.add_argument("-i","--items", type=int, help="items to be printed")
parser.add_argument("-r","--radius",type=int, help="radius of all circles")
parser.add_argument("--min_radius", type=int, help="minimum radius of random circles")
parser.add_argument("--max_radius", type=int, help="maximum radius of random circles")
parser.add_argument("-b","--boundary_file",help="boundary file")
parser.add_argument("-s","--seed", type=int, help="random seed") 
parser.add_argument("output_file",help="name of the input file")             
args = parser.parse_args()
ITEMS = args.items
RADIUS = args.radius
MIN_RADIUS = args.min_radius
MAX_RADIUS = args.max_radius
BOUNDARY_FILE = args.boundary_file  
SEED = args.seed
OUTPUT_FILE = args.output_file 

# Read bounds from boundary file.
if BOUNDARY_FILE :
    BOUND = ReadBounds()

# Execute the algorithm.
MainAlgorithm()
end = time.time()
print(end - start)