import requests

def get_owner_and_repo(repo_url):
    return (
        repo_url.split("https://sgithub.fr.world.socgen/")[1].rstrip(".git").split("/")
    )

def build_github_repository_by_organization(repository, namespace, service_name):
    if repository is None or repository == "" or repository.startswith("None"):
        match namespace.split("-")[1]:
            case "ogn":
                return f"https://sgithub.fr.world.socgen/ItecFccOsd/financing-platform-{service_name}.git"
            case "cav":
                return f"https://sgithub.fr.world.socgen/CreditApproval/{service_name}.git"
            case "mcm2":
                return f"https://sgithub.fr.world.socgen/debt-capital-markets/{service_name}.git"
    return repository

def get_github_org(namespace):
    match namespace.split("-")[1]:
        case "ogn":
            return "ItecFccOsd"
        case "cav":
            return "CreditApproval"
        case "mcm2":
            return "Debt-Capital-Markets"

def get_default_branch(owner, repo):
    if repo.endswith("-run"):
        repo = repo.replace("-run", "")
    branch_api_url = (
        f"https://sgithub.fr.world.socgen/api/v3/repos/{owner}/{repo}/branches"
    )
    response = requests.get(branch_api_url)
    if response.status_code != 200:
        print(f"Failed to fetch branches http status: {response.status_code}")
        return None
    branches = [branch["name"] for branch in response.json()]

    if "master" in branches:
        return "master"
    if "main" in branches:
        return "main"
    print("Neither master nor main branch found.")
    return None

def get_last_commit_from_default_branch(branch, owner, repo):
    if repo.endswith("-run"):
        repo = repo.replace("-run", "")
    branch_api_url = (
        f"https://sgithub.fr.world.socgen/api/v3/repos/{owner}/{repo}/commits/{branch}"
    )
    response = requests.get(branch_api_url)
    if response.status_code != 200:
        print(f"Failed to fetch commit http status: {response.status_code}")
        return None

    last_commit = dict(response.json())
    return last_commit["sha"]

def fetch_last_commit_orchestrator(project_repository):
    owner, repo = get_owner_and_repo(project_repository)
    default_branch = get_default_branch(owner, repo)
    commit_sha = get_last_commit_from_default_branch(default_branch, owner, repo)
    if commit_sha:
        return commit_sha[:10]
    return None
