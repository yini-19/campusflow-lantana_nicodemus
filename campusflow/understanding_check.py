from campusflow.understanding_questions import QUESTIONS

VALID_CHOICES = ("A", "B", "C", "D")
EXPLAIN_IDS = ("Q1", "Q4")   # choose any two you can defend
NOTES_PATH = "docs/understanding-check-notes.txt"


def score_answers(questions, answers):
    """Pure scoring. answers is {'Q1': 'B', ...}. Returns 0 to len(questions)."""
    return sum(1 for q in questions if answers.get(q["id"]) == q["correct"])


def run_check(questions=QUESTIONS, input_fn=input, output_fn=print,
              notes_path=NOTES_PATH):
    answers = {}
    for q in questions:
        output_fn(f"\n{q['id']}. {q['prompt']}")
        for letter, text in q["options"].items():
            output_fn(f"  {letter}) {text}")
        while True:
            choice = input_fn("Your answer (A/B/C/D): ").strip().upper()
            if choice in VALID_CHOICES:
                break
            output_fn("Invalid choice. Please enter A, B, C or D.")
        answers[q["id"]] = choice          # first valid choice is final
        if choice == q["correct"]:
            output_fn("Correct.")
        else:
            output_fn(f"Not quite. The correct answer is {q['correct']}.")

    score = score_answers(questions, answers)
    output_fn(f"\nFinal score: {score}/{len(questions)}")

    explanations = {}
    for qid in EXPLAIN_IDS:
        while True:
            text = input_fn(f"Briefly explain your answer to {qid} in your own words: ").strip()
            if text:
                explanations[qid] = text
                break
            output_fn("Explanation cannot be blank.")

    with open(notes_path, "a", encoding="utf-8") as f:
        for qid, text in explanations.items():
            f.write(f"{qid} (answered {answers[qid]}): {text}\n")
    output_fn(f"Explanations saved to {notes_path} for mentor discussion.")
    return score