from unittest.mock import patch, PropertyMock

class TestGithubOrgClient(unittest.TestCase):
    # ... (other tests)

    @patch('client.get_json')
    def test_public_repos(self, mock_get_json):
        """Test GithubOrgClient.public_repos returns expected repo names"""
        # Sample fake repo data returned by get_json
        repo_payload = [
            {"name": "repo1"},
            {"name": "repo2"},
            {"name": "repo3"}
        ]
        mock_get_json.return_value = repo_payload

        with patch.object(GithubOrgClient, "_public_repos_url",
                          new_callable=PropertyMock) as mock_repos_url:
            mock_repos_url.return_value = "https://api.github.com/orgs/google/repos"

            client = GithubOrgClient("google")
            repos = client.public_repos()

            # Assert that public_repos returns list of repo names
            self.assertEqual(repos, ["repo1", "repo2", "repo3"])

            # Assert _public_repos_url property was accessed exactly once
            mock_repos_url.assert_called_once()

            # Assert get_json was called exactly once with the mocked URL
            mock_get_json.assert_called_once_with("https://api.github.com/orgs/google/repos")
