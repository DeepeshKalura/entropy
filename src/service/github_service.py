from github import Github


class GithubService:
    def __init__(self):
        self.client = Github()

    def bounty_issue(
        self,
    ):
        pass

    def fetch_issues(self, repository, state="open", assignee=None):
        value = self.client.get_repo(repository).get_issues(state=state)
        return value
