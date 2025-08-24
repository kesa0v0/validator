import os
import hashlib
import argparse
import json
from pathlib import Path

def hash_file(filepath):
    """Computes the SHA256 hash of a file."""
    sha256_hash = hashlib.sha256()
    try:
        with open(filepath, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    except IOError as e:
        print(f"Error reading file {filepath}: {e}")
        return None

def hash_directory_tree(root_path: Path):
    """
    Hashes all files in a directory tree and returns a dictionary of
    relative_path: hash.
    """
    hashes = {}
    for item in sorted(root_path.rglob('*')):
        if item.is_file():
            relative_path = item.relative_to(root_path).as_posix()
            file_hash = hash_file(item)
            if file_hash:
                hashes[relative_path] = file_hash
    return hashes

def generate_hashes(directory, output_file):
    """Generates and saves the hash manifest."""
    print(f"Generating hashes for directory: {directory}")
    root_path = Path(directory)
    if not root_path.is_dir():
        print(f"Error: Directory not found at '{directory}'")
        return

    hashes = hash_directory_tree(root_path)

    try:
        with open(output_file, 'w') as f:
            json.dump(hashes, f, indent=4)
        print(f"Successfully created hash manifest at: {output_file}")
    except IOError as e:
        print(f"Error writing to output file {output_file}: {e}")


def compare_hashes(directory, compare_file):
    """Compares the directory against a hash manifest."""
    print(f"Comparing directory '{directory}' with manifest '{compare_file}'")
    
    compare_path = Path(compare_file)
    if not compare_path.is_file():
        print(f"Error: Comparison file not found at '{compare_file}'")
        return

    try:
        with open(compare_path, 'r') as f:
            old_hashes = json.load(f)
    except (IOError, json.JSONDecodeError) as e:
        print(f"Error reading or parsing comparison file: {e}")
        return

    root_path = Path(directory)
    if not root_path.is_dir():
        print(f"Error: Directory not found at '{directory}'")
        return
        
    new_hashes = hash_directory_tree(root_path)

    old_set = set(old_hashes.keys())
    new_set = set(new_hashes.keys())

    added_files = sorted(list(new_set - old_set))
    removed_files = sorted(list(old_set - new_set))
    common_files = old_set.intersection(new_set)

    modified_files = []
    for f in sorted(list(common_files)):
        if old_hashes[f] != new_hashes[f]:
            modified_files.append(f)

    if not added_files and not removed_files and not modified_files:
        print("\nResult: No changes detected.")
    else:
        print("\n--- Comparison Result ---")
        if added_files:
            print("\n[ADDED]")
            for f in added_files:
                print(f"+ {f}")
        if removed_files:
            print("\n[REMOVED]")
            for f in removed_files:
                print(f"- {f}")
        if modified_files:
            print("\n[MODIFIED]")
            for f in modified_files:
                print(f"~ {f}")
        print("\n-------------------------")


def main():
    parser = argparse.ArgumentParser(
        description="Create or compare a hash manifest for a directory."
    )
    parser.add_argument(
        '-d', '--directory',
        type=str,
        default='.',
        help="The path to the directory to process. Defaults to the current directory."
    )
    
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        '-o', '--output',
        type=str,
        help="Generate a hash manifest and save it to the specified JSON file path."
    )
    group.add_argument(
        '-c', '--compare',
        type=str,
        help="Compare the directory against the specified hash manifest JSON file."
    )

    args = parser.parse_args()

    if args.output:
        generate_hashes(args.directory, args.output)
    elif args.compare:
        compare_hashes(args.directory, args.compare)

if __name__ == "__main__":
    main()