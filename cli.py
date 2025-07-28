import argparse
from rich import print
from pubmed_pharma_papers.api_client import fetch_pubmed_ids, fetch_paper_details
from pubmed_pharma_papers.filters import filter_non_academic_authors
from pubmed_pharma_papers.csv_writer import write_csv

def main():
    parser = argparse.ArgumentParser(description="Fetch PubMed papers with non-academic authors.")
    parser.add_argument("query", type=str, help="PubMed search query")
    parser.add_argument("-f", "--file", type=str, help="CSV filename to write output")
    parser.add_argument("-d", "--debug", action="store_true", help="Enable debug logs")
    args = parser.parse_args()

    if args.debug:
        print(f"[cyan]Fetching results for query:[/] {args.query}")

    ids = fetch_pubmed_ids(args.query)
    papers = []
    for pid in ids:
        paper = fetch_paper_details(pid)
        papers.append(filter_non_academic_authors(paper))
        if args.debug:
            print(f"[green]Processed:[/] {pid}")

    if args.file:
        write_csv(papers, args.file)
        print(f"[bold green]Saved results to {args.file}[/]")
    else:
        for paper in papers:
            print(f"[bold]{paper.title}[/] ({paper.publication_date}) - ID: {paper.pubmed_id}")

if __name__ == "__main__":
    main()
