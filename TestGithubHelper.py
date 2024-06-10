import unittest
from unittest.mock import patch
import requests

# Assuming the GithubHelper.py module is imported as github_helper
import per as github_helper

class TestGithubHelper(unittest.TestCase):

    def test_get_owner_and_repo(self):
        repo_url = "https://sgithub.fr.world.socgen/owner/repo.git"
        expected_result = ["owner", "repo"]
        self.assertEqual(github_helper.get_owner_and_repo(repo_url), expected_result)

    def test_build_github_repository_by_organization(self):
        repository = None
        namespace = "some-ogn-namespace"
        service_name = "test-service"
        expected_result = "https://sgithub.fr.world.socgen/ItecFccOsd/financing-platform-test-service.git"
        self.assertEqual(github_helper.build_github_repository_by_organization(repository, namespace, service_name), expected_result)

        namespace = "some-cav-namespace"
        expected_result = "https://sgithub.fr.world.socgen/CreditApproval/test-service.git"
        self.assertEqual(github_helper.build_github_repository_by_organization(repository, namespace, service_name), expected_result)

        namespace = "some-mcm2-namespace"
        expected_result = "https://sgithub.fr.world.socgen/debt-capital-markets/test-service.git"
        self.assertEqual(github_helper.build_github_repository_by_organization(repository, namespace, service_name), expected_result)

    def test_get_github_org(self):
        namespace = "some-ogn-namespace"
        expected_result = "ItecFccOsd"
        self.assertEqual(github_helper.get_github_org(namespace), expected_result)

        namespace = "some-cav-namespace"
        expected_result = "CreditApproval"
        self.assertEqual(github_helper.get_github_org(namespace), expected_result)

        namespace = "some-mcm2-namespace"
        expected_result = "Debt-Capital-Markets"
        self.assertEqual(github_helper.get_github_org(namespace), expected_result)

    @patch('requests.get')
    def test_get_default_branch(self, mock_get):
        owner = "owner"
        repo = "repo"
        branches_response = [{"name": "master"}, {"name": "main"}]
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = branches_response

        self.assertEqual(github_helper.get_default_branch(owner, repo), "master")

        branches_response = [{"name": "main"}]
        mock_get.return_value.json.return_value = branches_response
        self.assertEqual(github_helper.get_default_branch(owner, repo), "main")

        branches_response = [{"name": "dev"}]
        mock_get.return_value.json.return_value = branches_response
        self.assertEqual(github_helper.get_default_branch(owner, repo), None)

        mock_get.return_value.status_code = 404
        self.assertEqual(github_helper.get_default_branch(owner, repo), None)

    @patch('requests.get')
    def test_get_last_commit_from_default_branch(self, mock_get):
        owner = "owner"
        repo = "repo"
        branch = "main"
        commit_response = {"sha": "1234567890abcdef"}
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = commit_response

        self.assertEqual(github_helper.get_last_commit_from_default_branch(branch, owner, repo), "1234567890abcdef")

        mock_get.return_value.status_code = 404
        self.assertEqual(github_helper.get_last_commit_from_default_branch(branch, owner, repo), None)

    @patch('github_helper.get_owner_and_repo', return_value=("owner", "repo"))
    @patch('github_helper.get_default_branch', return_value="main")
    @patch('github_helper.get_last_commit_from_default_branch', return_value="1234567890abcdef")
    def test_fetch_last_commit_orchestrator(self, mock_get_owner_and_repo, mock_get_default_branch, mock_get_last_commit_from_default_branch):
        project_repository = "https://sgithub.fr.world.socgen/owner/repo.git"
        expected_result = "1234567890"
        self.assertEqual(github_helper.fetch_last_commit_orchestrator(project_repository), expected_result)

if __name__ == '__main__':
    unittest.main()
