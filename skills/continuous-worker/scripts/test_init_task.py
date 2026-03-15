#!/usr/bin/env python3
"""
Tests for init_task helpers.
"""

from unittest import TestCase, main

from init_task import render_task, slugify


class InitTaskTest(TestCase):
    def test_slugify(self):
        self.assertEqual(slugify("My Long Task"), "my-long-task")
        self.assertEqual(slugify("  !!!  "), "task")

    def test_render_task_contains_defaults(self):
        class Args:
            title = "Example Task"
            goal = "Ship the feature"
            criterion = ["tests pass"]
            wake_owner = "manual"
            retry_budget = "3 attempts"
            update_policy = "blockers, milestones, completion only"

        rendered = render_task(Args, "example-task")
        self.assertIn("Slug: example-task", rendered)
        self.assertIn("Goal: Ship the feature", rendered)
        self.assertIn("- tests pass", rendered)
        self.assertIn(
            "Canonical runtime: the `task` record for `example-task` is the source of truth",
            rendered,
        )


if __name__ == "__main__":
    main()
