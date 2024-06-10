import unittest
from unittest.mock import patch, MagicMock
import json
from JenkinsClient import JenkinsClient

class TestJenkinsClient(unittest.TestCase):
    @patch('jenkins.Jenkins')
    def setUp(self, mock_jenkins):
        self.jenkins_client = JenkinsClient()
        self.mock_jenkins_instance = MagicMock()
        mock_jenkins.return_value = self.mock_jenkins_instance

    @patch('builtins.open')
    @patch('json.load')
    @patch('jenkins.Jenkins')
    def test_get_server_instance(self, mock_jenkins, mock_json_load, mock_open):
        mock_json_load.return_value = {
            "jenkins": {
                "url": "http://localhost",
                "username": "user",
                "token": "token"
            }
        }
        instance = self.jenkins_client.get_server_instance()
        mock_open.assert_called_once_with("./auth.dev.json")
        mock_jenkins.assert_called_once_with("http://localhost", "user", "token")
        self.assertEqual(instance, self.mock_jenkins_instance)

    @patch.object(JenkinsClient, 'get_server_instance')
    def test_get_job_detail(self, mock_get_server_instance):
        mock_get_server_instance.return_value = self.mock_jenkins_instance
        job_name = "test_job"
        self.jenkins_client.get_job_detail(job_name)
        self.mock_jenkins_instance.get_job_info.assert_called_once_with(job_name)

    @patch.object(JenkinsClient, 'get_server_instance')
    def test_trigger_build(self, mock_get_server_instance):
        mock_get_server_instance.return_value = self.mock_jenkins_instance
        job_name = "test_job"
        self.jenkins_client.trigger_build(job_name)
        self.mock_jenkins_instance.build_job.assert_called_once_with(job_name)

if __name__ == "__main__":
    unittest.main()
