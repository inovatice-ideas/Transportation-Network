"""
Enter the solution for Q2 here.
Note: You may use may define any additional class, functions if necessary.
However, DO NOT CHANGE THE TEMPLATE CHANGE THE TEMPLATE OF THE FUNCTIONS PROVIDED.
"""

# This program import the minDistance() function from Question 1. Then it runs the 'bidirectional_dij()' function to compute the
# length of shortest path from source to destination given as input by simultaneously moving in forward and backward direction 
# and to meet in the middle.

from Q1 import minDistance

#Function implementing the bidirectional dijkstra algorithm
def bidirectional_dij(source: int, destination: int, graph_object) -> int:
    #Bi-directional Dijkstra's algorithm.
    #Args:
        #source (int): Source stop id
        #destination (int): destination stop id
        #graph_object: python object containing network information
    #Returns:
        #shortest_path_distance (int): length of the shortest path.
    #Warnings:
        #If the destination is not reachable, function returns -1
    shortest_path_distance = -1

    try:
        # Enter your code here
        #toring the number of vertices for easy usage
        n = len(graph_object)
        #Initializing the distance array to infinity for forward direction
        dist_src = [float('inf')]*n
        dist_src[source-1] = 0
        #Initializing the sptSet array to unvisited for forward direction
        sptSet_src = [False]*n
        #Initializing the distance array to infinity for backward direction
        dist_dest = [float('inf')]*n
        dist_dest[destination-1] = 0
        #Initializing the sptSet array to unvisited for backward direction
        sptSet_dest = [False]*n
        #To store the shortest path distance
        mu = float('inf')
        #Running a loop through all vertices
        for i in range(n):
            #Getting the unvisited vertice which is closest to the source
            x_src = minDistance(dist_src, sptSet_src)
            #Getting the unvisited vertice which is closest to the destination
            x_dest = minDistance(dist_dest, sptSet_dest)
            #Marking the vertice closest to the source visited
            sptSet_src[x_src] = True
            #Marking the vertice closest to the destination visited
            sptSet_dest[x_dest] = True
            #Running through all the vertices in forward direction to update the forward distance array and mu
            for y in range(n):
                #Relaxing the forward distance array
                if graph_object[x_src][y] > 0 and sptSet_src[y] == False and \
                    dist_src[y] > dist_src[x_src] + graph_object[x_src][y]:
                        dist_src[y] = dist_src[x_src] + graph_object[x_src][y]
                #For updating the shortest distance so far if a meeting point is encountered
                if graph_object[x_src][y] > 0 and sptSet_dest[y] == True and \
                    dist_src[x_src] + graph_object[x_src][y] + dist_dest[y] < mu:
                        mu = dist_src[x_src] + graph_object[x_src][y] + dist_dest[y]
            #Running through all the vertices in backward direction to update the backward distance array and mu
            for y in range(n):
                #Relaxing the backward distance array
                if graph_object[y][x_dest] > 0 and sptSet_dest[y] == False and \
                    dist_dest[y] > dist_dest[x_dest] + graph_object[y][x_dest]:
                        dist_dest[y] = dist_dest[x_dest] + graph_object[y][x_dest]
                #For updating the shortest distance so far if a meeting point is encountered
                if graph_object[y][x_dest] > 0 and sptSet_src[y] == True and \
                    dist_dest[x_dest] + graph_object[y][x_dest] + dist_src[y] < mu:
                        mu = dist_dest[x_dest] + graph_object[y][x_dest] + dist_src[y]
            #Terminating Condition for the algorithm
            if dist_src[x_src] + dist_dest[x_dest] >= mu:
                break
        #Rounding off the shortest distance of the destination vertice and returning it
        shortest_path_distance = round(mu)
        return shortest_path_distance
    except:
        return shortest_path_distance