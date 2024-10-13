# gbfs.py

import heapq
from neo4j_operation import get_family_tree, get_root_ancestors
import streamlit as st

# Fungsi Heuristik yang Diperbarui
def heuristic(current, target, family_tree, depth=0):
    if current == target:
        return 0
    # Tentukan hubungan dan beratnya berdasarkan generasi
    # Semakin jauh generasinya, semakin tinggi beratnya
    relations = {
        'spouse': 1*5,
        'children': 2*5 + depth,
        'siblings': 2*5 + depth,
        'father': 2*5 + depth,
        'mother': 2*5 + depth,
        'uncles_aunts': 3*5 + depth,
        'cousins': 4*5 + depth,
        'inlaws': 5*5 + depth
    }
    min_h = 20*5 - depth * 5 # Default heuristic value bertambah dengan kedalaman
    data = family_tree.get(current, {})
    for rel, weight in relations.items():
        neighbor = data.get(rel)
        if isinstance(neighbor, list):
            if target in neighbor:
                min_h = min(min_h, weight)
        elif neighbor == target:
            min_h = min(min_h, weight)
    return min_h

# Fungsi Greedy Best-First Search dengan Heuristik yang Diperbarui
def find_person_greedy(family_tree, target_person, max_level=20):
    steps = []
    found = False

    # Initialize priority queue
    priority_queue = []
    visited = set()

    # Get root ancestors and prioritize starting from specific individuals
    initial_persons = get_root_ancestors(family_tree)
    initial_persons_ordered = []
    if 'Abdul Muthalib' in initial_persons:
        initial_persons_ordered.append('Abdul Muthalib')
        initial_persons.remove('Abdul Muthalib')
    if 'Wahab bin Abdu Manaf' in initial_persons:
        initial_persons_ordered.append('Wahab bin Abdu Manaf')
        initial_persons.remove('Wahab bin Abdu Manaf')
    initial_persons_ordered.extend(initial_persons)

    # Add initial persons to the priority queue
    for initial_person in initial_persons_ordered:
        initial_h = heuristic(initial_person, target_person, family_tree, depth=0)
        heapq.heappush(priority_queue, (initial_h, [initial_person]))
        steps.append({
            "Action": "Add to Queue",
            "Person": initial_person,
            "Path": initial_person,
            "h(n)": initial_h
        })

    # Start the Greedy search
    while priority_queue:
        current_h, path = heapq.heappop(priority_queue)
        current = path[-1]
        depth = len(path) - 1  # Depth dihitung dari jalur

        if current in visited:
            continue

        visited.add(current)
        steps.append({
            "Action": "Visit",
            "Person": current,
            "Path": " -> ".join(path),
            "h(n)": current_h
        })

        if current == target_person:
            found = True
            break

        # Get neighbors (relationships)
        neighbors = []
        data = family_tree.get(current, {})
        for relation in ['spouse', 'father', 'mother', 'children', 'siblings', 'uncles_aunts', 'cousins', 'inlaws']:
            neighbor = data.get(relation)
            if isinstance(neighbor, list):
                neighbors.extend(neighbor)
            elif neighbor:
                neighbors.append(neighbor)

        # Add neighbors to the priority queue
        for neighbor in neighbors:
            if neighbor not in visited:
                new_path = path + [neighbor]
                hn = heuristic(neighbor, target_person, family_tree, depth=len(new_path) -1)
                heapq.heappush(priority_queue, (hn, new_path))
                steps.append({
                    "Action": "Add to Queue",
                    "Person": neighbor,
                    "Path": " -> ".join(new_path),
                    "h(n)": hn
                })

    return steps, found
