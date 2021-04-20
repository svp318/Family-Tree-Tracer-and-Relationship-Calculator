import networkx as nx
from family_matrix import FamilyMatrix


class FamilyGraph:
    def __init__(self, people_dict):
        self.people = people_dict
        self.edges_list = set()
        for p in self.people.values():
            if p.father_id != "":
                self.edges_list.add((p.father_id, p.ident))
            if p.mother_id != "":
                self.edges_list.add((p.mother_id, p.ident))
        self.graph = nx.DiGraph()
        self.graph.add_edges_from(self.edges_list)
        self.u_graph = self.graph.to_undirected()

    def get_graph(self):
        return self.graph

    def get_u_graph(self):
        return self.u_graph

    def check_is_dag(self):
        return nx.is_directed_acyclic_graph(self.graph)

    def get_shortest_path(self, source_p, target_p, r_format="names"):
        return nx.shortest_path(self.u_graph, source_p, target_p)

    def get_all_paths(self, source_p, target_p, r_format="names"):
        all_s_paths = list(nx.all_simple_paths(self.u_graph, source_p, target_p))
        all_s_paths.sort(key=len)
        latest_person = ""
        at_first = True
        familiarity_matrix_coordinates = [0] * 2
        bad_path = False
        good_s_paths = list()
        for s_path in all_s_paths:
            for p in s_path:
                if at_first:
                    latest_person = p
                    at_first = False
                else:
                    if p == self.people[latest_person].father_id or p == self.people[latest_person].mother_id:
                        latest_person = p
                        familiarity_matrix_coordinates[0] += 1
                        if familiarity_matrix_coordinates[1] > 0:
                            bad_path = True
                            break
                    else:
                        latest_person = p
                        familiarity_matrix_coordinates[1] += 1
            if not bad_path:
                print(f"Appending good path: {s_path}")
                good_s_paths.append(s_path)
            else:
                # print(f"Not appending bad path: {s_path}")
                bad_path = False
            latest_person = ""
            at_first = True
            familiarity_matrix_coordinates = [0] * 2
        return good_s_paths

    def get_trace_text(self, path):
        last_in_s_path = len(path) - 1
        for i, p in enumerate(path):
            if i == last_in_s_path:
                # Last iteration
                print(f"{self.people[p].name} {self.people[p].last_names}")
            else:
                print(f"{self.people[p].name} {self.people[p].last_names} -> ", end="")

    def get_relationship_text(self, path):
        latest_person = ""
        at_first = True
        familiarity_matrix_coordinates = [0] * 2
        for p in path:
            if at_first:
                latest_person = p
                at_first = False
            else:
                if p == self.people[latest_person].father_id or p == self.people[latest_person].mother_id:
                    latest_person = p
                    familiarity_matrix_coordinates[0] += 1
                else:
                    latest_person = p
                    familiarity_matrix_coordinates[1] += 1
        print(f"The family matrix coordinates are {familiarity_matrix_coordinates}")

        fm = FamilyMatrix()
        print(f"{self.people[path[-1]].name} {self.people[path[-1]].last_names} is ", end="")
        print(f"{self.people[path[0]].name} {self.people[path[0]].last_names}'s ", end="")
        print(fm.get_relationship(familiarity_matrix_coordinates))
        print("")

    def get_predecessors(self, ident):
        return self.graph.predecessors(ident)

    def get_successors(self, ident):
        return self.graph.successors(ident)

    def get_descendants(self, ident):
        return nx.descendants(self.graph, ident)

    def get_ancestors(self, ident):
        return nx.ancestors(self.graph, ident)
