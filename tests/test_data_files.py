"""Verify the included source exports and their connection to saved results."""
from __future__ import annotations

from collections import Counter
import csv
import hashlib
import json
import math
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
TARGET = "Penicillin concentration(P:g/L)"
TIME = "Time (h)"
SPLITS = {
    "train_normal_60_batches.csv": (67820, 60, "Train", "train_batches"),
    "validation_normal_15_batches.csv": (17510, 15, "Validation", "validation_batches"),
    "test_normal_15_batches.csv": (17080, 15, "Normal_Test", "normal_test_batches"),
    "test_fault_10_batches.csv": (11525, 10, "Fault_Test", "fault_test_batches"),
}


def read_csv(path):
    with (ROOT / path).open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


class DatasetFileChecks(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest = json.loads((ROOT / "data/splits/manifest.json").read_text())
        cls.records = {item["file"]: item for item in cls.manifest["files"]}
        cls.summaries, cls.targets = {}, {}
        for filename in SPLITS:
            with (ROOT / "data/splits" / filename).open(newline="", encoding="utf-8-sig") as handle:
                reader = csv.DictReader(handle)
                columns = reader.fieldnames
                counts, labels, key_counts = Counter(), Counter(), Counter()
                last_times, issues = {}, []
                for row in reader:
                    if None in row or any(value is None for value in row.values()):
                        issues.append("Incomplete or extra CSV field")
                        continue
                    batch, time = int(row["Batch_ID"]), float(row[TIME])
                    target = float(row[TARGET])
                    if not math.isfinite(time) or not math.isfinite(target):
                        issues.append("Non-finite time or target")
                    if batch in last_times and time <= last_times[batch]:
                        issues.append("Non-increasing within-batch time")
                    last_times[batch] = time
                    key = batch, time
                    if key in cls.targets:
                        issues.append("Duplicate batch/time key across source rows")
                    cls.targets[key] = target
                    key_counts[key] += 1
                    counts[batch] += 1
                    labels[row["Data_Split"]] += 1
                cls.summaries[filename] = {
                    "columns": columns, "counts": counts, "labels": labels,
                    "key_counts": key_counts, "issues": issues,
                }

    def test_original_csv_bytes_and_sizes(self):
        self.assertEqual(set(self.records), set(SPLITS))
        for filename, record in self.records.items():
            raw = (ROOT / "data/splits" / filename).read_bytes()
            self.assertEqual(hashlib.sha256(raw).hexdigest(), record["sha256"])
            self.assertEqual(len(raw), record["bytes"])
            self.assertLess(len(raw), 100 * 1024 * 1024)
            self.assertEqual(len(record["source_copies"]), 2)
            self.assertEqual({item["sha256"] for item in record["source_copies"]}, {record["sha256"]})

    def test_split_counts_labels_and_disjoint_batches(self):
        seen = set()
        for filename, (rows, batches, label, _) in SPLITS.items():
            summary = self.summaries[filename]
            ids = set(summary["counts"])
            self.assertEqual(sum(summary["counts"].values()), rows)
            self.assertEqual(len(ids), batches)
            self.assertEqual(summary["labels"], Counter({label: rows}))
            self.assertEqual(sorted(ids), self.records[filename]["batches"])
            self.assertTrue(seen.isdisjoint(ids))
            seen.update(ids)
            if label == "Fault_Test":
                self.assertEqual(ids, set(range(91, 101)))
            else:
                for first in (1, 31, 61):
                    self.assertEqual(len(ids & set(range(first, first + 30))), batches // 3)
        self.assertEqual(seen, set(range(1, 101)))
        self.assertEqual(sum(sum(s["counts"].values()) for s in self.summaries.values()), 113935)

    def test_same_batch_assignment_as_original_result_runs(self):
        for folder in ("baseline_earlier", "baseline"):
            original = json.loads((ROOT / "results" / folder / "fault_aware_batch_split.json").read_text())
            for filename, (_, _, _, original_key) in SPLITS.items():
                self.assertEqual(set(self.summaries[filename]["counts"]), set(original[original_key]))

    def test_column_schema_and_valid_time_target_rows(self):
        expected_columns = self.manifest["column_names"]
        self.assertEqual(len(expected_columns), 41)
        self.assertEqual(len(set(expected_columns)), 41)
        metadata = json.loads((ROOT / "results/main/run_metadata.json").read_text())
        for summary in self.summaries.values():
            self.assertEqual(summary["columns"], expected_columns)
            self.assertEqual(summary["issues"], [])
            self.assertTrue(all(n == 1 for n in summary["key_counts"].values()))
            for name in metadata["model_features"][:20]:
                self.assertIn(name, expected_columns)
        self.assertIn(TARGET, expected_columns)
        self.assertIn("Fault reference(Fault_ref:Fault ref)", expected_columns)

    def test_input_targets_match_every_main_held_out_row(self):
        rows = read_csv("results/main/cross_validated_predictions.csv")
        seen = set()
        for row in rows:
            key = int(row["Batch_ID"]), float(row[TIME])
            self.assertIn(key, self.targets)
            self.assertNotIn(key, seen)
            seen.add(key)
            self.assertTrue(math.isclose(self.targets[key], float(row[TARGET]), rel_tol=1e-12, abs_tol=1e-12))
        self.assertEqual(seen, set(self.targets))
        self.assertEqual(len(seen), 113935)

    def test_data_paths_documented_and_explicitly_tracked(self):
        readme = (ROOT / "README.md").read_text()
        split_readme = (ROOT / "data/splits/README.md").read_text()
        ignore = (ROOT / ".gitignore").read_text().splitlines()
        for filename in SPLITS:
            self.assertIn("data/splits/" + filename, readme)
            self.assertIn(filename, split_readme)
            self.assertIn("!/data/splits/" + filename, ignore)
        self.assertIn("data/splits/*.csv -text", (ROOT / ".gitattributes").read_text())

    def test_each_result_file_has_a_purpose_in_its_folder_readme(self):
        for folder in ("baseline_earlier", "baseline", "experiments", "main"):
            directory = ROOT / "results" / folder
            guide = (directory / "README.md").read_text()
            for path in directory.iterdir():
                if path.is_file() and path.name != "README.md":
                    self.assertIn("](" + path.name + ")", guide, str(path))
            if folder == "baseline":
                for path in (directory / "figures").glob("*.png"):
                    self.assertIn("](figures/" + path.name + ")", guide)

    def test_both_baseline_runs_prediction_tables_reproduce_own_metrics(self):
        for folder in ("baseline_earlier", "baseline"):
            summaries = read_csv(f"results/{folder}/normal_and_fault_test_results.csv")
            for filename, summary in zip(("normal_test_predictions.csv", "fault_test_predictions.csv"), summaries):
                rows = read_csv(f"results/{folder}/{filename}")
                actual = [float(row[TARGET]) for row in rows]
                predicted = [float(row["Predicted_Target"]) for row in rows]
                mean = math.fsum(actual) / len(actual)
                squared = math.fsum((a - p) ** 2 for a, p in zip(actual, predicted))
                computed = {
                    "MAE": math.fsum(abs(a - p) for a, p in zip(actual, predicted)) / len(actual),
                    "RMSE": math.sqrt(squared / len(actual)),
                    "R2": 1.0 - squared / math.fsum((a - mean) ** 2 for a in actual),
                }
                for metric, value in computed.items():
                    self.assertTrue(math.isclose(value, float(summary[metric]), rel_tol=1e-9, abs_tol=1e-9),
                                    f"{folder}/{filename}: {metric}")


if __name__ == "__main__":
    unittest.main()
