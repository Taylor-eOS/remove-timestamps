from pathlib import Path

def is_time_line(line):
    stripped = line.strip()
    return all(c in "0123456789:., " for c in stripped) and any(c.isdigit() for c in stripped)

def remove_timestamps(text):
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    kept_lines = [line for line in lines if not is_time_line(line)]
    return " ".join(kept_lines)

def main():
    input_file = input("Input file: ").strip()
    path = Path(input_file)
    output_path = path.with_name(path.stem + "_text.txt")
    text = path.read_text(encoding="utf-8")
    cleaned = remove_timestamps(text)
    output_path.write_text(cleaned, encoding="utf-8")
    print(f"Processed: {path} to {output_path}")

if __name__ == "__main__":
    main()
