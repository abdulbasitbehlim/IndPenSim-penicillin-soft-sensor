"""Small, dependency-free checks; these do not train a model or fetch data."""
from __future__ import annotations

from collections import defaultdict
import csv
import hashlib
import json
import math
from pathlib import Path
import re
import statistics
import unittest

ROOT = Path(__file__).resolve().parents[1]


def read_csv(relative):
    with (ROOT / relative).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def digest(value):
    if isinstance(value, str):
        value = value.encode("utf-8")
    return hashlib.sha256(value).hexdigest()


def metrics(rows, prediction_column):
    actual = [float(row["Penicillin concentration(P:g/L)"]) for row in rows]
    predicted = [float(row[prediction_column]) for row in rows]
    if not all(math.isfinite(x) for x in actual + predicted):
        raise AssertionError("Non-finite archived target or prediction.")
    mean = statistics.fmean(actual)
    squared_error = math.fsum((a - p) ** 2 for a, p in zip(actual, predicted))
    target_variance_sum = math.fsum((a - mean) ** 2 for a in actual)
    return {
        "MAE": math.fsum(abs(a - p) for a, p in zip(actual, predicted)) / len(actual),
        "RMSE": math.sqrt(squared_error / len(actual)),
        "R2": 1.0 - squared_error / target_variance_sum,
    }


