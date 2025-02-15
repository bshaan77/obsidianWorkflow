from dataclasses import dataclass
from typing import List, Optional

@dataclass
class Ticket:
    title: str
    tags: List[str]
    description: List[str]
    repo_name: Optional[str] = None 