#!/usr/bin/env python3
"""
Unit tests for GithubOrgClient in client.py
"""
import unittest
from unittest.mock import patch, PropertyMock
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Tests for GithubOrgClient class"""

    def test_public_repos_url(self):
        """Test GithubOrgClient._public_repos_url property"""
        org_payload = {"repos_url": "https://api.github.com/orgs/google/repos"}

        with patch.object(GithubOrgClient, "org",
                          new_callable=PropertyMock) as mock_org:
            mock_org.return_value = org_payload
            client = GithubOrgClient("google")

            result = client._public_repos_url

            self.assertEqual(result, org_payload["repos_url"])
