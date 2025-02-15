import re
import os
import argparse
from typing import Dict, List
from src.models.models import Ticket
from src.github.github_manager import GitHubManager
from dotenv import load_dotenv
import glob

def parse_obsidian_note(file_path: str) -> Dict[str, List[Ticket]]:
    """
    Parse an Obsidian markdown file and extract repository and ticket information.
    
    Format:
    git RepoName.md
    Ticket: #tag Title
    - Description point 1
    - Description point 2
    
    Args:
        file_path: Path to the markdown file
        
    Returns:
        Dictionary with repo names as keys and lists of Ticket objects as values
    """
    print(f"Opening file: {file_path}")
    
    repos = {}
    current_repo = None
    current_ticket = None
    
    # Extract repo name from filename if it starts with 'git '
    # Get just the filename from the path
    filename = os.path.basename(file_path)
    if filename.lower().startswith('git '):
        current_repo = filename.replace('.md', '')[4:].strip()
        repos[current_repo] = []
        print(f"Found repository from filename: {current_repo}")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            print(f"Read {len(lines)} lines")
        
        for line in lines:
            line = line.strip()
            
            # Skip empty lines
            if not line:
                continue
            
            print(f"Processing line: {line}")
            
            # Look for ticket declarations
            if line.startswith('Ticket:'):
                if current_ticket and current_repo:
                    repos[current_repo].append(current_ticket)
                
                ticket_content = line[7:].strip()
                tags = re.findall(r'#(\w+)', ticket_content)
                title = re.sub(r'#\w+', '', ticket_content).strip()
                
                current_ticket = Ticket(
                    title=title,
                    tags=tags,
                    description=[],
                    repo_name=current_repo
                )
                print(f"Found ticket: {title} with tags: {tags}")
                
            # Look for description bullet points
            elif line.startswith('-') and current_ticket:
                description_point = line[1:].strip()
                current_ticket.description.append(description_point)
                print(f"Added description point: {description_point}")
                
        # Don't forget to add the last ticket
        if current_ticket and current_repo:
            repos[current_repo].append(current_ticket)
            
    except FileNotFoundError:
        print(f"Error: Could not find file {file_path}")
        return {}
    except Exception as e:
        print(f"Error processing file: {str(e)}")
        return {}
    
    print(f"\nFound {len(repos)} repositories")
    for repo, tickets in repos.items():
        print(f"Repository '{repo}' has {len(tickets)} tickets")
    
    return repos

def process_directory(directory_path: str, github_token: str) -> None:
    """
    Process all git-prefixed markdown files in a directory.
    
    Args:
        directory_path: Path to directory containing markdown files
        github_token: GitHub authentication token
    """
    # Initialize GitHub manager
    gh_manager = GitHubManager(github_token)
    
    # Find all markdown files starting with 'git '
    git_files = glob.glob(os.path.join(directory_path, "git *.md"))
    
    if not git_files:
        print(f"No git-prefixed markdown files found in {directory_path}")
        return
        
    print(f"Found {len(git_files)} git-prefixed files")
    
    # Process each file
    for file_path in git_files:
        print(f"\nProcessing file: {file_path}")
        repos = parse_obsidian_note(file_path)
        
        if not repos:
            print("No repositories or tickets found in this file!")
            continue
            
        # Process each repository and its tickets
        for repo_name, tickets in repos.items():
            print(f"\nProcessing repository: {repo_name}")
            if gh_manager.process_tickets(repo_name, tickets):
                print(f"Successfully processed all tickets for {repo_name}")
            else:
                print(f"Some errors occurred while processing {repo_name}")

if __name__ == "__main__":
    # Set up argument parser
    parser = argparse.ArgumentParser(
        description='Convert Obsidian notes into GitHub repositories and issues.'
    )
    parser.add_argument(
        '-d', '--directory',
        default='examples',
        help='Directory containing git-prefixed markdown files (default: examples)'
    )
    parser.add_argument(
        '--obsidian-vault',
        help='Path to your Obsidian vault directory'
    )

    args = parser.parse_args()

    # Load GitHub token from environment
    load_dotenv()
    github_token = os.getenv('GITHUB_TOKEN')
    
    if not github_token:
        print("Error: GITHUB_TOKEN not found in environment variables")
        exit(1)
    
    # Use obsidian vault path if provided, otherwise use directory argument
    directory = args.obsidian_vault if args.obsidian_vault else args.directory
    print(f"\nProcessing markdown files in: {directory}")
    process_directory(directory, github_token) 