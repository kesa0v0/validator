# Directory Hash Manifest Tool

A Python script to create a manifest of file hashes for a directory and compare it against that manifest at a later time to detect changes. This is useful for verifying file integrity, tracking changes in a directory, or ensuring a file transfer was successful.

## Description

This tool provides two main functions:

1. **Generate Manifest (`-o`, `--output`):** Scans a directory recursively and creates a JSON file (`manifest`) containing the relative paths and SHA256 hashes of all files found.
2. **Compare with Manifest (`-c`, `--compare`):** Compares the files in a directory against a previously generated manifest file. It reports any files that have been added, removed, or modified since the manifest was created.

## Requirements

- Python 3.6+
- No external libraries are required.

## Usage

All commands are run from your terminal or command prompt.

### Creating a Hash Manifest

To generate a `hashes.json` file for the files in the `data` directory:

```bash
python hasher.py --output hashes.json --directory ./data
```

If you omit the `--directory` argument, it will scan the current directory by default.

```bash
# Creates 'manifest.json' for the current directory
python hasher.py -o manifest.json
```

### Comparing a Directory with a Manifest

To check for changes in the `data` directory against the `hashes.json` manifest:

```bash
python hasher.py --compare hashes.json --directory ./data
```

The output will clearly list any added, removed, or modified files. If there are no changes, it will report that as well.

### Command-Line Arguments

- `-o, --output <FILE_PATH>`: **Generate Mode**. Creates a new hash manifest and saves it to the specified file path.
- `-c, --compare <FILE_PATH>`: **Compare Mode**. Compares the target directory against the specified manifest file.
- `-d, --directory <DIR_PATH>`: Specifies the target directory to scan. Defaults to the current directory (`.`) if not provided.

## Future Improvements

Here are some ideas for potential future enhancements:

- **Ignore Patterns:** Add a feature to read a `.ignore` file (similar to `.gitignore`) to exclude specific files or directories from the hashing process.
- **Different Hash Algorithms:** Allow the user to choose a different hashing algorithm (e.g., MD5, SHA1) via a command-line flag.
- **Verbose Mode:** Include a `-v` or `--verbose` flag to print every file being processed, which can be useful for large directories.
- **Update Manifest:** Add a function to update an existing manifest file instead of overwriting it, which could be more efficient for large directories with few changes.
- **GUI:** For non-technical users, a simple graphical user interface could be developed to perform the generate and compare actions.

## Using with Docker

With Docker, you can run the script without installing Python on your host machine. The provided `Dockerfile` sets up the necessary environment.

### 1. Build the Docker Image

First, build the image from the `Dockerfile` in the project root:

```bash
docker build -t directory-hasher .
```

### 2. Run the Container

To use the script, you must mount the host directory you want to scan into the container. We will mount the host directory to the `/app/data` directory inside the container.

**Creating a Manifest:**

```bash
docker run --rm -v "C:\path\to\your\data:/app/data" directory-hasher -o data/manifest.json -d data
```

- `--rm`: Automatically removes the container when it finishes.
- `-v "C:\path\to\your\data:/app/data"`: Mounts your local directory into the container. **You must replace `C:\path\to\your\data` with the absolute path to your target directory.**
- `directory-hasher`: The name of the image we just built.
- The arguments `-o data/manifest.json -d data` are for the script, and the paths are relative to the container's workdir (`/app`). The output `manifest.json` will be saved in your host directory.

**Comparing a Manifest:**

```bash
docker run --rm -v "C:\path\to\your\data:/app/data" directory-hasher -c data/manifest.json -d data
```

The command is very similar. The script will read the manifest from the mounted directory on your host and perform the comparison.
