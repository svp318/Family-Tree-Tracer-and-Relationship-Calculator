import csv
from person import Person
from family_graph import FamilyGraph
import networkx as nx
from matplotlib import pyplot as plt
import pydot
import pygraphviz
# from networkx.drawing.nx_pydot import graphviz_layout
from networkx.drawing.nx_pydot import graphviz_layout


people = dict()
with open('people.csv', 'r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        people[row["identification"]] = \
            Person(row["identification"], row["names"], row["last_names"], row["father"], row["mother"])

graph = FamilyGraph(people)

print(f"Is this a Directed Acyclic Graph?: {'Yes' if graph.check_is_dag() else 'No'}")


T = nx.balanced_tree(2, 5)

pos = graphviz_layout(T, prog="twopi")
nx.draw(T, pos)
plt.show()

source_p = ""
target_p = ""
while source_p != "exit" and source_p != "EXIT":
    source_p = "IOFSBZQT"  # input("Enter source person: ")
    if source_p != "exit" and source_p != "EXIT":
        target_p = "TTDSEGIW"  # input("Enter target person: ")
        good_s_paths = graph.get_all_paths(source_p, target_p)
        # s_path = list(p for p in good_s_paths)[2]
        print(f"good_s_paths: {good_s_paths}")
        # print(f"s_path: {s_path}")
        for s_path in good_s_paths:
            graph.get_trace_text(s_path)
            graph.get_relationship_text(s_path)
    source_p = "exit"

ident = ""
while ident != "exit" and ident != "EXIT":
    ident = input("Enter ident: ")
    if ident != "exit" and ident != "EXIT":
        predecessors = graph.get_predecessors(ident)
        successors = graph.get_successors(ident)
        ancestors = graph.get_ancestors(ident)
        descendants = graph.get_descendants(ident)
        print("\nPredecessors:")
        for p in predecessors:
            print(f"{people[p].name} {people[p].last_names}")
        print("\nSuccessors:")
        for p in successors:
            print(f"{people[p].name} {people[p].last_names}")
        print("\nAncestors:")
        for p in ancestors:
            print(f"{people[p].name} {people[p].last_names}")
        print("\nDescendants:")
        for p in descendants:
            print(f"{people[p].name} {people[p].last_names}")
