import csv
import subprocess
import argparse
from github import Github
from github.GithubException import UnknownObjectException

def get_gh_token():
    result = subprocess.run(['gh', 'auth', 'token'], stdout=subprocess.PIPE, text=True)
    return result.stdout.strip()

def ensure_label_exists(repo, label_name):
    try:
        return repo.get_label(label_name)
    except UnknownObjectException:
        print(f"Luo label: {label_name}")
        return repo.create_label(name=label_name, color="ededed")

def main(csv_filename):
    ACCESS_TOKEN = get_gh_token()
    REPO_NAME = "ReetuInkila/TIDE-VSCode"

    g = Github(ACCESS_TOKEN)
    repo = g.get_repo(REPO_NAME)

    with open(csv_filename, newline="", encoding="utf-8-sig") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            title = row["Summary"]
            body = row["Description"]
            priority = row["Priority"]

            labels = []
            
            if priority.strip():
                labels.append(ensure_label_exists(repo, priority.strip()))

            try:
                issue = repo.create_issue(
                    title=title,
                    body=body,
                    labels=labels
                )
                print(f"Issue luotu: {issue.title}")
            except Exception as e:
                print(f"Virhe luodessa issuea '{title}': {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Luo GitHub-issuet CSV-tiedostosta")
    parser.add_argument("csv_filename", help="CSV-tiedoston nimi, esim. issues.csv")
    args = parser.parse_args()

    main(args.csv_filename)
