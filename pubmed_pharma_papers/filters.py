from typing import List
from .models import Paper, Author

NON_ACADEMIC_KEYWORDS = [
    "pharma", "biotech", "inc", "corp", "gmbh", "co.", "pvt", "llc", "ltd"
]

ACADEMIC_KEYWORDS = [
    "university", "college", "institute", "school", "hospital", "centre", "department", "faculty", "nih", "gov"
]

def is_non_academic(affiliation: str) -> bool:
    affil = affiliation.lower()
    return (not any(keyword in affil for keyword in ACADEMIC_KEYWORDS)) and \
           any(keyword in affil for keyword in NON_ACADEMIC_KEYWORDS)

def filter_non_academic_authors(paper: Paper) -> Paper:
    non_acads = [a for a in paper.company_affiliations if is_non_academic(a)]
    paper.non_academic_authors = [a for a in paper.non_academic_authors if is_non_academic(a.affiliation)]
    return paper

