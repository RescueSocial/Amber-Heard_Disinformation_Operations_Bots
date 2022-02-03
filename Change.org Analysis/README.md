# SNA-ChangeOrg-AH
Change.org Social Network Analysis on AH's Case Study Example
 - Data Analysis of Petitions, Comments, Accounts, and Signatures with Timings and IDs

## Reverse-engineering the API

Obtain signatures for a petition on Change.org using reverse-engineered API

I use Python 3, you will also need Pandas and Requests installed.

- To look at the reverse-engineering process, check out change.org-signatures.ipynb
- To run the resulting script, run python get_last_signatures_csv.py --help . The notebook above contains an example

## Installation
1. Install [Miniconda](https://docs.conda.io/en/latest/miniconda.html)
2. Create the environment for the project: `conda env create -f environment.yml`
3. Activate the new environment: `conda activate rst-changeorg-data`
4. Run [`./jupyter.sh`](./jupyter.sh) to set up Jupyter
5. Run `jupyter lab` in the command line and navigate to the link provided in the console.

** Full Data collected on 181 petitions by a former Google Research Intern.
