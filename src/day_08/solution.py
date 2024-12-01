import math
import os
import re
import sys
from collections import Counter, OrderedDict, defaultdict, deque, namedtuple
from datetime import datetime
from functools import lru_cache, reduce
from itertools import chain, combinations, permutations, product

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from PIL import Image
from tqdm import tqdm

cur_dir = os.path.dirname(os.path.abspath(__file__))
par_dir = os.path.dirname(cur_dir)
sys.path.append(par_dir)

from util.general_util import load_input, timer

last_dir = str(os.path.basename(os.path.normpath(cur_dir)))
cur_day = re.findall(r"\d+", last_dir)
cur_day = int(cur_day[0]) if len(cur_day) > 0 else datetime.today().day
images_path = os.path.join(par_dir, "images")


def build_graph(nodes):
    G = nx.DiGraph()
    G.add_nodes_from(nodes.keys())
    edges = [(node, edge) for node, edges in nodes.items() for edge in edges]
    G.add_edges_from(edges)
    return G


def draw_graph(G, path, start_node, end_node):
    # Draw the graph
    pos = nx.spring_layout(G)  # positions for all nodes
    fig = plt.figure(figsize=(15, 6))
    nx.draw(G, pos, node_color="blue", edge_color="gray", node_size=10)
    nx.draw_networkx_nodes(G, pos, nodelist=path, node_color="r", node_size=3)
    nx.draw_networkx_edges(
        G, pos, edgelist=list(zip(path, path[1:])), edge_color="r", width=1
    )
    nx.draw_networkx_nodes(
        G, pos, nodelist=[start_node], node_color="green", node_size=60
    )
    nx.draw_networkx_nodes(
        G, pos, nodelist=[end_node], node_color="purple", node_size=60
    )
    plt.savefig(os.path.join(images_path, f"day_{cur_day}_task_1.png"), dpi=300)


@timer(return_time=True)
def task1(instructions, nodes, do_viz=False):
    total_steps = 0
    cur, target = "AAA", "ZZZ"
    path = [cur]

    while cur != target:
        for instr in instructions:
            total_steps += 1
            cur = nodes[cur][instr]
            path.append(cur)

    if do_viz:
        G = build_graph(nodes)
        draw_graph(G, path, "AAA", "ZZZ")

    return total_steps


@timer(return_time=True)
def task2(instructions, nodes):
    total_steps = 0
    curs = set([s for s in nodes if s.endswith("A")])
    targets = set(t for t in nodes if t.endswith("Z"))
    solutions = []

    while targets and curs:
        for instr in instructions:
            total_steps += 1
            curs = {nodes[c][instr] for c in curs}
            for c in curs.intersection(targets):
                solutions.append(total_steps)
                curs.remove(c)
                targets.remove(c)
    return reduce(math.lcm, solutions)


def main():
    # Choose between the real input or the example input
    day_input = load_input(os.path.join(cur_dir, "input.txt")).splitlines()
    # day_input = load_input(os.path.join(cur_dir, "example_input.txt")).splitlines()

    instructions = day_input[0].replace("R", "1").replace("L", "0")
    instructions = [int(i) for i in instructions]

    nodes = [l.replace("(", "").replace(")", "") for l in day_input[2:]]
    nodes = {
        node.split(" = ")[0]: [tn for tn in node.split(" = ")[1].split(", ")]
        for node in nodes
    }

    # Call the tasks and store their results (if needed)
    result_task1, time_task1 = task1(instructions, nodes, do_viz=True)
    result_task2, time_task2 = task2(instructions, nodes)

    print(f"\nDay {cur_day}")
    print("------------------")
    # Print the results
    print("\nAnswers:")
    print(f"Task 1: {result_task1}")
    print(f"Task 2: {result_task2}")

    print("\nTimes:")
    print(f"Task 1: {time_task1:.6f} seconds")
    print(f"Task 2: {time_task2:.6f} seconds")

    # Day 8
    # ------------------

    # Answers:
    # Task 1: 20513
    # Task 2: 15995167053923

    # Times:
    # Task 1: 0.000499 seconds
    # Task 2: 0.013520 seconds


if __name__ == "__main__":
    main()
