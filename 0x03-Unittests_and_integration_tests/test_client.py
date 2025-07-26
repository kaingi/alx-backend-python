#!/usr/bin/env python3
"""
Unit tests for GithubOrgClient in client.py
"""
import unittest
from unittest.mock import patch, PropertyMock
from parameterized import parameterized
from client import GithubOrgClient

# rest of your tests ...


class TestGithubOrgClient(unittest.TestCase):
    # ... (other tests)

   @patch('client.get_json')
def test_public_repos(self, mock_get_json):
    """Test GithubOrgClient.public_repos returns expected repo names"""
    repo_payload = [
        {"name": "repo1"},
        {"name": "repo2"},
        {"name": "repo3"}
    ]
    mock_get_json.return_value = repo_payload

    with patch.object(
        GithubOrgClient, "_public_repos_url", new_callable=PropertyMock
    ) as mock_repos_url:
        mock_repos_url.return_value = (
            "https://api.github.com/orgs/google/repos"
        )

        client = GithubOrgClient("google")
        repos = client.public_repos()

        self.assertEqual(repos, ["repo1", "repo2", "repo3"])
        mock_repos_url.assert_called_once()
        mock_get_json.assert_called_once_with(
            "https://api.github.com/orgs/google/repos"
        )

