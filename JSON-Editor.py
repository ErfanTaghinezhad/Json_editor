import os
import json

def get_directory():
    while True:
        directory = input("Enter the path to the JSON files folder (e.g., data): ").strip()
        if os.path.isdir(directory):
            return directory
        else:
            print("Directory not found. Please try again.")

def find_json_files(directory):
    json_files = [file for file in os.listdir(directory) if file.lower().endswith('.json')]
    if not json_files:
        print("No JSON files found in the specified directory.")
        exit()
    print("\nJSON files available:")
    for idx, file in enumerate(json_files, 1):
        print(f"{idx}. {file}")
    return json_files

def choose_files(json_files):
    selection = input("\nSelect files to edit by numbers separated by commas (e.g., 1,3) or type 'all': ").strip().lower()
    if selection == 'all':
        return json_files
    selected = []
    try:
        indices = selection.split(',')
        for index in indices:
            index = index.strip()
            if index.isdigit() and 1 <= int(index) <= len(json_files):
                selected.append(json_files[int(index)-1])
            else:
                print(f"Ignoring invalid selection: {index}")
    except:
        print("Invalid input. Selecting all files by default.")
        return json_files
    return selected if selected else json_files

def load_json(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
            if isinstance(data, list):
                return data
            else:
                print(f"{os.path.basename(filepath)} does not contain a list of objects.")
                return []
    except json.JSONDecodeError as e:
        print(f"Error reading {os.path.basename(filepath)}: {e}")
        return []

def show_sample(data):
    if not data:
        print("No data to display.")
        return
    print("\nSample data entries:")
    for entry in data[:3]:
        print(json.dumps(entry, ensure_ascii=False, indent=4))
    print("...")

def get_user_actions():
    actions = {'delete': [], 'modify': {}, 'rename': {}}
    while True:
        action = input("\nChoose an action - delete, modify, rename, or type 'done' to finish: ").strip().lower()
        if action == 'delete':
            key = input("Key to delete: ").strip()
            if key:
                actions['delete'].append(key)
        elif action == 'modify':
            key = input("Key to modify: ").strip()
            new_val = input(f"New value for '{key}': ").strip()
            if key:
                actions['modify'][key] = new_val
        elif action == 'rename':
            old_key = input("Key to rename: ").strip()
            new_key = input(f"New name for '{old_key}': ").strip()
            if old_key and new_key:
                actions['rename'][old_key] = new_key
        elif action == 'done':
            break
        else:
            print("Unknown action. Please choose from delete, modify, rename, or done.")
    # Remove empty actions
    actions = {k: v for k, v in actions.items() if v}
    return actions

def apply_changes(data, actions):
    for item in data:
        # Delete keys
        for key in actions.get('delete', []):
            item.pop(key, None)
        # Modify values
        for key, new_val in actions.get('modify', {}).items():
            if key in item:
                item[key] = new_val
        # Rename keys
        for old_key, new_key in actions.get('rename', {}).items():
            if old_key in item:
                item[new_key] = item.pop(old_key)
    return data

def save_changes(directory, filename, data):
    edit_dir = os.path.join(directory, 'edited')
    os.makedirs(edit_dir, exist_ok=True)
    new_path = os.path.join(edit_dir, filename)
    with open(new_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print(f"Saved edited file to {new_path}")

def main():
    print("=== JSON Editor ===")
    directory = get_directory()
    json_files = find_json_files(directory)
    selected_files = choose_files(json_files)
    actions = get_user_actions()
    if not actions:
        print("No actions selected. Exiting.")
        return
    for file in selected_files:
        path = os.path.join(directory, file)
        data = load_json(path)
        if not data:
            continue
        show_sample(data)
        updated_data = apply_changes(data, actions)
        save_changes(directory, file, updated_data)
    print("\nAll selected files have been processed.")

if __name__ == "__main__":
    main()
