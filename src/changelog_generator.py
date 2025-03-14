from github import Github, Repository, PullRequest, ContentFile
import os
from datetime import datetime
from dotenv import load_dotenv
from constants import RELEASE_BRANCH, authenticate

# Meta information
CHANGELOG_FILE = "CHANGELOG.md"
COMMIT_MESSAGE = "chore(changelog): update changelog"

ghub, repository = authenticate()

def get_latest_release() -> dict:
    """
    Get the latest release from the repository.

    :param repo: The repository object.
    :return: A dictionary containing the latest release information.
    """
    
    try:
        latest_release = repository.get_latest_release()
        latest_version = latest_release.tag_name
        
        return {
            "latest_release": latest_release,
            "latest_release_date": latest_release.created_at,
            "latest_version": latest_version
        }
        
    except:
        print("No releases found")
        return None
    
def get_merged_prs(release_date: datetime) -> list[PullRequest.PullRequest]:
    merged_prs: list[PullRequest.PullRequest] = []
    pulls = repository.get_pulls(state="closed", base=RELEASE_BRANCH)
    for pr in pulls:
        if pr.merged_at and pr.merged_at > release_date:
            # PaginatedList of pull request
            merged_prs.append(pr)
            
    print(f"Found {len(merged_prs)} merged PRs since last release.")
    return merged_prs

def calculate_new_version(current_version: str, merged_prs: list[PullRequest.PullRequest]) -> str:
    major_bump = False
    minor_bump = False
    patch_bump = False
    
    for pr in merged_prs:
        content = (pr.title + "\n" + (pr.body or "")).lower()
        if "breaking change" in content:
            major_bump = True
        elif "feat" in content:
            minor_bump = True
        elif "fix" in content:
            patch_bump = True
            
    try:
        major_num, minor_num, patch_num = map(int, current_version.strip("v").split("."))
        return f"v{major_num + (1 if major_bump else 0)}.{minor_num + (1 if minor_bump else 0)}.{patch_num + (1 if patch_bump else 0)}"
    except:
        print("Invalid version format.")
        return None
    
def update_changelog(new_entry: str) -> str:
    try:
        current_content = repository.get_contents(CHANGELOG_FILE, ref=RELEASE_BRANCH)
    except:
        print("Cannot find the changelog file.")
        return ""
    
    decoded = current_content.decoded_content.decode("utf-8")
    # Split the existing changelog into lines
    lines = decoded.splitlines()
    # Find the index of the first release entry (lines starting with "##")
    insert_index = 0
    for i, line in enumerate(lines):
        if line.startswith("##"):
            insert_index = i
            break
    else:
        insert_index = len(lines)
    
    # Insert new_entry just before the first release entry, maintaining header
    updated_lines = lines[:insert_index] + [new_entry, ""] + lines[insert_index:]
    updated_content = "\n".join(updated_lines)
    
    try:
        repository.update_file(current_content.path, COMMIT_MESSAGE, updated_content, current_content.sha, branch=RELEASE_BRANCH)
        print("Changelog updated successfully.")
        return updated_content
    except:
        print("Cannot update the changelog file.")
        return ""
    
def create_release(new_version: str) -> bool:
    try:
        repository.create_git_release(
            tag=new_version,
            name=new_version,
            message="Release " + new_version,
            target_commitish=RELEASE_BRANCH
        )
        print("Release created successfully.")
        return True
    except:
        print("Cannot create the release.")
        return False
    

if not authenticate():
    print("Authentication failed. Exiting...")
    exit(0)

release_info = get_latest_release()
if not release_info:
    print("No releases found. Exiting...")
    exit(1)
    
latest_version = release_info["latest_version"]
print("Latest version:", latest_version)

merged_prs = get_merged_prs(release_info["latest_release_date"])
if not merged_prs:
    print("No merged PRs found. Exiting...")
    exit(2)
    
new_version = calculate_new_version(latest_version, merged_prs)
if not new_version:
    print("Invalid version format. Exiting...")
    exit(3)
    
print("New version:", new_version)

changelog_entry = f"## {new_version} ({datetime.now().strftime('%Y-%m-%d')})\n"
for pr in merged_prs:
    changelog_entry += f"- {pr.title} (#{pr.number})\n"
    
print("Changelog entry generated:\n", changelog_entry)

if not update_changelog(changelog_entry):
    print("Failed to update the changelog.")
    exit(4)

create_release(new_version)

print("Done.")