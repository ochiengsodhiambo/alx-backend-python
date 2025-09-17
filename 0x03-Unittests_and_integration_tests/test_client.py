#!/usr/bin/env python3
"""
Unit and integration tests for GithubOrgClient.
"""

import unittest
from unittest.mock import patch, Mock
from parameterized import parameterized, parameterized_class

from client import GithubOrgClient
from fixtures import org_payload, repos_payload, expected_repos, apache2_repos


class TestGithubOrgClient(unittest.TestCase):
    """Unit tests for GithubOrgClient."""

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch("client.get_json")
    def test_org(self, org_name, mock_get_json):
        """
        Test that GithubOrgClient.org calls get_json exactly once
        with the expected API URL for the given org.
        """
        client = GithubOrgClient(org_name)
        client.org
        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}"
        )

    def test_public_repos_url(self):
        """
        Test that _public_repos_url returns the expected repos_url
        from the mocked org payload.
        """
        with patch(
            "client.GithubOrgClient.org",
            new_callable=Mock
        ) as mock_org:
            mock_org.return_value = {
                "repos_url": (
                    "http://api.github.com/orgs/test/repos"
                )
            }
            client = GithubOrgClient("test")
            self.assertEqual(
                client._public_repos_url,
                "http://api.github.com/orgs/test/repos"
            )

    @patch("client.get_json")
    def test_public_repos(self, mock_get_json):
        """
        Test that public_repos returns the expected list of repo names
        based on the mocked API response payload.
        """
        test_payload = [{"name": "repo1"}, {"name": "repo2"}]
        mock_get_json.return_value = test_payload

        with patch(
            "client.GithubOrgClient._public_repos_url",
            new_callable=Mock
        ) as mock_repos_url:
            mock_repos_url.return_value = (
                "http://api.github.com/orgs/test/repos"
            )
            client = GithubOrgClient("test")
            result = client.public_repos()
            self.assertEqual(result, ["repo1", "repo2"])
            mock_repos_url.assert_called_once()
            mock_get_json.assert_called_once_with(
                "http://api.github.com/orgs/test/repos"
            )

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected):
        """
        Test that has_license returns True only if the repo dictionary
        contains a license entry matching the given license key.
        """
        self.assertEqual(
            GithubOrgClient.has_license(repo, license_key),
            expected
        )


@parameterized_class([
    {
        "org_payload": org_payload,
        "repos_payload": repos_payload,
        "expected_repos": expected_repos,
        "apache2_repos": apache2_repos,
    }
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration tests for GithubOrgClient using fixtures data."""

    @classmethod
    def setUpClass(cls):
        """
        Set up a patcher for requests.get.
        Configure its side_effect to return payloads from fixtures
        depending on the requested URL.
        """
        cls.get_patcher = patch("requests.get")
        mock_get = cls.get_patcher.start()

        def side_effect(url):
            if url.endswith("orgs/google"):
                return Mock(json=lambda: cls.org_payload)
            if url.endswith("orgs/google/repos"):
                return Mock(json=lambda: cls.repos_payload)
            return Mock(json=lambda: {})

        mock_get.side_effect = side_effect

    @classmethod
    def tearDownClass(cls):
        """
        Stop the patcher after all integration tests complete.
        """
        cls.get_patcher.stop()

    def test_public_repos(self):
        """
        Test that public_repos returns the expected repo list
        using data from fixtures.
        """
        client = GithubOrgClient("google")
        self.assertEqual(client.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self):
        """
        Test that public_repos correctly filters the repos list
        when a license argument is passed.
        """
        client = GithubOrgClient("google")
        self.assertEqual(
            client.public_repos(license="apache-2.0"),
            self.apache2_repos
        )
