import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import networkx as nx
from pyvis.network import Network

# Read dataset (CSV)

def bad_line(x):
    print(x)
    return None
  
df = pd.read_csv('https://github.com/huilde/networkAnalisys/blob/d27ffc3d70fcdb9af0a7dd1640ab7b4ba5c9403c/dados.csv?raw=true',sep=';',skiprows=[0] ,encoding='unicode_escape', on_bad_lines=bad_line, engine='python',usecols = ["AEROPORTO_DE_ORIGEM_SIGLA", "AEROPORTO_DE_DESTINO_SIGLA","ANO"])


df_between_airports = df.groupby(by=["AEROPORTO_DE_ORIGEM_SIGLA", "AEROPORTO_DE_DESTINO_SIGLA"]).count()
df_between_airports = df_between_airports['ANO'].rename('QUANTIDADE').reset_index()
df_between_airports = df_between_airports.sort_values(by="QUANTIDADE", ascending=False)

df_between_airports = df_between_airports
df_between_airports['QUANTIDADE'] = df_between_airports['QUANTIDADE'] / 50

node_sizes = df_between_airports.groupby('AEROPORTO_DE_ORIGEM_SIGLA').QUANTIDADE.agg(sum)

nodes = list(set([*df_between_airports['AEROPORTO_DE_ORIGEM_SIGLA'],
                  *df_between_airports['AEROPORTO_DE_DESTINO_SIGLA']
                 ]))
# Set header title
st.title('Network Graph Visualization')


net = Network(
    notebook = True,
    directed = True,            # directed graph
    bgcolor = "black",          # background color of graph
    font_color = "yellow",      # use yellow for node labels
    cdn_resources = 'in_line',  # make sure Jupyter notebook can display correctly
    height = "1000px",          # height of chart
    width = "100%",             # fill the entire width
    )



values = [node_sizes.get(node, 0)for node in nodes]
net.add_nodes(nodes, value = values)

edges = df_between_airports.values.tolist()
net.add_edges(edges)
net.show_buttons(filter_=['physics'])

net.repulsion(node_distance=420, central_gravity=0.33,
                       spring_length=110, spring_strength=0.10,
                       damping=0.95)

    # Save and read graph as HTML file (on Streamlit Sharing)
    try:
        path = '/tmp'
        net.save_graph(f'{path}/net.html')
        HtmlFile = open(f'{path}/net.html', 'r', encoding='utf-8')

    # Save and read graph as HTML file (locally)
    except:
        path = '/html_files'
        net.save_graph(f'{path}/net.html')
        HtmlFile = open(f'{path}/net.html', 'r', encoding='utf-8')

    # Load HTML file in HTML component for display on Streamlit page
    components.html(HtmlFile.read(), height=435)
