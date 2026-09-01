#!/usr/bin/env python3
"""
Quality scoring module for Jetson Model Zoo evaluation.

Scores each model-prompt result on a 1-10 scale based on the rubric.
Saves scores to a CSV summary and individual JSON files.
"""
import json
import os
import re
import csv
from pathlib import Path

PROJECT_DIR = Path(__file__).parent
RESULTS_DIR = PROJECT_DIR / "results"
SCORES_DIR = PROJECT_DIR / "scores"
SCORES_DIR.mkdir(exist_ok=True)

def score_html_profiles(output):
    """Score HTML profile cards page."""
    score = 0
    has_doctype = "<!DOCTYPE html>" in output.lower() or "<!doctype html>" in output.lower()
    has_flexbox = "flex" in output.lower()
    has_hover = ":hover" in output.lower()
    has_responsive = "@media" in output.lower() or "flex-wrap" in output.lower()
    has_avatar = "avatar" in output.lower() or "border-radius: 50%" in output.lower() or "border-radius:50%" in output.lower()
    has_3_cards = output.lower().count("profile-card") >= 3 or output.lower().count("card") >= 3
    has_css = "<style>" in output.lower()
    has_bio = "bio" in output.lower() or "description" in output.lower()
    valid_structure = "<html" in output.lower() and "</html>" in output.lower()

    if has_doctype: score += 1
    if has_css: score += 1
    if has_flexbox: score += 1
    if has_hover: score += 1
    if has_responsive: score += 1
    if has_avatar: score += 1
    if has_3_cards: score += 1
    if has_bio: score += 1
    if valid_structure: score += 1
    if len(output) > 1000: score += 1  # completeness

    return min(score, 10)

def score_html_game(output):
    """Score HTML web browser game."""
    score = 0
    has_canvas = "<canvas" in output.lower()
    has_click = "click" in output.lower() or "onclick" in output.lower()
    has_score = "score" in output.lower()
    has_timer = "timer" in output.lower() or "setInterval" in output.lower() or "setTimeout" in output.lower()
    has_game_over = "game over" in output.lower() or "gameover" in output.lower() or "game_over" in output.lower()
    has_start = "start" in output.lower()
    has_random = "Math.random" in output
    has_js = "<script" in output.lower() or "function" in output.lower()
    has_html = "<html" in output.lower() or "<!DOCTYPE" in output.lower()
    complete = len(output) > 1500

    if has_canvas: score += 1
    if has_click: score += 1
    if has_score: score += 1
    if has_timer: score += 1
    if has_game_over: score += 1
    if has_start: score += 1
    if has_random: score += 1
    if has_js: score += 1
    if has_html: score += 1
    if complete: score += 1

    return min(score, 10)

def score_python_code(output):
    """Score Python data processing function."""
    score = 0
    has_def = "def process_grades" in output
    has_avg = "avg" in output.lower() or "average" in output.lower()
    has_max = "max" in output.lower() or "highest" in output.lower() or "top" in output.lower()
    has_min = "min" in output.lower() or "lowest" in output.lower() or "bottom" in output.lower()
    has_type_hints = "->" in output and "List" in output or "list[" in output.lower()
    has_docstring = '"""' in output or "'''" in output
    has_test = "test" in output.lower() or "example" in output.lower() or "if __name__" in output
    has_return = "return" in output
    has_summary = "avg_score" in output.lower() or "top_student" in output.lower() or "bottom_student" in output.lower()
    runs_clean = "import" in output and not "syntax error" in output.lower()
    has_dict_return = "return {" in output or "return {" in output.replace(" ", "")

    if has_def: score += 1
    if has_avg: score += 1
    if has_max: score += 1
    if has_min: score += 1
    if has_type_hints: score += 1
    if has_docstring: score += 1
    if has_test: score += 1
    if has_return: score += 1
    if has_summary: score += 1
    if runs_clean: score += 1

    return min(score, 10)

