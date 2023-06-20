# CodeCloneCrawler Project

This Python project uses the libraries `requests`, `beautifulsoup4`, and `lxml` for web scraping.

## Prerequisites

Ensure you have Python 3.10 installed on your machine. You can verify the installation by running the following command in the terminal:

```bash
python --version
```

This should output something like **'Python 3.10.x'**

Ensure you have the following Python packages installed. You can 

- requests
- beautifulsoup4
- lxml

You can install these packages using pip:

```bash
pip install requests beautifulsoup4 lxml
```

## Setup

To set up the project, follow the steps given below:

### Step 1: Clone the repository

Clone the repository to your local machine.

```bash
git clone https://github.com/C00pster/CodeCloneCrawler.git
```

### Step 2: Ensure competitions directory is present

The 'competitions' directory must be present in the root directory of the project, i.e., at the same level as the repository.

## Usage

Navigate to the root directory of the project and run the crawler with the following command:

```bash
python crawler.py
```

The crawler will start running and scraping the required information.

If there are any errors during the scraping process, they will be logged in the following files:

- `constraints_errors.txt`: URLs where there was an error getting the constraints.
- `input_errors.txt`: URLs where there was an error getting the input.
- `output_errors.txt`: URLs where there was an error getting the output.
- `problem_statement_errors.txt`: URLs where there was an error getting the problem statement.
- `sample_input_output_errors.txt`: URLs where there was an error getting any of the sample inputs or sample outputs.
- `score_errors.txt`: URLs where there was an error getting the score.

Please check these files to understand where and what kind of errors occurred during the scraping process.