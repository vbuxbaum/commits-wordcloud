import requests


def get_repo_branches(repo_path):
    res = requests.get(f"https://api.github.com/repos/{repo_path}/branches")
    try:
        return [branch["name"] for branch in res.json()]
    except TypeError as e:
        print(res.json())
        raise e


def get_commit_messages(repo_path, branch):
    res = requests.get(
        f"https://api.github.com/repos/{repo_path}/commits?sha={branch}"
    )
    return [commit["commit"]["message"] for commit in res.json()]


if __name__ == "__main__":

    requests.get("https://api.github.com", auth={"u": "vbuxbaum"})
    branches = get_repo_branches("tryber/sd-08-tech-news")
    result_string = ""
    for branch in branches:
        commit_messages = get_commit_messages("tryber/sd-08-tech-news", branch)
        result_string += " ".join(commit_messages)
        print(f"Done {branch }")
    print(result_string)
