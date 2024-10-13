# dfs.py

def find_person_dfs(family_tree, target_person, max_level=20):
    steps = []
    found = False

    visited = set()
    stack = []

    # Fungsi untuk menemukan leluhur tertinggi
    def get_root_ancestors(family_tree):
        root_ancestors = []
        for person, data in family_tree.items():
            if not data.get('father') and not data.get('mother'):
                root_ancestors.append(person)
        return root_ancestors

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

    # Add initial persons to the stack
    for initial_person in reversed(initial_persons_ordered):  # reversed for LIFO
        stack.append([initial_person])
        steps.append({
            "Action": "Add to Stack",
            "Person": initial_person,
            "Path": initial_person
        })

    # Start the DFS
    while stack:
        path = stack.pop()
        current = path[-1]

        if current in visited:
            continue

        visited.add(current)
        steps.append({
            "Action": "Visit",
            "Person": current,
            "Path": " -> ".join(path)
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

        # Add neighbors to the stack
        for neighbor in reversed(neighbors):  # reversed for LIFO
            if neighbor not in visited:
                new_path = path + [neighbor]
                stack.append(new_path)
                steps.append({
                    "Action": "Add to Stack",
                    "Person": neighbor,
                    "Path": " -> ".join(new_path)
                })

    return steps, found
