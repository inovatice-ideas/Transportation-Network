"""
Enter the solution for Q3 here.
Note: You may use may define any additional class, functions if necessary.
However, DO NOT CHANGE THE TEMPLATE CHANGE THE TEMPLATE OF THE FUNCTIONS PROVIDED.
"""

# This program import the 'anaheim_gtfs.zip' file and extract the required dataset. The datasets are processed to create dictionary of
# various relevant informations to be accessed easily. Then edges are determined on the basis of route_id and stop_sequence. Then it
# create a graph from the edges and runs a DFS search in order to count the number of routes from source to destination given as input.

#importing required modules
from zipfile import ZipFile
import pandas as pd
import numpy as np

#specifying the zip file name
fileName = 'anaheim_gtfs.zip'

#opening the zip file in READ mode
with ZipFile(fileName, 'r') as zip:
    zip.printdir()
    zip.extract('stops.txt')
    zip.extract('routes.txt')
    zip.extract('trips.txt')
    zip.extract('stop_times.txt')

#Processing the stop id and creating a dictionary for easy access for the graph
stop_id = pd.read_csv('stops.txt')['stop_id']
stop_id_dict = dict({})
for i in range(len(stop_id)):
    stop_id_dict[stop_id[i]] = i

#no of vertices for graph i.e. no of stops
n = len(stop_id_dict)

#definition of graphs
graph_object = [[] for i in range(n)]

#Processing the route id and creating a dictionary for easy access for the graph
route_id = pd.read_csv('routes.txt')['route_id']
route_id_dict = dict({})
for i in range(len(route_id)):
    route_id_dict[route_id[i]] = i

#Processing the trip id, route id and creating a dictionary for easy access for the graph
trips_data = pd.read_csv('trips.txt')[['trip_id','route_id']]
trip_id = trips_data['trip_id']
route_id = trips_data['route_id']
trip_id_dict = dict({})
for i in range(len(trip_id)):
    trip_id_dict[trip_id[i]] = route_id_dict[route_id[i]]

#Processing the stop id, trip id, stop sequence and creating a dictionary for easy access for the graph
stop_times = pd.read_csv('stop_times.txt')[['trip_id','stop_id','stop_sequence']]
trip_id = stop_times['trip_id']
stop_id = stop_times['stop_id']
stop_sequence = stop_times['stop_sequence']

#For storing the unique edges present in the dataset
edges = set()

#Running through the 'stop_times.txt' to extract the stop sequence and stop_ids and add their edges if not already in the set
for i in range(len(trip_id)-1):
    #Next stop sequence
    curr = stop_sequence[i+1]
    #Current stop sequence
    prev = stop_sequence[i]
    #Checking whether the cities are in the direction of the edge
    if curr > prev:
        #Adding the edge in the form of tuples (source, destination, route_id)
        #We get the route_id from the trip_id_dict which we created earlier for easy access
        edges.add((stop_id_dict[stop_id[i]], stop_id_dict[stop_id[i+1]], trip_id_dict[trip_id[i]]))
    else:
        #Ignoring the existing edges or invalid edges
        continue

#Creating the adjacency list by adding the edges to the same, also keeping the route info intact
for i in edges:
    graph_object[i[0]].append([i[1],i[2]])

#Util Function for the number of routes function
def number_of_routes_Util(u: int, dest: int, visited, routesCount, prev):
    #Marking the current vertice as visited
    visited[u] = True
    #Checking if the current vertice is the destination itself, if yes we increment the count
    if u == dest:
        routesCount[0] += 1
        
    else:
        i = 0
        #Going through the vertices linked to the current vertice
        while i < len(graph_object[u]):
            #Checking whether the vertice is unvisited and the source follows the same route as previous
            if (not visited[graph_object[u][i][0]]) and graph_object[u][i][1] == prev:
                #Doing a recursive call with the linked vertice as the new source vertice
                number_of_routes_Util(graph_object[u][i][0], dest, visited, routesCount, prev)
            #Incrementing the loop variable
            i += 1
    #Marking the current vertice unvisited for backtracking
    visited[u] = False

#Function for getting the number of routes from source to destination
def number_of_routes(source_stopid: str, destination_stopid: str) -> int:
    #Find the number of routes going from source stop id to destination stop id.
    #Args:
        #source_stopid (str): Source Stop Id
        #destination_stopid (str): Destination Stop Id
    #Returns:
        #final_count (int): Number of routes going from source to destination.
    final_count = -1
    try:
        # Enter your code here
        #Getting the numerical representation of the source stop_id
        src = stop_id_dict[source_stopid]
        #Getting the numerical representation of the destination stop_id
        dest = stop_id_dict[destination_stopid]
        #Initializing the visited array with False marking all the vertices as unvisited
        visited = [False]*n
        #List for keeping track of the number of routes
        routesCount = [0]
        #Going through the linked vertices of the source vertice
        for i in  graph_object[src]:
            #Calling the util function fro the number of routes
            number_of_routes_Util(src, dest, visited, routesCount, i[1])
        #Assigning the count of routes to final_count for final return
        final_count = routesCount[0]
        return final_count
    except:
        return final_count