import tempfile
import unittest
from pathlib import Path

from scripts.update_repo_catalog import (
    render_catalog,
    update_readme,
    validate_private_visibility,
)


REPOSITORIES = [
    {
        "name": "public-spec",
        "description": "Portable governance specifications",
        "visibility": "PUBLIC",
        "isArchived": False,
        "isFork": False,
        "url": "https://github.com/example/public-spec",
    },
    {
        "name": "private-core",
        "description": "Internal engine",
        "visibility": "PRIVATE",
        "isArchived": False,
        "isFork": False,
        "url": "https://github.com/example/private-core",
    },
    {
        "name": "old-repo",
        "description": "Retired",
        "visibility": "PUBLIC",
        "isArchived": True,
        "isFork": False,
        "url": "https://github.com/example/old-repo",
    },
    {
        "name": "active-fork",
        "description": "Maintained organization fork",
        "visibility": "PUBLIC",
        "isArchived": False,
        "isFork": True,
        "url": "https://github.com/example/active-fork",
    },
]


class RenderCatalogTests(unittest.TestCase):
    def test_incomplete_private_visibility_fails_closed(self):
        with self.assertRaisesRegex(ValueError, "expected 2 private repositories, found 1"):
            validate_private_visibility(REPOSITORIES, 2)

    def test_public_catalog_excludes_private_and_archived_repositories(self):
        catalog = render_catalog(REPOSITORIES, {}, "public")

        self.assertIn("public-spec", catalog)
        self.assertIn("active-fork", catalog)
        self.assertNotIn("private-core", catalog)
        self.assertNotIn("old-repo", catalog)

    def test_member_catalog_includes_active_private_repositories(self):
        catalog = render_catalog(REPOSITORIES, {}, "member")

        self.assertIn("public-spec", catalog)
        self.assertIn("private-core", catalog)

    def test_configured_role_and_status_override_repository_metadata(self):
        config = {
            "repositories": {
                "public-spec": {
                    "role": "The portable contract layer.",
                    "status": "Public draft.",
                    "order": 1,
                }
            }
        }

        catalog = render_catalog(REPOSITORIES, config, "public")

        self.assertIn("The portable contract layer.", catalog)
        self.assertIn("Public draft.", catalog)

    def test_unconfigured_new_repository_is_added_using_live_description(self):
        repositories = REPOSITORIES + [
            {
                "name": "new-repo",
                "description": "Newly added component",
                "visibility": "PUBLIC",
                "isArchived": False,
                "isFork": False,
                "url": "https://github.com/example/new-repo",
            }
        ]

        catalog = render_catalog(repositories, {}, "public")

        self.assertIn("new-repo", catalog)
        self.assertIn("Newly added component", catalog)

    def test_removed_repository_disappears_even_if_it_remains_in_config(self):
        config = {"repositories": {"missing": {"role": "No longer present"}}}

        catalog = render_catalog(REPOSITORIES, config, "public")

        self.assertNotIn("missing", catalog)
        self.assertNotIn("No longer present", catalog)


class UpdateReadmeTests(unittest.TestCase):
    def test_only_generated_region_is_replaced(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "README.md"
            path.write_text(
                "Before\n<!-- REPOSITORY-CATALOG:START -->\nold\n"
                "<!-- REPOSITORY-CATALOG:END -->\nAfter\n",
                encoding="utf-8",
            )

            update_readme(path, "new catalog")

            self.assertEqual(
                path.read_text(encoding="utf-8"),
                "Before\n<!-- REPOSITORY-CATALOG:START -->\nnew catalog\n"
                "<!-- REPOSITORY-CATALOG:END -->\nAfter\n",
            )

    def test_missing_markers_fail_closed(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "README.md"
            path.write_text("Hand-written content only\n", encoding="utf-8")

            with self.assertRaisesRegex(ValueError, "catalog markers"):
                update_readme(path, "new catalog")


if __name__ == "__main__":
    unittest.main()
