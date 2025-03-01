# Obsidian to GitHub Workflow

Convert Obsidian notes into GitHub repositories and issues automatically. This tool scans markdown files with the `git` prefix and creates corresponding GitHub repositories with issues based on the content.

## Features

- Automatically creates GitHub repositories from Obsidian notes
- Converts markdown tickets into GitHub issues
- Supports tags and descriptions
- Handles multiple repositories and tickets
- Preserves markdown formatting

## Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/obsidianWorkflows.git
cd obsidianWorkflows
```

2. Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -e .
```

## Configuration

1. Create a GitHub Personal Access Token:

   - Go to GitHub.com → Settings → Developer settings → Personal access tokens → Tokens (classic)
   - Generate new token with `repo` scope
   - Copy the token

2. Create a `.env` file in the project root:

```plaintext
GITHUB_TOKEN=your_github_token_here
```

## Usage

### File Format

Create Obsidian notes with the following format:

```markdown
Ticket: #tag Your ticket title

- Description point 1
- Description point 2
```

Name your files with the `git` prefix to indicate repository creation:

- `git MyProject.md`
- `git AnotherRepo.md`

### Running the Tool

There are several ways to run the tool:

1. Using the default examples directory:

```bash
python -m src.parser.obsidian_parser
```

2. Specifying a custom directory:

```bash
python -m src.parser.obsidian_parser --directory /path/to/your/notes
```

3. Directly using your Obsidian vault:

```bash
python -m src.parser.obsidian_parser --obsidian-vault /path/to/obsidian/vault
```

> **Note about Obsidian Vaults**: An Obsidian vault is simply the folder where you store
> your Obsidian notes. This is typically found in:
>
> - Windows: `C:\Users\YourName\Documents\Obsidian\YourVaultName`
> - Mac: `/Users/YourName/Documents/Obsidian/YourVaultName`
> - Linux: `/home/YourName/Documents/Obsidian/YourVaultName`

The tool will only process markdown files that start with `git ` in the specified directory.
All other files will be left untouched.

Available options:

- `-d, --directory`: Specify a directory containing git-prefixed markdown files
- `--obsidian-vault`: Directly specify your Obsidian vault location

## Project Structure

```
obsidianWorkflows/
├── src/
│   ├── parser/         # Markdown parsing logic
│   ├── github/         # GitHub integration
│   └── models/         # Data models
├── examples/           # Example markdown files
└── docs/              # Documentation
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

[MIT](https://choosealicense.com/licenses/mit/)
