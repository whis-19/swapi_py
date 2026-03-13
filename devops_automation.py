import os
import requests
import subprocess
import sys

# Configuration
GITHUB_TOKEN = "YOUR_GITHUB_PAT"
REPO_OWNER = "whis-19"
REPO_NAME = "swapi_py"
BASE_URL = "https://api.github.com"

headers = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

TASKS = [
    {"title": "Task 1a: Backend Dockerfile", "assignee": "whis-19", "body": "Create a optimized Dockerfile for the Flask backend."},
    {"title": "Task 1b: Frontend Dockerfile", "assignee": "SyedTaqii", "body": "Create a optimized Dockerfile for the Angular frontend."},
    {"title": "Task 2a: Compose DB & Networking", "assignee": "whis-19", "body": "Configure PostgreSQL and network in docker-compose.yml."},
    {"title": "Task 2b: Compose Orchestration", "assignee": "SyedTaqii", "body": "Set up service dependencies and env vars in docker-compose.yml."},
    {"title": "Task 3a: Backend K8s Deployment", "assignee": "SyedTaqii", "body": "Create Kubernetes Deployment and Service for the backend."},
    {"title": "Task 3b: Frontend K8s Deployment", "assignee": "whis-19", "body": "Create Kubernetes Deployment and Service for the frontend."},
    {"title": "Task 4a: K8s Storage (PV/PVC)", "assignee": "whis-19", "body": "Configure Persistent Volume and Claim for the database."},
    {"title": "Task 4b: DB K8s Deployment", "assignee": "SyedTaqii", "body": "Deploy database with volume mounts in Kubernetes."},
    {"title": "Task 5a: K8s HPA", "assignee": "SyedTaqii", "body": "Implement Horizontal Pod Autoscaler for scaling."},
    {"title": "Task 5b: Scaling Verification", "assignee": "whis-19", "body": "Verify K8s scaling and perform stress tests."},
    {"title": "Task 6a: Docker Documentation", "assignee": "whis-19", "body": "Document Docker and Compose setup in README.md."},
    {"title": "Task 6b: K8s Documentation", "assignee": "SyedTaqii", "body": "Document Kubernetes and Scaling setup in README.md."},
]

def run_git_command(cmd):
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error running command {' '.join(cmd)}: {e.stderr}")
        return None

def create_issue(task):
    url = f"{BASE_URL}/repos/{REPO_OWNER}/{REPO_NAME}/issues"
    data = {
        "title": task["title"],
        "body": task["body"],
        "assignees": [task["assignee"]]
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 201:
        issue_data = response.json()
        print(f"Created Issue #{issue_data['number']}: {task['title']}")
        return issue_data['number']
    else:
        print(f"Failed to create issue: {response.status_code}, {response.text}")
        return None

def setup_branch(issue_number, task_title):
    branch_name = f"feature/issue-{issue_number}-{task_title.lower().replace(' ', '-').replace(':', '')}"
    print(f"Setting up branch: {branch_name}")
    run_git_command(["git", "checkout", "main"])
    run_git_command(["git", "pull", "origin", "main"])
    run_git_command(["git", "checkout", "-b", branch_name])
    return branch_name

def main():
    print("Starting DevOps Automation Script...")
    
    # 1. Create Issues
    issue_numbers = []
    for task in TASKS:
        num = create_issue(task)
        if num:
            issue_numbers.append((num, task["title"]))
            
    print("\nAll issues created successfully.")
    
    # Example: Setup first branch for Member 1
    if issue_numbers:
        setup_branch(issue_numbers[0][0], issue_numbers[0][1])
        print("\nPrimary branch for Task 1a established. Ready for implementation.")

if __name__ == "__main__":
    main()
