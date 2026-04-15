import csv
import os
import subprocess
import sys
import tempfile
import unittest

from utils.joke_skill import (
    STANDALONE_SKILL_DIRNAME,
    TOPIC_KEYWORDS,
    JokeRecord,
    build_topic_reference,
    classify_topics,
    format_final_joke,
    generate_standalone_skill_bundle,
    load_jokes,
    select_joke,
)


class JokeSkillTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        repo_root = os.path.dirname(os.path.dirname(__file__))
        cls.csv_path = os.path.join(repo_root, "jokes_with_id.csv")
        cls.jokes = load_jokes(cls.csv_path)

    def test_load_jokes_returns_records(self):
        self.assertGreater(len(self.jokes), 150)
        self.assertIsInstance(self.jokes[0], JokeRecord)

    def test_classify_topics_contains_debugging_quote(self):
        topics = classify_topics(self.jokes)
        debugging_ids = {joke.id for joke in topics["Debugging"]}
        self.assertIn("22", debugging_ids)
        self.assertIn("68", debugging_ids)

    def test_select_joke_prefers_debugging_context(self):
        joke = select_joke(self.jokes, "I fixed a nasty debugging bug in the code path")
        self.assertIn(joke.id, {"22", "68", "122", "133", "150", "38", "45", "55", "102"})

    def test_select_joke_falls_back_to_classic_quote(self):
        joke = select_joke(self.jokes, "totally unrelated phrase with no signal")
        self.assertTrue(joke.english)
        self.assertTrue(joke.chinese)

    def test_format_final_joke_has_bilingual_shape(self):
        joke = select_joke(self.jokes, "please show me the code")
        formatted = format_final_joke(joke)
        self.assertIn("技术段子 / Tech Joke", formatted)
        self.assertIn("EN:", formatted)
        self.assertIn("ZH:", formatted)

    def test_build_topic_reference_contains_expected_sections(self):
        content = build_topic_reference(self.jokes)
        self.assertIn("# Jokes by Topic", content)
        self.assertIn("## Debugging", content)
        self.assertIn("## Code Quality", content)
        self.assertIn("## Optimization", content)

    def test_generated_reference_can_be_written(self):
        content = build_topic_reference(self.jokes)
        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = os.path.join(tmpdir, "jokes-by-topic.md")
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(content)
            with open(output_path, "r", encoding="utf-8") as f:
                self.assertEqual(content, f.read())

    def test_generate_standalone_skill_bundle_creates_drop_in_folder(self):
        repo_root = os.path.dirname(os.path.dirname(__file__))
        with tempfile.TemporaryDirectory() as tmpdir:
            bundle_path = generate_standalone_skill_bundle(repo_root, tmpdir)
            self.assertEqual(bundle_path.name, STANDALONE_SKILL_DIRNAME)
            self.assertTrue(os.path.exists(os.path.join(bundle_path, "SKILL.md")))
            self.assertTrue(os.path.exists(os.path.join(bundle_path, "references", "jokes-by-topic.md")))
            self.assertTrue(os.path.exists(os.path.join(bundle_path, "references", "joke-selection-rules.md")))
            self.assertTrue(os.path.exists(os.path.join(bundle_path, "scripts", "pick_joke.py")))
            self.assertTrue(os.path.exists(os.path.join(bundle_path, "utils", "joke_skill.py")))
            self.assertTrue(os.path.exists(os.path.join(bundle_path, "jokes_with_id.csv")))

    def test_standalone_bundle_script_runs_directly(self):
        repo_root = os.path.dirname(os.path.dirname(__file__))
        with tempfile.TemporaryDirectory() as tmpdir:
            bundle_path = generate_standalone_skill_bundle(repo_root, tmpdir)
            result = subprocess.run(
                [
                    sys.executable,
                    os.path.join(bundle_path, "scripts", "pick_joke.py"),
                    "--query",
                    "please debug this release bug",
                    "--format",
                    "text",
                ],
                cwd=bundle_path,
                capture_output=True,
                text=True,
                check=True,
            )
            self.assertIn("技术段子 / Tech Joke", result.stdout)
            self.assertIn("EN:", result.stdout)
            self.assertIn("ZH:", result.stdout)

    def test_pick_joke_script_returns_text_output(self):
        repo_root = os.path.dirname(os.path.dirname(__file__))
        result = subprocess.run(
            [
                sys.executable,
                os.path.join(repo_root, "scripts", "pick_joke.py"),
                "--query",
                "please debug this bug",
                "--format",
                "text",
            ],
            cwd=repo_root,
            capture_output=True,
            text=True,
            check=True,
        )
        self.assertIn("技术段子 / Tech Joke", result.stdout)
        self.assertIn("EN:", result.stdout)
        self.assertIn("ZH:", result.stdout)

    def test_topic_keywords_include_core_buckets(self):
        self.assertIn("Debugging", TOPIC_KEYWORDS)
        self.assertIn("Code Quality", TOPIC_KEYWORDS)
        self.assertIn("Planning", TOPIC_KEYWORDS)


if __name__ == "__main__":
    unittest.main()
