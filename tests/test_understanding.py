import os
import tempfile
import unittest

from campusflow.understanding_check import score_answers, run_check
from campusflow.understanding_questions import QUESTIONS


def fake_input(responses):
    iterator = iter(responses)
    return lambda prompt="": next(iterator)


class UnderstandingCheckTests(unittest.TestCase):
    def test_all_correct_scores_six(self):
        answers = {q["id"]: q["correct"] for q in QUESTIONS}
        self.assertEqual(score_answers(QUESTIONS, answers), 6)

    def test_all_wrong_scores_zero(self):
        wrong = {q["id"]: ("A" if q["correct"] != "A" else "B") for q in QUESTIONS}
        self.assertEqual(score_answers(QUESTIONS, wrong), 0)

    def test_invalid_answer_is_retried_and_score_is_correct(self):
        correct = [q["correct"] for q in QUESTIONS]
        responses = ["Z"] + correct + ["my reason one", "my reason two"]
        outputs = []
        with tempfile.TemporaryDirectory() as folder:
            path = os.path.join(folder, "notes.txt")
            score = run_check(input_fn=fake_input(responses),
                              output_fn=outputs.append, notes_path=path)
            with open(path, encoding="utf-8") as f:
                saved = f.read()
        self.assertEqual(score, 6)
        self.assertTrue(any("Invalid choice" in line for line in outputs))
        self.assertIn("my reason one", saved)


if __name__ == "__main__":
    unittest.main()