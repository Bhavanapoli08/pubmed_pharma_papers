from typing import List
from .models import Paper, Author

NON_ACADEMIC_KEYWORDS = [
    "pharma", "biotech", "inc", "corp", "gmbh", "co.", "pvt", "llc", "ltd", "therapeutics", "biosciences"
]

ACADEMIC_KEYWORDS = [
    "university", "college", "institute", "school", "hospital", "centre",
    "department", "faculty", "nih", "gov", "academia"
]

def is_non_academic(affiliation: str) -> bool:
    affil = affiliation.lower()
    return (
        not any(keyword in affil for keyword in ACADEMIC_KEYWORDS)
        and any(keyword in affil for keyword in NON_ACADEMIC_KEYWORDS)
    )

def filter_non_academic_authors(paper: Paper) -> Paper:
    """Filters authors and affiliations for non-academic institutions"""
    # Filter non-academic authors from full list of authors
    paper.non_academic_authors = [
        author for author in paper.authors
        if author.affiliation and is_non_academic(author.affiliation)
    ]

    # Filter company affiliations
    paper.company_affiliations = [
        aff for aff in paper.company_affiliations
        if is_non_academic(aff)
    ]
    
    return paper


