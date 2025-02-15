from github import Github
from typing import List, Optional
from src.models.models import Ticket

class GitHubManager:
    def __init__(self, token: str):
        """Initialize GitHub manager with authentication token."""
        self.gh = Github(token)
        try:
            # Test authentication
            self.user = self.gh.get_user()
            print(f"Successfully authenticated as: {self.user.login}")
            print(f"Token has access to: {[repo.full_name for repo in self.user.get_repos()[:5]]}")
        except Exception as e:
            print(f"Authentication failed: {str(e)}")
            raise

    def format_repo_name(self, repo_name: str) -> str:
        """Format repository name to match GitHub's format."""
        # Replace spaces with hyphens and remove any special characters
        return repo_name.replace(' ', '-')

    def create_or_get_repo(self, repo_name: str) -> Optional[str]:
        """Create a new repository or get existing one."""
        try:
            # Format the name consistently with hyphens
            formatted_name = self.format_repo_name(repo_name)
            full_name = f"{self.user.login}/{formatted_name}"
            
            try:
                # First try to get the repository with hyphenated name
                repo = self.gh.get_repo(full_name)
                print(f"Found existing repository: {repo.full_name}")
                return repo.full_name
            except Exception as e:
                print(f"Could not find repository: {full_name}")
                print(f"Trying alternate formats...")
                
                # Try to find the repo with different format variations
                try:
                    # Try with original name
                    repo = self.user.get_repo(repo_name)
                    print(f"Found existing repository with original name: {repo.full_name}")
                    return repo.full_name
                except:
                    # If all attempts fail, create new repo with hyphenated name
                    print(f"Creating new repository: {formatted_name}")
                    repo = self.user.create_repo(
                        formatted_name,
                        private=True,
                        auto_init=True
                    )
                    print(f"Created new repository: {repo.full_name}")
                    return repo.full_name
            
        except Exception as e:
            print(f"Error creating/getting repository: {str(e)}")
            return None

    def create_issue(self, repo_full_name: str, ticket: Ticket) -> bool:
        """Create a GitHub issue from a ticket."""
        try:
            # Format repository name
            owner, repo_name = repo_full_name.split('/')
            formatted_full_name = f"{owner}/{self.format_repo_name(repo_name)}"
            
            repo = self.gh.get_repo(formatted_full_name)
            
            # Create labels if they don't exist
            existing_labels = [label.name for label in repo.get_labels()]
            for tag in ticket.tags:
                if tag not in existing_labels:
                    print(f"Creating new label: {tag}")
                    repo.create_label(
                        name=tag,
                        color="0366d6"  # GitHub's default blue color
                    )
            
            # Format description
            description = "\n".join([f"- {point}" for point in ticket.description])
            
            # Create issue
            issue = repo.create_issue(
                title=ticket.title,
                body=description,
                labels=ticket.tags
            )
            
            print(f"Created issue: {issue.title} (#{issue.number})")
            return True
            
        except Exception as e:
            print(f"Error creating issue: {str(e)}")
            return False

    def process_tickets(self, repo_name: str, tickets: List[Ticket]) -> bool:
        """Process all tickets for a repository."""
        # Create or get repository
        repo_full_name = self.create_or_get_repo(repo_name)
        if not repo_full_name:
            return False
        
        try:
            # Get repository
            formatted_full_name = f"{self.user.login}/{self.format_repo_name(repo_name)}"
            repo = self.gh.get_repo(formatted_full_name)
            
            # Get existing issues
            existing_issues = {issue.title: issue for issue in repo.get_issues(state='all')}
            
            # Create issues for tickets that don't exist
            success = True
            for ticket in tickets:
                if ticket.title in existing_issues:
                    print(f"Issue already exists: {ticket.title}")
                    continue
                
                if not self.create_issue(repo_full_name, ticket):
                    success = False
                
            return success
            
        except Exception as e:
            print(f"Error processing tickets: {str(e)}")
            return False 