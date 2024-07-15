import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt

# Function to load external CSS file
def load_css(file_name):
    with open(file_name, 'r') as f:
        css = f.read()
    st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)

# Load external CSS
load_css('style.css')

# Function to visualize the graph
def visualize_graph(G):
    pos = nx.spring_layout(G)
    plt.figure(figsize=(8, 6))
    nx.draw(G, pos, with_labels=True, node_size=700, node_color="lightblue", font_color='red')
    labels = nx.get_edge_attributes(G, 'capacity')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, font_color='red')
    st.pyplot(plt)

# Function to solve maximum flow
def solve_maximum_flow():
    st.title("Maximum Flow Problem Solver")

    st.sidebar.header("Graph Input")
    st.sidebar.markdown("---")

    # Number of nodes
    num_nodes = st.sidebar.number_input("Number of nodes", min_value=2, value=7, key='maxflow_num_nodes')

    # Add edges
    edges = []
    for i in range(1, num_nodes + 1):
        for j in range(1, num_nodes + 1):
            if i != j:
                u = str(i)
                v = str(j)
                capacity = st.sidebar.number_input(f"Capacity of edge {u} -> {v}", min_value=0, value=0, key=f'maxflow_capacity_{u}_{v}')
                if capacity > 0:
                    edges.append((u, v, capacity))

    # Create directed graph
    G = nx.DiGraph()
    for u, v, capacity in edges:
        G.add_edge(u, v, capacity=capacity)

    source = st.sidebar.text_input("Source node", "1", key='maxflow_source')
    target = st.sidebar.text_input("Target node", str(num_nodes), key='maxflow_target')

    if st.sidebar.button("Visualize Network"):
        visualize_graph(G)

    if st.sidebar.button("Solve Maximum Flow"):
        # Compute maximum flow
        try:
            flow_value, flow_dict = nx.maximum_flow(G, source, target)
            st.success(f"Maximum Flow: {flow_value}")

            st.subheader("Flow Distribution:")
            for key_i, inner_dict in flow_dict.items():
                for key_j, inner_val in inner_dict.items():
                    st.write(f'{key_i} -> {key_j}: {inner_val}')

            visualize_graph(G)

        except nx.NetworkXError as e:
            st.error(f"Error: {e}")

# Function to solve minimum cost flow
def solve_minimum_cost_flow():
    st.title("Minimum Cost Flow Problem Solver")

    st.sidebar.header("Graph Input")
    st.sidebar.markdown("---")

    # Set up the directed network with node demands and edge costs
    num_nodes = st.sidebar.number_input("Number of nodes", min_value=2, value=5, key='mincost_num_nodes')

    nodes = []
    for i in range(1, num_nodes + 1):
        demand = st.sidebar.number_input(f"Demand for node {i} (negative for supply)", value=0, key=f'mincost_demand_{i}')
        color = '#C5E0B4' if demand < 0 else '#F8CBAD'
        nodes.append((i, demand, color))

    edges = []
    for i in range(1, num_nodes + 1):
        for j in range(1, num_nodes + 1):
            if i != j:
                weight = st.sidebar.number_input(f"Cost of edge {i} -> {j}", value=0, key=f'mincost_weight_{i}_{j}')
                capacity = st.sidebar.number_input(f"Capacity of edge {i} -> {j}", min_value=0, value=999999, key=f'mincost_capacity_{i}_{j}')
                if weight != 0 or capacity != 999999:
                    edges.append((i, j, weight, capacity))

    # Create directed graph
    G = nx.DiGraph()
    for node, demand, color in nodes:
        G.add_node(node, demand=demand, color=color)

    for u, v, weight, capacity in edges:
        G.add_edge(u, v, weight=weight, capacity=capacity)

    # Check if the sum of demands is zero
    total_demand = sum(demand for _, demand, _ in nodes)
    if total_demand != 0:
        st.error("Error: The sum of demands must be zero. Please adjust the node demands.")
        return

    if st.sidebar.button("Visualize Network"):
        node_pos = {i: (i % 3, i // 3) for i in range(1, num_nodes + 1)}
        node_colors = list(nx.get_node_attributes(G, 'color').values())
        plt.figure(figsize=(8, 6))
        nx.draw(G, node_pos, with_labels=True, node_color=node_colors, node_size=1000, node_shape='h', connectionstyle='arc3, rad=0.1')
        labels = nx.get_edge_attributes(G, 'weight')
        nx.draw_networkx_edge_labels(G, node_pos, edge_labels=labels)
        st.pyplot(plt)

    if st.sidebar.button("Solve Minimum Cost Flow"):
        try:
            # Solve the model using network simplex method
            flowCost, flowDict = nx.network_simplex(G)
            st.success(f'Minimum cost: {flowCost}')

            st.subheader("Flow Distribution:")
            for key_i, inner_dict in flowDict.items():
                for key_j, inner_val in inner_dict.items():
                    st.write(f'{key_i} -> {key_j}\t Flow: {inner_val}')

            node_pos = {i: (i % 3, i // 3) for i in range(1, num_nodes + 1)}
            node_colors = list(nx.get_node_attributes(G, 'color').values())
            plt.figure(figsize=(8, 6))
            nx.draw(G, node_pos, with_labels=True, node_color=node_colors, node_size=1000, node_shape='h', connectionstyle='arc3, rad=0.1')
            labels = nx.get_edge_attributes(G, 'weight')
            nx.draw_networkx_edge_labels(G, node_pos, edge_labels=labels)
            st.pyplot(plt)

        except nx.NetworkXUnfeasible:
            st.error("No feasible solution: Check your demands and capacities.")

# Streamlit app with multiple pages
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Maximum Flow", "Minimum Cost Flow"])

if page == "Maximum Flow":
    solve_maximum_flow()
elif page == "Minimum Cost Flow":
    solve_minimum_cost_flow()

# Add footer
footer = """
<div class="footer">
    <p>Developed By Sehan D Amendra</p>
</div>
"""
st.markdown(footer, unsafe_allow_html=True)
