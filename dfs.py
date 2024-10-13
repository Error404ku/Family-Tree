# dfs.py

from neo4j_operation import get_family_tree, get_root_ancestors

# Fungsi untuk mendapatkan semua leluhur
def get_ancestors(family_tree, person, max_level=20, dfs_steps=None):
    ancestors = []
    visited = set()
    stack = []
    father = family_tree[person].get('father')
    if father:
        stack.append({'current': father, 'level': 1, 'side': 'ayah'})
    mother = family_tree[person].get('mother')
    if mother:
        stack.append({'current': mother, 'level': 1, 'side': 'ibu'})

    while stack:
        node = stack.pop()
        current = node['current']
        level = node['level']
        side = node['side']
        key = (current, side)
        if current and current in family_tree and level <= max_level and key not in visited:
            visited.add(key)
            if dfs_steps is not None:
                dfs_steps.append({
                    "Action": "Visit",
                    "Person": current,
                    "Level": level,
                    "Side": side
                })
            father = family_tree[current].get('father')
            mother = family_tree[current].get('mother')
            # Tentukan relasi
            if level == 1:
                relation = "ayah" if side == "ayah" else "ibu"
            else:
                is_male = family_tree[current]['gender'] == 'male'
                ancestor_type = "kakek" if is_male else "nenek"
                generation = level - 1
                if generation == 1:
                    relation = f"{ancestor_type} dari {side}"
                else:
                    relation = f"{ancestor_type} ke-{generation -1} dari {side}"
            ancestors.append({"Relasi": relation, "Nama": f"{current} ({family_tree[current]['gender']})"})
            # Tambahkan ke stack
            if father:
                if dfs_steps is not None:
                    dfs_steps.append({
                        "Action": "Add to Stack",
                        "Person": father,
                        "Level": level +1,
                        "Side": side
                    })
                stack.append({'current': father, 'level': level +1, 'side': side})
            if mother:
                if dfs_steps is not None:
                    dfs_steps.append({
                        "Action": "Add to Stack",
                        "Person": mother,
                        "Level": level +1,
                        "Side": side
                    })
                stack.append({'current': mother, 'level': level +1, 'side': side})
    return ancestors

# Fungsi untuk mendapatkan semua keturunan
def get_descendants(family_tree, person, max_level=20, dfs_steps=None):
    descendants = []
    visited = set()
    stack = [{'current': person, 'level': 0}]  # Mulai dengan level 0 untuk generasi 1

    # Dictionary untuk menghitung nomor anak per generasi
    generation_counters = {}

    while stack:
        node = stack.pop()
        current = node['current']
        level = node['level']

        if level >= max_level or current not in family_tree:
            continue

        if current not in visited:
            visited.add(current)
            if dfs_steps is not None:
                dfs_steps.append({
                    "Action": "Visit",
                    "Person": current,
                    "Level": level
                })

            children = family_tree[current]["children"]

            for child in reversed(children):  # reverse untuk LIFO
                if child not in visited:
                    # Hitung generasi untuk anak
                    generasi = level + 1  # generasi 1 untuk anak langsung

                    # Inisialisasi counter untuk generasi ini jika belum ada
                    if generasi not in generation_counters:
                        generation_counters[generasi] = 1
                    else:
                        generation_counters[generasi] += 1

                    # Tentukan nomor anak ke
                    anak_ke = generation_counters[generasi]

                    relation = f"anak ke-{anak_ke} dari generasi {generasi}"

                    descendants.append({"Relasi": relation, "Nama": f"{child} ({family_tree[child]['gender']})"})

                    if dfs_steps is not None:
                        dfs_steps.append({
                            "Action": "Add to Stack",
                            "Person": child,
                            "Level": level + 1
                        })

                    stack.append({'current': child, 'level': level +1})

        else:
            if dfs_steps is not None:
                dfs_steps.append({
                    "Action": "Backtrack",
                    "Person": current,
                    "Level": level
                })
    return descendants

# Fungsi DFS
def find_person_dfs(family_tree, target_person, max_level=20):
    steps = []
    found = False

    visited = set()
    stack = []

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
