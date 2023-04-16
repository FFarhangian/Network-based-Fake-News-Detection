# create a dictionary to store the network
network_dict = {}

# loop through each row in the followers dataframe and add the user_id and follower_id to the dictionary
for index, row in followers.iterrows():
    user_id = row['user_id']
    follower_id = row['follower_id']
    if user_id not in network_dict:
        network_dict[user_id] = {'following': set(), 'followers': set()}
    network_dict[user_id]['followers'].add(follower_id)

# loop through each row in the Real_users dataframe and add the tweet label to the dictionary
for index, row in Real_users.iterrows():
    user_id = row['user_id']
    tweet_label = row['tweet_label']
    if user_id not in network_dict:
        network_dict[user_id] = {'following': set(), 'followers': set(), 'tweet_label': tweet_label}
    else:
        network_dict[user_id]['tweet_label'] = tweet_label

# loop through each row in the Fake_users dataframe and add the tweet label to the dictionary
for index, row in Fake_users.iterrows():
    user_id = row['user_id']
    tweet_label = row['tweet_label']
    if user_id not in network_dict:
        network_dict[user_id] = {'following': set(), 'followers': set(), 'tweet_label': tweet_label}
    else:
        network_dict[user_id]['tweet_label'] = tweet_label

# loop through each row in the following dataframe and add the user_id and following_id to the dictionary
for index, row in followings.iterrows():
    user_id = row['user_id']
    following_id = row['following_id']
    if user_id not in network_dict:
        network_dict[user_id] = {'following': set(), 'followers': set()}
    network_dict[user_id]['following'].add(following_id)

import pickle

# save network_dict to file
with open('network_dict_new_before_R.pkl', 'wb') as f:
    pickle.dump(network_dict, f)


####################################################################

import pickle
# load network_dict from file
with open('network_dict_neww.pkl', 'rb') as f:
    network_dict = pickle.load(f)

real_network = {}
fake_network = {}

for user_id, network_info in network_dict.items():
    if network_info.get('tweet_label') == 'real':
        real_network[user_id] = network_info
    elif network_info.get('tweet_label') == 'fake':
        fake_network[user_id] = network_info


import networkx as nx

# Create an empty dictionary to store the graphs for each network
# Create a graph for the real network
real_network_graph = nx.Graph()  # Replace DiGraph() with Graph()
for user_id, network_info in real_network.items():
    for follower_id in network_info['followers']:
        real_network_graph.add_edge(user_id, follower_id)
for user_id, network_info in real_network.items():
    for following_id in network_info['following']:
        real_network_graph.add_edge(following_id, user_id)
# network_graphs['real'] = real_network_graph

nx.write_graphml(real_network_graph, 'real_network_graph')


# save network_dict to file
with open('real_network_graph.pkl', 'wb') as f:
    pickle.dump(real_network_graph, f)


import networkx as nx

# Create a graph for the fake network
fake_network_graph = nx.Graph()  # Replace DiGraph() with Graph()
for user_id, network_info in fake_network.items():
    for follower_id in network_info['followers']:
        fake_network_graph.add_edge(user_id, follower_id)
for user_id, network_info in fake_network.items():
    for following_id in network_info['following']:
        fake_network_graph.add_edge(following_id, user_id)
# network_graphs['fake'] = fake_network_graph

nx.write_graphml(fake_network_graph, 'fake_network_graph')


# save network_dict to file
with open('fake_network_graph.pkl', 'wb') as f:
    pickle.dump(fake_network_graph, f)


########################################################Analysis
# compute the number of nodes and edges
real_nodes = len(real_network_graph.nodes())
print(f"#nodes: {real_nodes}")

real_edges = len(real_network_graph.edges())
print(f"#edges: {real_edges}")

fake_nodes = len(real_network_graph.nodes())
print(f"#nodes: {fake_nodes}")

fake_edges = len(real_network_graph.edges())
print(f"#edges: {fake_edges}")

# compute the degree distribution
real_degrees = dict(real_network_graph.degree())
fake_degrees = dict(fake_graph.degree())

# compute the density
real_density = nx.density(real_network_graph)
fake_density = nx.density(fake_graph)

# compute the clustering coefficient
real_cc = nx.average_clustering(real_network_graph)
fake_cc = nx.average_clustering(fake_graph)

# compute the betweenness centrality
# Calculate centrality measures for real_network_graph
real_betweenness_centrality = nx.betweenness_centrality(real_network_graph)
# Print average centrality measures for real_network_graph
print("Average betweenness centrality (real network):", sum(real_betweenness_centrality.values()) / len(real_network_graph))

# Calculate centrality measures for fake_network_graph
fake_betweenness_centrality = nx.betweenness_centrality(fake_network_graph)
# Print average centrality measures for fake_network_graph
print("Average betweenness centrality (fake network):", sum(fake_betweenness_centrality.values()) / len(fake_network_graph))

#Ave Closeness Centrality
real_closeness_centrality = nx.closeness_centrality(real_network_graph)
print("Average closeness centrality (real network):", sum(real_closeness_centrality.values()) / len(real_network_graph))

fake_closeness_centrality = nx.closeness_centrality(fake_network_graph)
print("Average closeness centrality (fake network):", sum(fake_closeness_centrality.values()) / len(fake_network_graph))

# Average eigenvector centrality
real_eigenvector_centrality = nx.eigenvector_centrality(real_network_graph)
print("Average eigenvector centrality (real network):", sum(real_eigenvector_centrality.values()) / len(real_network_graph))

fake_eigenvector_centrality = nx.eigenvector_centrality(fake_network_graph)
print("Average eigenvector centrality (fake network):", sum(fake_eigenvector_centrality.values()) / len(fake_network_graph))

# compute the PageRank centrality
real_pr = nx.pagerank(real_network_graph)
fake_pr = nx.pagerank(fake_graph)

# Average geodesic distance
import networkx as nx

# Calculate average geodesic distance for true network
avg_geodist_true = nx.average_shortest_path_length(real_network_graph)

# Calculate average geodesic distance for fake network
avg_geodist_fake = nx.average_shortest_path_length(fake_network_graph)

print("Average geodesic distance for true network:", avg_geodist_true)
print("Average geodesic distance for fake network:", avg_geodist_fake)

#Compute #Triads
fake_triads = sum(nx.triangles(fake_network_graph).values()) // 3
print(f"#triads: {fake_triads}")

real_triads = sum(nx.triangles(real_network_graph).values()) // 3
print(f"#triads: {real_triads}")

#Compute diameter
fake_diameter = nx.diameter(fake_network_graph)
print(f"The network diameter is: {fake_diameter}")

real_diameter = nx.diameter(real_network_graph)
print(f"The network diameter is: {real_diameter}")

# if not nx.is_connected(fake_network_graph):
#     # Calculate the diameter for each connected component
#     diameter = 0
#     for component in nx.connected_components(fake_network_graph):
#         subgraph = fake_network_graph.subgraph(component)
#         component_diameter = nx.diameter(subgraph)
#         if component_diameter > diameter:
#             diameter = component_diameter
# else:
#     diameter = nx.diameter(fake_network_graph)
#
# print(f"fake_diameter: {diameter}")

# Calculate Assortativity
real_assortativity = nx.degree_assortativity_coefficient(real_network_graph)
print(f"Assortativity of real network: {real_assortativity}")

fake_assortativity = nx.degree_assortativity_coefficient(fake_network_graph)
print(f"Assortativity of fake network: {fake_assortativity}")

