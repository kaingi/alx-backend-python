#!/usr/bin/env python3
"""
Integration tests for GithubOrgClient.public_repos using fixtures.
"""

import unittest
from unittest.mock import patch, Mock
from parameterized import parameterized_class
from client import GithubOrgClient
from fixtures import org_payload, repos_payload, expected_repos, apache2_repos


@parameterized_class([
    {
        "org_payload": org_payload,
        "repos_payload": repos_payload,
        "expected_repos": expected_repos,
        "apache2_repos": apache2_repos,
    }
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration tests for GithubOrgClient.public_repos."""

   @classmethod
def setUpClass(cls):
    """Patch requests.get to return fixtures based on URL."""
    cls.get_patcher = patch('requests.get')
    mock_get = cls.get_patcher.start()

    org_url = f"https://api.github.com/orgs/{cls.org_payload['login']}"

    def get_side_effect(url, *args, **kwargs):
        mock_resp = Mock()
        if url == cls.org_payload['repos_url']:
            mock_resp.json.return_value = cls.repos_payload
        elif url == org_url:
            mock_resp.json.return_value = cls.org_payload
        else:
            mock_resp.json.return_value = None
        return mock_resp

    mock_get.side_effect = get_side_effect

    @classmethod
    def tearDownClass(cls):
        """Stop patcher."""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Test that public_repos returns expected repo list."""
        client = GithubOrgClient(self.org_payload['login'])
        repos = client.public_repos()
        self.assertEqual(repos, self.expected_repos)

    def test_public_repos_with_license(self):
        """Test filtering repos with license 'apache-2.0'."""
        client = GithubOrgClient(self.org_payload['login'])
        apache_repos = client.public_repos(license="apache-2.0")
        self.assertEqual(apache_repos, self.apache2_repos)
