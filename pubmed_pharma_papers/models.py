from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class Author:
    name: str
    affiliation: Optional[str] = None
    email: Optional[str] = None

@dataclass
class Paper:
    pubmed_id: str
    title: str
    publication_date: str
    authors: List[Author] = field(default_factory=list)
    non_academic_authors: List[Author] = field(default_factory=list)
    company_affiliations: List[str] = field(default_factory=list)
    corresponding_author_email: Optional[str] = None  
