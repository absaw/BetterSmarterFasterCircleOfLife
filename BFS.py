from Graph import *

def get_bfs_path(G:nx.Graph,start,end):
    visited_set=set([])
    
    fringe_q=deque([[start]])
    path_found=False


    while len(fringe_q)>0:

        if start==end:
            # print("Goal reached")
            path_found=True
            updated_path=[start]
            break
        path = fringe_q.popleft()
        
        curr_node=path[-1]
        
        if curr_node not in visited_set:
            neighbor_list=list(G.neighbors(curr_node))

            for neighbor in neighbor_list:
                updated_path=list(path)
                updated_path.append(neighbor)
                fringe_q.append(updated_path)

                if neighbor == end:
                    # print("Shortest path=",updated_path)
                    path_found=True
                    break
            if path_found:
                break
            visited_set.add(curr_node)

    if path_found==False:
        return None
        # print("Path not found")
    
    return updated_path

# G=generate_graph(10)

# G=nx.Graph()
# G.add_edge(1,2)
# # G.add_edge(1,3)
# # G.add_edge(1,6)
# G.add_edge(1,5)
# G.add_edge(5,6)
# G.add_edge(6,4)
# G.add_edge(3,4)
# G.add_edge(2,3)
# G.add_edge(1,4)
# visualize_graph(G)

# print(get_bfs_path(G,1,4)[1])
        
