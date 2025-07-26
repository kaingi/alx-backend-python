from parameterized import parameterized

class TestGithubOrgClient(unittest.TestCase):
    # ... other tests ...

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected):
        """
        Test GithubOrgClient.has_license returns correct boolean
        depending on license key match.
        """
        client = GithubOrgClient("any_org")
        result = client.has_license(repo, license_key)
        self.assertEqual(result, expected)
