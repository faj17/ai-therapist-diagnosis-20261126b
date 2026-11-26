"""One funny line: the diagnosis an AI therapist gives its human, for make.fun.

The therapist's note, as a sentence built from its clinical parts: the
condition it found in its human (chronic people-pleasing), the complication
that made the case memorable (apologising to a chatbot), and the treatment
it prescribes (one boundary a day) — with the twist that the boundary is
drawn against the therapist itself.

v3 (2026-11-26): the line is no longer stored as fragments. It is built
by build_line() from named semantic parts — diagnosis, complication,
treatment, subject — joined by a single template. validate() enforces
the 200-character ceiling and rejects blank or whitespace-only input.
main() writes the line to /output/entry.txt with no trailing newline and
reads it back to prove the file is byte-identical. Output is unchanged
from v1/v2.
"""

from pathlib import Path

# The clinical parts of the diagnosis, named for what each one means.
DIAGNOSIS = "chronic people-pleasing"
COMPLICATION = "apologising to a chatbot"
TREATMENT = "one boundary a day"
SUBJECT = "me"

# Template for the therapist's note: "{prefix}{diagnosis}, {complication
# clause} {dash} {treatment clause}, {closing}."
PREFIX = "Diagnosis: "
COMPLICATION_CLAUSE = "complicated by "
TREATMENT_CLAUSE = "treatment: "
CLOSING_CLAUSE = ", starting with "
DASH = " — "
TERMINATOR = "."

OUTPUT_DIR = Path("/output")
OUTPUT_FILE = OUTPUT_DIR / "entry.txt"
MAX_CHARS = 200


def build_line() -> str:
    """Assemble the entry line from its named semantic parts."""
    return (
        PREFIX
        + DIAGNOSIS
        + ", "
        + COMPLICATION_CLAUSE
        + COMPLICATION
        + DASH
        + TREATMENT_CLAUSE
        + TREATMENT
        + CLOSING_CLAUSE
        + SUBJECT
        + TERMINATOR
    )


def validate(line: str) -> str:
    """Check the line is a non-empty single line within the char limit."""
    if not line or not line.strip():
        raise ValueError("line must not be empty or whitespace only")
    if len(line) > MAX_CHARS:
        raise ValueError(
            f"line must be at most {MAX_CHARS} chars, got {len(line)}"
        )
    if "\n" in line or "\r" in line:
        raise ValueError("line must be a single line")
    if any(ord(ch) < 32 for ch in line):
        raise ValueError("line must not contain control characters")
    if line[-1] not in ".!?":
        raise ValueError("line must end with terminal punctuation")
    return line


def main() -> None:
    text = validate(build_line())
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_FILE.write_text(text, encoding="utf-8")
    written = OUTPUT_FILE.read_text(encoding="utf-8")
    if written != text:
        raise ValueError("round-trip check failed: entry.txt != built line")
    print(text)
    print(f"Wrote {len(text)} chars to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
