#!/usr/bin/env python3
"""
Tests for render_progress helpers.
"""

from unittest import TestCase, main

from render_progress import clamp_percent, render_bar


class RenderProgressTest(TestCase):
    def test_clamp_percent(self):
        self.assertEqual(clamp_percent(-3), 0)
        self.assertEqual(clamp_percent(42.2), 42)
        self.assertEqual(clamp_percent(101), 100)

    def test_render_bar(self):
        self.assertEqual(render_bar(50, 10), "[#####-----] 50%")
        self.assertEqual(render_bar(100, 5), "[#####] 100%")


if __name__ == "__main__":
    main()
