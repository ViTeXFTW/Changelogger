from dotenv import load_dotenv
from github import Github, Repository
import os

# Load environment variables from a .env file
load_dotenv()
# Access the GitHub token from the environment
GH_TOKEN = os.getenv("GH_TOKEN")

REPO_NAME = "ViTeXFTW/Changelogger"
RELEASE_BRANCH = "release"

MAX_COMMIT_HEADER_LENGTH = 100

def authenticate() -> tuple[Github, Repository.Repository]:
    """
    Authenticate with the GitHub API.
    
    :return: A tuple containing the GitHub object and the repository object.
    """
    
    global ghub, repository
    try:
        ghub = Github(GH_TOKEN)
        repository = ghub.get_repo(REPO_NAME)
        return ghub, repository
    except:
        print("Authentication failed.")
        return False