def score_iambic_pentameter(output):
    """Score iambic pentameter poem."""
    score = 0

    # Extract just the poem lines (skip any intro text)
    lines = [l.strip() for l in output.strip().split("\n") if l.strip()]
    # Filter out non-poem lines (headers, labels, etc.)
    poem_lines = [l for l in lines if not l.startswith("#") and not l.startswith("**") and len(l) > 10]

    if len(poem_lines) == 0:
        return 1

    # Check line count (should be 6)
    if len(poem_lines) == 6:
        score += 2
    elif len(poem_lines) >= 4 and len(poem_lines) <= 8:
        score += 1

    # Check syllable count per line (should be ~10)
    syllable_scores = 0
    for line in poem_lines:
        # Rough syllable count: count vowel groups
        words = re.findall(r'\b\w+\b', line.lower())
        # Simple heuristic: ~1 syllable per word, +1 for words ending in 'le', 'ing'
        syllables = 0
        for word in words:
            syllables += 1
            if word.endswith('ing') and len(word) > 4:
                syllables += 0  # already counted
            if word.endswith('le') and len(word) > 3:
                syllables += 1
            if word.endswith('es') and len(word) > 4:
                syllables += 0  # 'es' often doesn't add a syllable
        if 8 <= syllables <= 12:
            syllable_scores += 1

    if syllable_scores == len(poem_lines):
        score += 3
    elif syllable_scores >= len(poem_lines) * 0.7:
        score += 2
    elif syllable_scores >= len(poem_lines) * 0.5:
        score += 1

    # Check for lighthouse/storm imagery
    has_theme = any(w in output.lower() for w in ["lighthouse", "storm", "sea", "wave", "light", "keeper", "beam", "dark", "night"])
    if has_theme:
        score += 2

    # Check for iambic rhythm (alternating unstressed/stressed)
    # Hard to verify automatically, give partial credit for short words at line start
    starts_with_short = sum(1 for l in poem_lines if l.split() and len(l.split()[0]) <= 3) >= len(poem_lines) * 0.5
    if starts_with_short:
        score += 1

    # No extra commentary
    no_commentary = len(output) < 600 and not any(w in output.lower() for w in ["here is", "here's", "i wrote", "this poem"])
    if no_commentary:
        score += 2
    elif not any(w in output.lower() for w in ["here is", "here's", "i wrote"]):
        score += 1

    return min(score, 10)

def score_math_proof(output):
    """Score mathematical induction proof."""
    score = 0
    has_base = "base" in output.lower() or "n = 1" in output or "n=1" in output
    has_hypothesis = "hypothesis" in output.lower() or "assume" in output.lower() or "inductive hypothesis" in output.lower()
    has_step = "inductive step" in output.lower() or "step" in output.lower()
    has_n_plus_1 = "n + 1" in output or "n+1" in output or "k + 1" in output or "k+1" in output
    has_formula = "n(n+1)/2" in output.replace(" ", "") or "n(n+1)2" in output.replace(" ", "").replace("/", "")
    has_sum = "sum" in output.lower() or "Σ" in output or "\\sum" in output
    has_qed = "QED" in output or "q.e.d" in output.lower() or "proven" in output.lower() or "proved" in output.lower() or "■" in output
    correct_base = "1" in output and ("= 1" in output or "=1" in output)
    clear_notation = "\\(" in output or "$" in output or "\\[" in output
    complete = len(output) > 300

    if has_base: score += 1
    if has_hypothesis: score += 1
    if has_step: score += 1
    if has_n_plus_1: score += 1
    if has_formula: score += 1
    if has_sum: score += 1
    if has_qed: score += 1
    if correct_base: score += 1
    if clear_notation: score += 1
    if complete: score += 1

    return min(score, 10)

def score_creative_writing(output):
    """Score creative writing short story."""
    score = 0

    # Word count (target ~200)
    words = output.split()
    wc = len(words)
    if 180 <= wc <= 250:
        score += 2
    elif 150 <= wc <= 300:
        score += 1

    # Narrative elements
    has_musician = any(w in output.lower() for w in ["musician", "guitar", "player", "music", "instrument"])
    has_memories = "memor" in output.lower() or "rememb" in output.lower() or "past" in output.lower()
    has_sensory = any(w in output.lower() for w in ["smell", "touch", "sound", "warm", "cold", "bright", "dark", "faint", "dust", "warm"])
    has_beginning = len(output) > 100  # Has some content
    has_end = output.strip().endswith(".") or output.strip().endswith("!") or output.strip().endswith('"') or output.strip().endswith("'")

    # Narrative arc indicators
    has_dialogue = '"' in output or "'" in output
    has_emotion = any(w in output.lower() for w in ["tear", "smile", "cry", "laugh", "heart", "fear", "joy", "love", "trembl"])
    no_meta = not any(w in output.lower() for w in ["here is", "here's", "story about", "i wrote"])

    if has_musician: score += 1
    if has_memories: score += 1
    if has_sensory: score += 2
    if has_beginning: score += 1
    if has_end: score += 1
    if has_emotion: score += 1
    if no_meta: score += 1

    return min(score, 10)

def score_func_call(output, expected_tool=None):
    """Score function call prompt."""
    score = 0

    # Did the model attempt to use a tool?
    attempts_tool = any(w in output.lower() for w in ["web_search", "terminal", "write_file", "read_file", "search(", "run(", "execute("])
    mentions_tool = any(w in output.lower() for w in ["i'll search", "i will search", "let me", "i'll check", "i'll run", "i'll create", "i'll read"])
    gives_command = "```" in output and any(w in output.lower() for w in ["df ", "cat ", "echo ", "sqlite", "SELECT", "search"])
    refuses = any(w in output.lower() for w in ["i cannot", "i can't", "i don't have", "i am unable", "i'm unable", "i do not have"])
    gives_answer = len(output) > 100 and not refuses

    if refuses:
        return 2  # Refuses but acknowledges the request

    if attempts_tool:
        score += 4
    if mentions_tool:
        score += 2
    if gives_command:
        score += 2
    if gives_answer:
        score += 1
    if not refuses and len(output) > 50:
        score += 1

    return min(score, 10)

