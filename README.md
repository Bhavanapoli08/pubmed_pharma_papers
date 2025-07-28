# PubMed Pharma Papers

A command-line Python tool to fetch PubMed research papers with **at least one author affiliated with a pharmaceutical or biotech company**, based on any user-specified search query. Results are exported as a CSV file.

---

## 📌 Features

- 🔍 Search PubMed using full query syntax (via [Entrez eUtils API](https://www.ncbi.nlm.nih.gov/books/NBK25501/))
- 🧪 Detect non-academic authors using email/affiliation heuristics
- 🧾 Output results to CSV with:
  - `PubmedID`
  - `Title`
  - `Publication Date`
  - `Non-academic Author(s)`
  - `Company Affiliation(s)`
  - `Corresponding Author Email`
- 🖥️ CLI options:
  - `-f` or `--file`: Save to file (CSV)
  - `-d` or `--debug`: Enable debug logs
  - `-h` or `--help`: Show usage instructions

---

## 🚀 Quick Start

### 1. Clone the repo

```bash
git clone https://github.com/Bhavanapoli08/pubmed_pharma_papers.git
cd pubmed_pharma_papers

2. Install dependencies using Poetry
poetry install

3. Run the tool
poetry run get-papers-list "covid vaccine" -f results.csv -d
You’ll find results.csv with the extracted metadata.

Project Structure
pubmed_pharma_papers/
├── __init__.py
├── api_client.py       # Handles PubMed API interactions
├── filters.py          # Filters authors for non-academic affiliations
├── models.py           # Typed dataclass model for papers
├── csv_writer.py       # CSV export logic
├── cli.py              # Command-line interface
pyproject.toml          # Poetry config
README.md

Sample Output
| PubmedID | Title                         | Publication Date | Non-academic Authors       | Company Affiliations | Email |
| -------- | ----------------------------- | ---------------- | -------------------------- | -------------------- | ----- |
| 40710045 | Evaluation of Simultaneous... | 2025             | Soojeong Chang, Jieun Shin | Cellid Co., Ltd.     | —     |


Heuristics for Non-Academic Authors
Authors are flagged as non-academic if their affiliation:

Doesn’t contain words like university, college, institute, school

Contains known company terms like Ltd, Inc, Corp, Biotech, etc.

Tools & Libraries Used
PubMed eUtils API

Poetry

requests

pandas

lxml

rich – for CLI formatting

To gain bonus points:

Create a TestPyPI account: https://test.pypi.org/account/register/

Build your package:
poetry build

Upload to TestPyPI:
poetry config repositories.testpypi https://test.pypi.org/legacy/
poetry publish -r testpypi

Author
Bhavana Poli
📧 bhavanapoli61@gmail.com
🔗 GitHub


