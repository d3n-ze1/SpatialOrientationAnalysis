from pathlib import Path
import csv

DATA_DIR = Path("data")
OUTPUT_FILE = Path("output/scores.csv")

results = []

for file in DATA_DIR.glob("*.txt"):

    participant = None
    errors = []

    with open(file, "r", encoding="utf-8") as f:
        for line in f:

            parts = line.strip().split()

            if not parts:
                continue

            # Subject line
            if parts[0] == "Subject" and len(parts) == 2:
                participant = parts[1]
                continue

            # Trial rows begin with participant number
            if parts[0].isdigit():

                try:
                    target_angle = float(parts[-3])
                    estimate_angle = float(parts[-2])
                    angular_error = float(parts[-1])

                    errors.append(angular_error)

                except (ValueError, IndexError):
                    pass

    if participant and errors:

        mean_error = sum(errors) / len(errors)

        results.append([
            participant,
            round(mean_error, 2)
        ])

OUTPUT_FILE.parent.mkdir(exist_ok=True)

with open(OUTPUT_FILE, "w", newline="") as f:

    writer = csv.writer(f)
    writer.writerow(["ParticipantNumber", "MeanScore"])

    writer.writerows(results)

print(f"Processed {len(results)} participants")
