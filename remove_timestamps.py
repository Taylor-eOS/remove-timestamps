import os
import re
from pathlib import Path
from urllib.parse import urlparse
from urllib.request import url2pathname

MINUTE_WORDS = {"minute", "minutes", "second", "seconds", "mins", "secs", "min", "sec"}
THRESHOLD = 10
PRINT_SCORE = True

def score_timestamp(line):
    if PRINT_SCORE: print(line)
    stripped = line.strip()
    if not stripped:
        if PRINT_SCORE: print(f"not stripped {score}")
        return 0
    score = 0
    lower = stripped.lower()
    words = lower.replace(",", " ").replace(":", " ").split()
    has_digit = any(c.isdigit() for c in stripped)
    if not has_digit:
        if PRINT_SCORE: print(f"has no digit {score}")
        return -100
    time_word_count = sum(1 for w in words for tw in MINUTE_WORDS if w == tw)
    score += time_word_count * 40
    if PRINT_SCORE: print(f"time_word_count {score}")
    non_time_words = [w for w in words if not any(c.isdigit() for c in w) and w not in MINUTE_WORDS and w not in {",", ""}]
    score -= len(non_time_words) * 15
    if PRINT_SCORE: print(f"non_time_words {score}")
    if re.fullmatch(r'\d{1,2}:\d{2}', stripped):
        score += 60
        if PRINT_SCORE: print(f"non_time_words {score}")
    all_time_chars = all(c in "0123456789:., " for c in stripped)
    if all_time_chars:
        score += 30
        if PRINT_SCORE: print(f"all_time_chars {score}")
    score -= min(len(stripped), 80)
    if len(stripped) > 60:
        score -= 40
        if PRINT_SCORE: print(f"len {score}")
    return score

def remove_timestamps(text):
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    scores = [score_timestamp(line) for line in lines]
    is_ts = [s >= THRESHOLD for s, line in zip(scores, lines)]
    for i in range(1, len(lines) - 1):
        if not is_ts[i]:
            continue
        prev_ts = is_ts[i - 1] if i > 0 else False
        next_ts = is_ts[i + 1] if i < len(lines) - 1 else False
        if prev_ts or next_ts:
            is_ts[i] = True
        else:
            is_ts[i] = scores[i] >= 5
    kept = [line for line, ts in zip(lines, is_ts) if not ts]
    return " ".join(kept)

def main():
    input_file = input("Input file: ").strip()
    if input_file.startswith("file://"):
        parsed_url = urlparse(input_file)
        input_file = url2pathname(parsed_url.path)
    path = Path(input_file)
    output_path = path.with_name(path.stem + "_text.txt")
    text = path.read_text(encoding="utf-8")
    cleaned = remove_timestamps(text)
    output_path.write_text(cleaned, encoding="utf-8")
    print(f"Processed: {path} to {output_path}")

if __name__ == "__main__":
    main()
