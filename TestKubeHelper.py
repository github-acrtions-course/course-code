import unittest
from unittest.mock import MagicMock
from kubeHelper import auth, list_deployment, launch

class TestKubeHelper(unittest.TestCase):

    def test_auth(self):
        # Mock the open function and json.load
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

        # Replace the builtins.open and json.load with our mocks
        builtins_open_backup = open
        json_load_backup = json.load
        try:
            open = mock_open
            json.load = mock_json_load

            # Create a mock for KubeAuth
            mock_KubeAuth = MagicMock()
            kube_auth_instance = MagicMock()
            mock_KubeAuth.return_value = kube_auth_instance

            result = auth('test_env')

            mock_open.assert_called_once_with('./auth.test_env.json')
            mock_json_load.assert_called_once()
            mock_KubeAuth.assert_called_once_with(
                url="http://example.com",
                username="user",
                password="pass"
            )
            self.assertEqual(result, kube_auth_instance)
        finally:
            # Restore the original functions
            open = builtins_open_backup
            json.load = json_load_backup
    
    def test_list_deployment(self):
        # Create a mock for KubeNamespace
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
        # Create mocks
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

        # Backup the original functions
        original_auth = launch.__globals__['auth']
        original_list_deployment = launch.__globals__['list_deployment']
        original_fetch_last_commit_orchestrator = launch.__globals__['fetch_last_commit_orchestrator']

        # Replace the original functions with mocks
        launch.__globals__['auth'] = mock_auth
        launch.__globals__['list_deployment'] = mock_list_deployment
        launch.__globals__['fetch_last_commit_orchestrator'] = mock_fetch_last_commit

        try:
            result = launch(['namespace1'], 'test_env', mock_edit_method)

            expected_result = [
                {"repository": "repo1", "commit_hash": "commit_sha"},
                {"repository": "repo1", "commit_hash": "commit_sha"}
            ]
            self.assertEqual(result, expected_result)
            self.assertIn("commit_hash", result[0])
            self.assertIn("repository", result[0])
        finally:
            # Restore the original functions
            launch.__globals__['auth'] = original_auth
            launch.__globals__['list_deployment'] = original_list_deployment
            launch.__globals__['fetch_last_commit_orchestrator'] = original_fetch_last_commit_orchestrator

if __name__ == '__main__':
    unittest.main()
