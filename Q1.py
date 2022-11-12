"""
CiSTUP Internship: Round 1
Enter the solution for Q1 here.
Note: You may use may define any additional class, functions if necessary.
However, DO NOT CHANGE THE TEMPLATE CHANGE THE TEMPLATE OF THE FUNCTIONS PROVIDED.
"""
# This program reads the 'ChicagoSketch_net.tntp.txt' file and extract the necessary data. Then it process the data and evaluate the cost
# of the edges present in the graph (depicting the transport network of Chicago). Then it runs the 'Q1_dijkstra()' function to compute the
# length of shortest path from source to destination given as input
 
#importing the required modules
import pandas as pd
import numpy as np

#Assuming the distance factor for calculating cost of the links of the graph
const = 0.001

#Function for calculating the weights of the edges of the graph
def find_cost(data):
    link_travel_time = data[4]*(1+data[5]*pow(data[4]/data[2], data[6]))
    link_generalised_cost = link_travel_time + const*data[3]
    return link_generalised_cost

#Function for generating the graph from the given dataset
def Dij_generator():
    """
    Reads the ChicagoSketch_net.tntp and convert it into suitable python object on which you will implement shortest-path algorithms.
    Returns:
        graph_object: variable containing network information.
    """
    #Storing the name of the txt file of the dataset
    url = 'ChicagoSketch_net.tntp.txt'
    #Declaration of graph object
    graph_object = None
    try:
        # Enter your code here
        #Reading the dataset in csv format and transforming it to dataframe
        df = pd.read_csv(url)
        #Extracting the no of vertices for the graph object
        no_of_nodes = int(df.iloc[0][0].split()[-1])
        #Extracting the no of edges of the graph object
        no_of_links = int(df.iloc[2][0].split()[-1])
        #Creating the adjacency matrix for storing the cost of the graph with initial values being 0
        graph_object = np.zeros([no_of_nodes, no_of_nodes])
        #Running a loop throught the dataframe and splitting it to extract relevant data for calculating the cost
        for i in range(no_of_links):
            data = df.iloc[i+6][0].split()[0:10]
            #Converting the data from string datatype to float datatype
            for j in range(10):
                data[j] = float(data[j])
            #Updating the cost matrix of graph with the cost of that edge
            #The graph object is 0-indexed hence taking source and destination and subtracting 1 to point to it's corresponding cost
            graph_object[int(data[0])-1][int(data[1])-1] = find_cost(data)
        return graph_object
    except:
        return graph_object

#Function for finding the unvisited vertice which is at closest to the source 
def minDistance(distance, sptSet):
    #Initializing min variable to infinity
    min = float('inf')
    #Running a loop through distance array to get the vertice which is unvisited and closest to the source
    for u in range(len(distance)):
        if distance[u] < min and sptSet[u] == False:
            min = distance[u]
            min_index = u
    return min_index

#Modified function of dijkstra's algorithm
def Q1_dijkstra(source: int, destination: int, graph_object) -> int:
    #Dijkstra's algorithm.
    #Args:
        #source (int): Source stop id
        #destination (int): : destination stop id
        #graph_object: python object containing network information
    #Returns:
        #shortest_path_distance (int): length of the shortest path.
    #Warnings:
        #If the destination is not reachable, function returns -1
    shortest_path_distance = -1
    try:
        # Enter your code here
        #Storing the number of vertices for easy handling
        n = len(graph_object)
        #Initializing the distance array with inifinity and updating the source distance to 0
        distance = [float('inf')]*n
        distance[source-1] = 0
        #Initializing the sptSet array to False marking every nodes unvisited
        sptSet = [False]*n
        
        #Running a loop through all vertices as it would be the maximum no the loop can run
        for i in range(n):
            #Getting the vertice which is closest to the source and unvisited
            x = minDistance(distance, sptSet)
            #Base case for terminating the loop if destination is reached
            if x==destination-1:
                break
            #Marking the current vertice as visited
            sptSet[x] = True
            #Running through all the vertices for updating the distance array
            for y in range(n):
                #Checking whether there exists a link and the vertice is still unvisted and its distance from source is min or not
                if graph_object[x][y] > 0 and sptSet[y] == False and \
                    distance[y] > distance[x] + graph_object[x][y]:
                        #Updating the distance from the source to the minimum
                        distance[y] = distance[x] + graph_object[x][y]
        #Rounding off the shortest distance of the destination vertice and returning it
        shortest_path_distance = round(distance[destination-1])
        return shortest_path_distance
    except:
        return shortest_path_distance