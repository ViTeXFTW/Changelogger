from github import Github, PullRequest
import os
import sys
import re
import json
from constants import authenticate, MAX_COMMIT_HEADER_LENGTH

# Load lint_configuration.json
lint_configuration = None


try:
    with open("src/lint_config.json") as f:
        lint_configuration = json.load(f)
except:
    print("Failed to load lint configuration.")
    exit(1)

lint_types = lint_configuration["types"]
    
# Define commit header pattern
commit_header_pattern = re.compile(
    rf"^({'|'.join(lint_types)})(\([^()]+\))?(!)?:\s.+"
)

ghub, repository = authenticate()

def get_pull_request(pr_number: int) -> PullRequest.PullRequest:
    """
    Get a pull request by its number.
    
    :param pr_number: The pull request number.
    :return: The pull request object.
    """
    
    try:
        return repository.get_pull(pr_number)
    except:
        print(f"Failed to get pull request {pr_number}.")
        exit(2)
        
def validate_commit_message(message: str) -> list:
    """
    Validate a commit message.
    
    :param message: The commit message.
    :return: A list of errors.
    """
    
    errors = []
    lines = message.splitlines()
    if not lines:
        errors.append("Empty commit message.")
        return errors
    
    header = lines[0]
    body = '\n'.join(lines[1:]) if len(lines) > 1 else ""
    
    if len(header) > MAX_COMMIT_HEADER_LENGTH:
        errors.append(
            f"X title: Exceeds {MAX_COMMIT_HEADER_LENGTH} characters."
        )
    
    if not commit_header_pattern.match(header):
        errors.append(
            f"X title format: <type> must be one of {', '.join(lint_types)}."
        )
        
    if ":" not in header:
        errors.append("X title format: Must contain a colon after <type>.")

def lint_pull_request(pr: PullRequest.PullRequest) -> dict:
    
    commit_errors = {}
    commits = pr.get_commits()
    
    for commit in commits:
        message = commit.commit.message
        errors = validate_commit_message(message)
        if errors:
            commit_errors[commit.sha[:7]] = errors
            
    return commit_errors

def post_or_update_pr_comment(pr: PullRequest.PullRequest, comment_body: str):
    
    marker = "## Conventional Commit Linting Report"
    try:
        comments = pr.get_issue_comments()
        for comment in comments:
            if comment.body.startswith(marker):
                comment_to_update = comment
                break
            
        if comment_to_update:
            comment_to_update.edit(comment_body)
            print("Updating existing linting report.")
        else:
            pr.create_issue_comment(comment_body)
            print("Created new linting report.")
            
    except:
        print("Failed to post or update comment.")
        exit(3)
        
if len(sys.argv) < 2:
    print("Usage: python commit_linter.py <pull_request_number>")
    exit(0)
    
pr_number = int(sys.argv[1])

pr = get_pull_request(pr_number)
commit_errors = lint_pull_request(pr)

if commit_errors:
    report = "## Conventional Commit Linting Report\n"
    report += "The following commits have linting errors:\n\n"
    for sha, errors in commit_errors.items():
        report += f"**Commit {sha}**:\n"
        for err in errors:
            report += f"- {err}\n"
        report += "\n"
        
    post_or_update_pr_comment(pr, report)