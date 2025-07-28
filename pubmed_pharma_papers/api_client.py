import requests
import xml.etree.ElementTree as ET
from typing import List, Optional
from .models import Author, Paper


def fetch_pubmed_ids(query: str, max_results: int = 10) -> List[str]:
    """
    Fetches a list of PubMed IDs for the given query using esearch.
    Returns up to `max_results` PMIDs.
    """
    url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    params = {
        "db": "pubmed",
        "term": query,
        "retmode": "json",
        "retmax": max_results
    }
    headers = {
        "Accept": "application/json"
    }

    response = requests.get(url, params=params, headers=headers)

    if response.status_code != 200:
        raise RuntimeError(f"PubMed API error {response.status_code}: {response.text}")

    try:
        data = response.json()
        return data.get("esearchresult", {}).get("idlist", [])
    except requests.exceptions.JSONDecodeError as e:
        raise RuntimeError(f"Invalid JSON response from PubMed: {response.text}") from e


def fetch_paper_details(pubmed_id: str) -> Paper:
    """
    Fetches detailed paper metadata using efetch for a given PubMed ID.
    Parses XML and extracts title, publication date, authors, affiliations, and email.
    """
    url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
    params = {
        "db": "pubmed",
        "id": pubmed_id,
        "retmode": "xml"
    }

    response = requests.get(url, params=params)
    response.raise_for_status()

    root = ET.fromstring(response.content)
    article = root.find(".//PubmedArticle")
    if article is None:
        raise ValueError(f"No article data found for PubMed ID: {pubmed_id}")

    # Title
    title = article.findtext(".//ArticleTitle") or "No Title"

    # Publication Date
    year = article.findtext(".//PubDate/Year")
    medline_date = article.findtext(".//PubDate/MedlineDate")
    pub_date = year or medline_date or "Unknown"

    # Authors & Affiliations
    authors: List[Author] = []
    affiliations: List[str] = []
    corresponding_email: Optional[str] = None

    for author in article.findall(".//Author"):
        fore_name = author.findtext("ForeName", "")
        last_name = author.findtext("LastName", "")
        full_name = f"{fore_name} {last_name}".strip()

        affiliation = author.findtext("AffiliationInfo/Affiliation") or ""
        email = None
        if "@" in affiliation:
            # Crude email extraction
            for part in affiliation.split():
                if "@" in part:
                    email = part
                    break

        # Set corresponding author email if available
        if corresponding_email is None and email:
            corresponding_email = email

        if full_name or affiliation:
            authors.append(Author(name=full_name, affiliation=affiliation, email=email))
            affiliations.append(affiliation)

    return Paper(
        pubmed_id=pubmed_id,
        title=title,
        publication_date=pub_date,
        non_academic_authors=authors,  # Will be filtered later
        company_affiliations=affiliations,
        corresponding_author_email=corresponding_email
    )
