import json
import os
import tempfile
import unittest

from hexasset.core import find_matches

class TestCore(unittest.TestCase):
    def test_finds_match_in_xcassets_colorset(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            # Create: Foo.xcassets/BrandBlue.colorset/Contents.json
            colorset_dir = os.path.join(td, "Foo.xcassets", "BrandBlue.colorset")
            os.makedirs(colorset_dir, exist_ok=True)

            contents = {
                "colors": [
                    {
                        "color": {
                            "components": {
                                "red": "0xAA",
                                "green": "0xBB",
                                "blue": "0xCC",
                                "alpha": "0.5",
                            }
                        }
                    }
                ]
            }
            with open(os.path.join(colorset_dir, "Contents.json"), "w", encoding="utf-8") as f:
                json.dump(contents, f)

            matches = find_matches(td, "#AABBCC")
            self.assertEqual(len(matches), 1)
            self.assertEqual(matches[0].name, "BrandBlue")
            self.assertEqual(matches[0].alpha, "0.5")


if __name__ == "__main__":
    unittest.main()
