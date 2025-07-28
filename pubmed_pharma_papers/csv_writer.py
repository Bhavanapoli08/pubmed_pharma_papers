import csv
from typing import List
from .models import Paper

def write_csv(papers: List[Paper], filename: str):
    with open(filename, mode="w", newline='', encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "PubmedID", "Title", "Publication Date", 
            "Non-academic Author(s)", "Company Affiliation(s)", "Corresponding Author Email"
        ])
        for paper in papers:
            writer.writerow([
                paper.pubmed_id,
                paper.title,
                paper.publication_date,
                "; ".join([a.name for a in paper.non_academic_authors]),
                "; ".join(paper.company_affiliations),
                paper.corresponding_author_email or ""
            ])
