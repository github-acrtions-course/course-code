import unittest
from unittest.mock import MagicMock
from kubeHelper import auth, list_deployment, launch

class TestKubeHelper(unittest.TestCase):

    def test_auth(self):
        mock_open = MagicMock()
        mock_file = MagicMock()
        mock_open.return_value = mock_file
        mock_json_load = MagicMock()
        mock_json_load.return_value = {
            "kube": {
                "url": "http://example.com",
                "username": "user",
                "password": "pass"
            }
        }

        original_open = builtins.open
        original_json_load = json.load

        builtins.open = mock_open
        json.load = mock_json_load

        result = auth('test_env')

        self.assertEqual(result.url, "http://example.com")
        self.assertEqual(result.username, "user")
        self.assertEqual(result.password, "pass")

        builtins.open = original_open
        json.load = original_json_load
    
    def test_list_deployment(self):
        mock_namespace = MagicMock()
        mock_namespace.recover_deployment_list.return_value = {
            "items": [
                {"metadata": {"name": "app1"}},
                {"metadata": {"name": "other"}},
                {"metadata": {"name": "app2"}}
            ]
        }

        namespaces = ['namespace1', 'namespace2']
        result = list_deployment(mock_namespace, namespaces)
        
        expected_result = [
            {"metadata": {"name": "app1"}},
            {"metadata": {"name": "app2"}}
        ]
        self.assertEqual(result, expected_result)
    
    def test_launch(self):
        mock_auth = MagicMock()
        mock_auth.return_value = MagicMock()

        mock_list_deployment = MagicMock()
        mock_list_deployment.return_value = [
            {"metadata": {"name": "app1"}},
            {"metadata": {"name": "app2"}}
        ]

        mock_fetch_last_commit = MagicMock()
        mock_fetch_last_commit.return_value = "commit_sha"

        def mock_edit_method(deployment, env):
            return {"repository": "repo1"}

        result = launch(
            namespaces=['namespace1'],
            env='test_env',
            edit_method=mock_edit_method,
            auth_fn=mock_auth,
            list_deployment_fn=mock_list_deployment,
            fetch_commit_fn=mock_fetch_last_commit
        )

        expected_result = [
            {"repository": "repo1", "commit_hash": "commit_sha"},
            {"repository": "repo1", "commit_hash": "commit_sha"}
        ]
        self.assertEqual(result, expected_result)
        self.assertIn("commit_hash", result[0])
        self.assertIn("repository", result[0])

if __name__ == '__main__':
    unittest.main()
