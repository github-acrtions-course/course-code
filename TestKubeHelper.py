import unittest
from unittest.mock import patch, MagicMock
from kubeHelper import auth

class TestKubeHelper(unittest.TestCase):

    @patch('KubeClient.KubeAuth')
    def test_auth(self, mock_KubeAuth):
        with patch('builtins.open', new_callable=MagicMock) as mock_open:
            with patch('json.load') as mock_json_load:
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

                mock_open.assert_called_once_with(f'./auth.test_env.json')
                mock_json_load.assert_called_once()
                mock_KubeAuth.assert_called_once_with(
                    url="http://example.com",
                    username="user",
                    password="pass"
                )
                self.assertEqual(result, kube_auth_instance)

if __name__ == '__main__':
    unittest.main()
