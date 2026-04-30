"""Unit tests for the Edit-mode preset radio handler (#1156 PR-C).

Regression for codex round-1 P2 finding: ``on_edit_type_change`` was
defined but never wired, so the radio change was inert and
``remix``/``custom`` silently sent the ``only_lyrics`` defaults.
"""

import unittest

from acestep.ui.gradio.interfaces.generation_tab_edit_controls import (
    EDIT_TYPE_PRESETS,
    on_edit_type_change,
)


class OnEditTypeChangeTests(unittest.TestCase):

    def test_only_lyrics_preset(self):
        n_min_update, n_max_update = on_edit_type_change("only_lyrics")
        self.assertEqual(n_min_update["value"], EDIT_TYPE_PRESETS["only_lyrics"]["n_min"])
        self.assertEqual(n_max_update["value"], EDIT_TYPE_PRESETS["only_lyrics"]["n_max"])
        self.assertFalse(n_min_update["interactive"])
        self.assertFalse(n_max_update["interactive"])

    def test_remix_preset(self):
        n_min_update, n_max_update = on_edit_type_change("remix")
        self.assertEqual(n_min_update["value"], EDIT_TYPE_PRESETS["remix"]["n_min"])
        self.assertEqual(n_max_update["value"], EDIT_TYPE_PRESETS["remix"]["n_max"])
        self.assertFalse(n_min_update["interactive"])

    def test_custom_unlocks_sliders(self):
        n_min_update, n_max_update = on_edit_type_change("custom")
        self.assertTrue(n_min_update["interactive"])
        self.assertTrue(n_max_update["interactive"])
        # Custom leaves the slider value alone so the user can fine-tune
        # whatever the previous preset put there.
        self.assertNotIn("value", n_min_update)
        self.assertNotIn("value", n_max_update)

    def test_unknown_value_falls_back_to_only_lyrics(self):
        n_min_update, _ = on_edit_type_change("garbage_input")
        self.assertEqual(n_min_update["value"], EDIT_TYPE_PRESETS["only_lyrics"]["n_min"])


if __name__ == "__main__":
    unittest.main()