class RepositoryChecks(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.provenance = json.loads((ROOT / "docs/notebook_provenance.json").read_text(encoding="utf-8"))
        cls.predictions = read_csv("results/main/cross_validated_predictions.csv")
        cls.by_condition = defaultdict(list)
        cls.by_batch = defaultdict(list)
        for row in cls.predictions:
            cls.by_condition[row["Condition"]].append(row)
            cls.by_batch[int(row["Batch_ID"])].append(row)
        cls.model_columns = {
            "Normal-only HGB": "Normal_Only_Prediction",
            "Fault-aware HGB": "Fault_Aware_Prediction",
        }

    def test_required_files_and_licence(self):
        for name in [
            "README.md", "LICENSE", "CITATION.cff", "DATA_SOURCES.md", ".gitignore",
            ".gitattributes", "requirements.txt", "requirements/baseline.txt", "requirements/main.txt",
            "notebooks/baseline.ipynb", "notebooks/main.ipynb", "docs/FIGURES.md",
            "docs/REPRODUCIBILITY.md", "docs/RESULTS_GUIDE.md", "data/raw/README.md", "data/splits/README.md",
        ]:
            self.assertTrue((ROOT / name).is_file(), name)
        self.assertTrue((ROOT / "LICENSE").read_text().startswith("MIT License\n"))
        self.assertIn("CC BY 4.0", (ROOT / "DATA_SOURCES.md").read_text())
        self.assertEqual(
            {path.name for path in (ROOT / "notebooks").glob("*.ipynb")},
            {"main.ipynb", "baseline.ipynb"},
        )

    def test_notebook_json_syntax_and_clean_outputs(self):
        for item in self.provenance["notebooks"]:
            notebook = json.loads((ROOT / item["path"]).read_text(encoding="utf-8"))
            self.assertEqual(notebook["nbformat"], 4)
            setup = next(
                cell for cell in notebook["cells"]
                if cell["cell_type"] == "code" and "REQUIREMENTS_FILE =" in "".join(cell["source"])
            )
            requirement_path = re.search(
                r"REQUIREMENTS_FILE = ['\"]([^'\"]+)['\"]", "".join(setup["source"])
            ).group(1)
            self.assertTrue((ROOT / requirement_path).is_file())
            ids = [cell["id"] for cell in notebook["cells"]]
            self.assertEqual(len(ids), len(set(ids)))
            for cell in notebook["cells"]:
                if cell["cell_type"] != "code":
                    continue
                self.assertEqual(cell["outputs"], [])
                self.assertIsNone(cell["execution_count"])
                compile("".join(cell["source"]), f"{item['path']}:{cell['id']}", "exec")

    def test_original_scientific_sources_are_preserved(self):
        # Setup paths may legitimately be edited by a user. Scientific changes
        # should be versioned and described rather than silently changing the
        # historical snapshot. This check intentionally catches such changes.
        for item in self.provenance["notebooks"]:
            notebook = json.loads((ROOT / item["path"]).read_text(encoding="utf-8"))
            by_id = {cell["id"]: cell for cell in notebook["cells"]}
            preserved_count = 0
            for record in item["code_cells"]:
                cell = by_id[record["repository_cell_id"]]
                if record["scientific_source_unchanged"]:
                    self.assertEqual(digest("".join(cell["source"])), record["original_source_sha256"])
                    preserved_count += 1
                else:
                    self.assertTrue(record["setup_change"])
            self.assertGreater(preserved_count, 8)

    def test_archived_results_have_not_been_replaced(self):
        for item in self.provenance["archived_results"]:
            self.assertEqual(digest((ROOT / item["path"]).read_bytes()), item["sha256"], item["path"])

    def test_prediction_rows_and_held_out_membership(self):
        self.assertEqual(len(self.predictions), 113935)
        self.assertEqual(len(self.by_condition["Normal"]), 102410)
        self.assertEqual(len(self.by_condition["Fault"]), 11525)
        self.assertEqual(set(self.by_batch), set(range(1, 101)))
        keys = {(int(r["Batch_ID"]), float(r["Time (h)"])) for r in self.predictions}
        self.assertEqual(len(keys), len(self.predictions))
        fold_batches = defaultdict(set)
        for row in self.predictions:
            fold_batches[row["Outer_Fold"]].add(int(row["Batch_ID"]))
        self.assertEqual(len(fold_batches), 15)
        normals_seen = set()
        for fold in range(1, 6):
            batches = fold_batches[f"Normal fold {fold}"]
            self.assertEqual(len(batches), 18)
            self.assertTrue(normals_seen.isdisjoint(batches))
            normals_seen.update(batches)
            for start in [1, 31, 61]:
                self.assertEqual(len(batches & set(range(start, start + 30))), 6)
        self.assertEqual(normals_seen, set(range(1, 91)))
        for batch in range(91, 101):
            self.assertEqual(fold_batches[f"Fault LOBO {batch}"], {batch})

    def test_pooled_metric_arithmetic(self):
        overall = read_csv("results/main/cross_validated_overall_metrics.csv")
        self.assertEqual(len(overall), 4)
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        for row in overall:
            recomputed = metrics(self.by_condition[row["Condition"]], self.model_columns[row["Model"]])
            for name, value in recomputed.items():
                self.assertTrue(math.isclose(value, float(row[name]), abs_tol=1e-9, rel_tol=1e-9))
                self.assertIn(f"{float(row[name]):.4f}", readme)

    def test_individual_batch_metric_arithmetic(self):
        batch_metrics = read_csv("results/main/cross_validated_batch_metrics.csv")
        self.assertEqual(len(batch_metrics), 200)
        for row in batch_metrics:
            data = self.by_batch[int(row["Batch_ID"])]
            self.assertEqual(len(data), int(row["Rows"]))
            computed = metrics(data, self.model_columns[row["Model"]])
            for name, value in computed.items():
                self.assertTrue(math.isclose(value, float(row[name]), abs_tol=1e-9, rel_tol=1e-9))

    def test_paired_batch_summary(self):
        rows = read_csv("results/main/cross_validated_batch_metrics.csv")
        lookup = {(int(r["Batch_ID"]), r["Model"]): float(r["RMSE"]) for r in rows}
        for summary in read_csv("results/main/paired_batch_bootstrap.csv"):
            batches = range(1, 91) if summary["Condition"] == "Normal" else range(91, 101)
            differences = [lookup[b, "Fault-aware HGB"] - lookup[b, "Normal-only HGB"] for b in batches]
            self.assertEqual(len(differences), int(summary["Batches"]))
            self.assertEqual(sum(d < 0 for d in differences), int(summary["Batches_Improved"]))
            self.assertAlmostEqual(statistics.fmean(differences), float(summary["Mean_RMSE_Difference_Aware_Minus_Normal_Only"]), places=11)
            self.assertAlmostEqual(statistics.median(differences), float(summary["Median_RMSE_Difference_Aware_Minus_Normal_Only"]), places=11)

    def test_risk_warning_rate_arithmetic(self):
        normal = self.by_condition["Normal"]
        fault = self.by_condition["Fault"]
        affected = [r for r in fault if int(r["Fault_Affected"]) == 1]
        pre_onset = [r for r in fault if int(r["Fault_Affected"]) == 0]
        expected_groups = [normal, affected, pre_onset]
        summaries = read_csv("results/main/fault_risk_summary.csv")
        for summary, rows in zip(summaries[:3], expected_groups):
            warned = sum(float(r["Fault_Risk_Probability"]) >= 0.5 for r in rows)
            self.assertEqual(len(rows), int(summary["Rows"]))
            self.assertAlmostEqual(warned / len(rows), float(summary["Value"]), places=12)

    def test_earlier_cv_membership(self):
        rows = read_csv("results/experiments/experiment_1_repeated_batch_cv_fold_metrics.csv")
        self.assertEqual(len(rows), 25)
        for repeat in range(1, 6):
            seen = set()
            folds = [row for row in rows if int(row["Repeat"]) == repeat]
            self.assertEqual(len(folds), 5)
            for row in folds:
                ids = set(json.loads(row["Test_Batch_IDs"]))
                self.assertEqual(int(row["Train_Batches"]), 72)
                self.assertEqual(int(row["Test_Batches"]), 18)
                self.assertEqual(len(ids), 18)
                self.assertTrue(seen.isdisjoint(ids))
                seen.update(ids)
            self.assertEqual(seen, set(range(1, 91)))

    def test_feature_metadata_and_full_run(self):
        metadata = json.loads((ROOT / "results/main/run_metadata.json").read_text())
        self.assertEqual(metadata["run_mode"], "full")
        self.assertEqual(metadata["normal_outer_folds_completed"], 5)
        self.assertEqual(metadata["fault_outer_folds_completed"], 10)
        self.assertEqual(metadata["max_iter"], 180)
        self.assertEqual(metadata["fault_weight_multiplier"], 3.0)
        self.assertEqual(len(metadata["model_features"]), 36)
        self.assertEqual(len(metadata["reliability_features"]), 34)
        self.assertNotIn("Time (h)", metadata["reliability_features"])
        self.assertNotIn("Cumulative_Sugar_Feed", metadata["reliability_features"])

    def test_markdown_local_links(self):
        for path in ROOT.rglob("*.md"):
            for target in re.findall(r"\]\(([^)]+)\)", path.read_text(encoding="utf-8")):
                if target.startswith(("http://", "https://", "mailto:", "#")):
                    continue
                local_target = target.split("#", 1)[0]
                self.assertTrue((path.parent / local_target).exists(), f"{path.relative_to(ROOT)}: {target}")


if __name__ == "__main__":
    unittest.main()