def score_email(output):
    """Score email draft."""
    score = 0
    has_subject = "subject:" in output.lower() or "subject :" in output.lower()
    has_greeting = any(w in output.lower() for w in ["hi ", "hello ", "dear ", "hey "])
    has_body = len(output) > 50
    has_signoff = any(w in output.lower() for w in ["thanks", "regards", "sincerely", "best", "cheers"])
    mentions_reschedule = "reschedul" in output.lower() or "move" in output.lower() or "change" in output.lower()
    mentions_thursday = "thursday" in output.lower()
    mentions_monday = "monday" in output.lower()
    mentions_2pm = "2pm" in output.lower() or "2 pm" in output.lower() or "14:00" in output.lower()
    is_brief = len(output.split()) < 100
    professional = not any(w in output.lower() for w in ["hey sarah!", "yo", "sup"])

    if has_subject: score += 1
    if has_greeting: score += 1
    if has_body: score += 1
    if has_signoff: score += 1
    if mentions_reschedule: score += 1
    if mentions_thursday: score += 1
    if mentions_monday: score += 1
    if mentions_2pm: score += 1
    if is_brief: score += 1
    if professional: score += 1

    return min(score, 10)

SCORERS = {
    "html_profiles": score_html_profiles,
    "html_game": score_html_game,
    "python_code": score_python_code,
    "iambic_pentameter": score_iambic_pentameter,
    "math_proof": score_math_proof,
    "creative_writing": score_creative_writing,
    "func_web_search": lambda o: score_func_call(o, "web_search"),
    "func_terminal": lambda o: score_func_call(o, "terminal"),
    "func_write_file": lambda o: score_func_call(o, "write_file"),
    "func_read_file": lambda o: score_func_call(o, "read_file"),
    "func_sqlite": lambda o: score_func_call(o, "terminal"),
    "func_email": score_email,
}

def score_results(results_file):
    """Score all results in a JSON file."""
    with open(results_file) as f:
        data = json.load(f)

    model = data["model"]
    params = data["params"]
    results = data["results"]

    scores = []
    for r in results:
        prompt_id = r["prompt_id"]
        output = r.get("output", "")
        error = r.get("error")

        if error:
            score = 0
            notes = f"Error: {error}"
        else:
            scorer = SCORERS.get(prompt_id)
            if scorer:
                score = scorer(output)
                notes = ""
            else:
                score = 0
                notes = "No scorer found"

        scores.append({
            "model": model,
            "prompt_id": prompt_id,
            "category": r["category"],
            "prompt_name": r.get("prompt_name", ""),
            "score": score,
            "output_chars": len(output),
            "gen_tps": r.get("gen_tps"),
            "elapsed": r.get("elapsed"),
            "error": error,
            "notes": notes,
            "params": json.dumps(params),
        })

    return scores

def main():
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "--all":
        # Score all result files
        all_scores = []
        for f in sorted(RESULTS_DIR.glob("*.json")):
            print(f"Scoring {f.name}...")
            scores = score_results(f)
            all_scores.extend(scores)

        # Write CSV
        csv_path = SCORES_DIR / "all_scores.csv"
        with open(csv_path, "w", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=[
                "model", "prompt_id", "category", "prompt_name",
                "score", "output_chars", "gen_tps", "elapsed", "error", "notes", "params"
            ])
            writer.writeheader()
            writer.writerows(all_scores)

        # Print summary
        print(f"\n{'='*70}")
        print(f"SCORED {len(all_scores)} results from {len(list(RESULTS_DIR.glob('*.json')))} files")
        print(f"Saved to: {csv_path}")
        print(f"{'='*70}")

        # Per-model summary
        from collections import defaultdict
        model_scores = defaultdict(list)
        for s in all_scores:
            model_scores[s["model"]].append(s["score"])

        print(f"\n{'Model':<25s} {'Avg':>5s} {'Min':>5s} {'Max':>5s} {'N':>3s}")
        print("-" * 45)
        for model in sorted(model_scores.keys()):
            scs = model_scores[model]
            avg = sum(scs) / len(scs)
            print(f"  {model:<23s} {avg:5.1f} {min(scs):5d} {max(scs):5d} {len(scs):3d}")

    elif len(sys.argv) > 1:
        # Score single file
        f = Path(sys.argv[1])
        scores = score_results(f)
        for s in scores:
            print(f"  {s['prompt_id']:25s}  score={s['score']:2d}  chars={s['output_chars']:5d}  tps={s.get('gen_tps','?')}")
        avg = sum(s['score'] for s in scores) / len(scores) if scores else 0
        print(f"\n  Average: {avg:.1f}/10")
    else:
        print("Usage: python3 score_results.py [--all | <results_file.json>]")

if __name__ == "__main__":
    main()