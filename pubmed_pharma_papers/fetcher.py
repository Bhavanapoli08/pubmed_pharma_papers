# pubmed_pharma_papers/fetcher.py

from typing import List, Dict
import requests
import lxml.etree as ET


# Required by PubMed API to identify your client
HEADERS = {
    "User-Agent": "pubmed-fetcher-cli/0.1 (contact: bhavanapoli61@gmail.com)"
}


def fetch_pubmed_ids(query: str, max_results: int = 20) -> List[str]:
    """
    Fetches a list of PubMed IDs for a given query.
    """
    url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    params = {
        "db": "pubmed",
        "term": query,
        "retmax": max_results,
        "retmode": "json",
        "tool": "pubmed-fetcher-cli",
        "email": "bhavanapoli61@gmail.com"
    }

    response = requests.get(url, params=params, headers=HEADERS)
    response.raise_for_status()

    try:
        data = response.json()
    except requests.exceptions.JSONDecodeError:
        print("❌ PubMed returned non-JSON response. Raw response below:")
        print(response.text[:1000])
        raise

    return data.get("esearchresult", {}).get("idlist", [])


def fetch_pubmed_details(pubmed_ids: List[str]) -> List[Dict]:
    """
    Fetches detailed information for a list of PubMed IDs.
    """
    url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
    params = {
        "db": "pubmed",
        "id": ",".join(pubmed_ids),
        "retmode": "xml"
    }

    response = requests.get(url, params=params, headers=HEADERS)
    response.raise_for_status()

    root = ET.fromstring(response.content)
    results = []

    for article in root.findall(".//PubmedArticle"):
        paper = {
            "PubmedID": article.findtext(".//PMID"),
            "Title": article.findtext(".//ArticleTitle"),
            "PublicationDate": article.findtext(".//PubDate/Year"),
            "Authors": [],
            "Emails": [],
            "Affiliations": [],
        }

        for author in article.findall(".//Author"):
            name = (
                (author.findtext("ForeName") or "") +
                " " +
                (author.findtext("LastName") or "")
            ).strip()
            aff = author.findtext(".//AffiliationInfo/Affiliation")
            if name and aff:
                paper["Authors"].append(name)
                paper["Affiliations"].append(aff)
                if "@" in aff:
                    paper["Emails"].append(aff)

        results.append(paper)

    return results

