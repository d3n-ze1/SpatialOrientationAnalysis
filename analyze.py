from pathlib import Path
import csv

DATA_DIR = Path("data")
OUTPUT_FILE = Path("output/scores.csv")

results = []

for file in DATA_DIR.glob("*.txt"):

    with open(file, "r", encoding="utf-8") as f:
        # Get all lines
        lines = f.readlines()

    participant = None
    errors = []

    # Subject number from first line
    first_line = lines[0].strip().split()
    if len(first_line) == 2:
        participant = int(first_line[-1])

    # Work on only Lines 7–15
    for line in lines[6:15]:

        parts = line.strip().split()

        if not parts:
            continue

        try:
            errors.append(float(parts[-1]))
        except ValueError:
            pass

    if participant and errors:

        mean_error = sum(errors) / len(errors)

        results.append([
            participant,
            round(mean_error, 2)
        ])

# Sort by participant number
results.sort(key=lambda x: x[0])

OUTPUT_FILE.parent.mkdir(exist_ok=True)

with open(OUTPUT_FILE, "w", newline="") as f:

    writer = csv.writer(f)
    writer.writerow(["ParticipantNumber", "MeanScore"])

    writer.writerows(results)

print(f"Processed {len(results)} participants")
