import csv
import subprocess
import argparse
from github import Github
from github.GithubException import UnknownObjectException

def get_gh_token():
    """
    Retrieve the GitHub authentication token using the GitHub CLI.

    Returns:
        str: The authentication token as a string.
    """
    result = subprocess.run(['gh', 'auth', 'token'], stdout=subprocess.PIPE, text=True)
    return result.stdout.strip()

def ensure_label_exists(repo, label_name):
    """
    Ensure that a label exists in the given repository. If the label does not exist, create it.

    Args:
        repo (github.Repository.Repository): The GitHub repository object.
        label_name (str): The name of the label to ensure.

    Returns:
        github.Label.Label: The existing or newly created label object.
    """
    try:
        return repo.get_label(label_name)
    except UnknownObjectException:
        print(f"Creating label: {label_name}")
        return repo.create_label(name=label_name, color="ededed")

def main(csv_filename):
    """
    Main function to create GitHub issues from a CSV file.

    Args:
        csv_filename (str): The path to the CSV file containing issues.
    """
    ACCESS_TOKEN = get_gh_token()
    REPO_NAME = "your_username/your_repo"  # Replace with your repo, e.g., "example/Hello-World"

    g = Github(ACCESS_TOKEN)
    repo = g.get_repo(REPO_NAME)

    # Open the CSV file with UTF-8-SIG encoding to handle BOM if present
    with open(csv_filename, newline="", encoding="utf-8-sig") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # Read data from the CSV columns
            title = row["Summary"]
            body = row["Description"]
            priority = row["Priority"]

            labels = []
            # Add priority as a label if specified
            if priority.strip():
                labels.append(ensure_label_exists(repo, priority.strip()))

            try:
                issue = repo.create_issue(
                    title=title,
                    body=body,
                    labels=labels
                )
                print(f"Issue created: {issue.title}")
            except Exception as e:
                print(f"Error creating issue '{title}': {e}")

if __name__ == "__main__":
    # Set up command-line argument parsing
    parser = argparse.ArgumentParser(description="Create GitHub issues from a CSV file.")
    parser.add_argument("csv_filename", help="Name of the CSV file, e.g., issues.csv")
    args = parser.parse_args()

    main(args.csv_filename)