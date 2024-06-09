import unittest
from unittest.mock import patch, MagicMock
from kubeHelper import auth, list_deployment, launch

class TestKubeHelper(unittest.TestCase):
    
    @patch('builtins.open')
    @patch('json.load')
    @patch('KubeClient.KubeAuth')
    def test_auth(self, mock_KubeAuth, mock_json_load, mock_open):
        mock_json_load.return_value = {
            "kube": {
                "url": "http://example.com",
                "username": "user",
                "password": "pass"
            }
        }
        
        kube_auth_instance = MagicMock()
        mock_KubeAuth.return_value = kube_auth_instance

        result = auth('test_env')

        mock_open.assert_called_once_with('f./auth.test_env.json')
        mock_json_load.assert_called_once()
        mock_KubeAuth.assert_called_once_with(
            url="http://example.com",
            username="user",
            password="pass"
        )
        self.assertEqual(result, kube_auth_instance)
    
    @patch('KubeClient.KubeNamespace')
    def test_list_deployment(self, mock_KubeNamespace):
        mock_namespace = MagicMock()
        mock_namespace.recover_deployment_list.return_value = {
            "items": [
                {"metadata": {"name": "app1"}},
                {"metadata": {"name": "app2"}},
            ]
        }
        mock_KubeNamespace.return_value = mock_namespace
        
        namespaces = ['namespace1', 'namespace2']
        result = list_deployment(mock_KubeNamespace, namespaces)
        
        expected_result = [{"metadata": {"name": "app1"}}, {"metadata": {"name": "app2"}}]
        self.assertEqual(result, expected_result)
    
    @patch('kubeHelper.fetch_last_commit_orchestrator')
    @patch('kubeHelper.list_deployment')
    @patch('kubeHelper.auth')
    def test_launch(self, mock_auth, mock_list_deployment, mock_fetch_last_commit):
        mock_auth.return_value = MagicMock()
        mock_list_deployment.return_value = [
            {"metadata": {"name": "app1"}},
            {"metadata": {"name": "app2"}}
        ]
        mock_fetch_last_commit.return_value = "commit_sha"
        
        def mock_edit_method(deployment, env):
            return {"repository": "repo1"}
        
        result = launch(['namespace1'], 'test_env', mock_edit_method)
        
        expected_result = [
            {"repository": "repo1", "commit_hash": "commit_sha"},
            {"repository": "repo1", "commit_hash": "commit_sha"}
        ]
        self.assertEqual(result, expected_result)
        self.assertIn("commit_hash", result[0])
        self.assertIn("repository", result[0])

if __name__ == '__main__':
    unittest.main()
