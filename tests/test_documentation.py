"""Check documentation and original figures without training or network access."""
from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path
import re
import struct
import unittest
from urllib.parse import unquote
import zlib

ROOT = Path(__file__).resolve().parents[1]


def rows(path):
    with (ROOT / path).open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def heading_ids(text):
    """GitHub-style IDs for the simple ATX headings used in these documents."""
    ids, counts = set(), {}
    in_fence = False
    for line in text.splitlines():
        if line.startswith(("```", "~~~")):
            in_fence = not in_fence
            continue
        match = re.match(r"^#{1,6}\s+(.+?)\s*#*$", line)
        if in_fence or not match:
            continue
        heading = re.sub(r"\[([^]]+)\]\([^)]*\)", r"\1", match.group(1))
        slug = re.sub(r"[^\w\- ]", "", heading.lower()).replace(" ", "-")
        occurrence = counts.get(slug, 0)
        counts[slug] = occurrence + 1
        ids.add(slug if occurrence == 0 else f"{slug}-{occurrence}")
    return ids


class DocumentationChecks(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest = json.loads((ROOT / "docs/figure_provenance.json").read_text())
        cls.figures = cls.manifest["figures"]
        cls.image_paths = {item[key] for item in cls.figures for key in ("path", "notebook_display_path")}

    def test_original_figure_inventory_and_hashes(self):
        self.assertEqual(len(self.figures), 14)
        self.assertEqual(len({item["id"] for item in self.figures}), 14)
        self.assertEqual(len(self.image_paths), 20)
        self.assertEqual({str(p.relative_to(ROOT)) for p in (ROOT / "results").rglob("*.png")}, self.image_paths)
        for item in self.figures:
            for path_key, hash_key in [("path", "sha256"), ("notebook_display_path", "notebook_display_sha256")]:
                self.assertEqual(hashlib.sha256((ROOT / item[path_key]).read_bytes()).hexdigest(), item[hash_key])

    def test_png_integrity(self):
        for name in sorted(self.image_paths):
            with self.subTest(image=name):
                data = (ROOT / name).read_bytes()
                self.assertEqual(data[:8], b"\x89PNG\r\n\x1a\n")
                offset, kinds = 8, []
                while offset < len(data):
                    self.assertGreaterEqual(len(data) - offset, 12)
                    size = struct.unpack(">I", data[offset:offset + 4])[0]
                    kind = data[offset + 4:offset + 8]
                    end = offset + 12 + size
                    self.assertLessEqual(end, len(data))
                    payload = data[offset + 8:offset + 8 + size]
                    crc = struct.unpack(">I", data[offset + 8 + size:end])[0]
                    self.assertEqual(zlib.crc32(kind + payload) & 0xffffffff, crc)
                    if kind == b"IHDR":
                        width, height = struct.unpack(">II", payload[:8])
                        self.assertGreater(width, 0)
                        self.assertGreater(height, 0)
                    kinds.append(kind)
                    offset = end
                self.assertEqual(kinds[0], b"IHDR")
                self.assertEqual(kinds[-1], b"IEND")
                self.assertIn(b"IDAT", kinds)

    def test_all_figures_are_visible_and_variants_linked(self):
        embedded, linked = set(), set()
        for path in (ROOT / "docs/figures").glob("*.md"):
            text = path.read_text(encoding="utf-8")
            for alt, target in re.findall(r"!\[([^]]*)\]\(([^)]+)\)", text):
                self.assertTrue(alt.strip(), path)
                embedded.add((path.parent / target).resolve())
            for target in re.findall(r"\]\(([^)]+)\)", text):
                if not target.startswith(("https://", "http://", "#")):
                    linked.add((path.parent / target.split("#", 1)[0]).resolve())
        for item in self.figures:
            self.assertIn((ROOT / item["path"]).resolve(), embedded)
            self.assertIn((ROOT / item["notebook_display_path"]).resolve(), linked)

    def test_gallery_metric_captions_match_results(self):
        experiments = (ROOT / "docs/figures/EXPERIMENTS.md").read_text()
        for row in rows("results/experiments/experiment_4_model_comparison_test.csv"):
            self.assertIn(f"{float(row['RMSE']):.3f}", experiments)
        for row in rows("results/experiments/experiment_3_fault_phase_overall.csv"):
            for metric in ("Mean_Batch_MAE", "MAE"):
                self.assertIn(f"{float(row[metric]):.3f}", experiments)
        final = (ROOT / "docs/figures/FAULT_INCLUSIVE.md").read_text()
        for row in rows("results/main/cross_validated_overall_metrics.csv"):
            self.assertIn(f"{float(row['RMSE']):.4f}", final)
        for row in rows("results/main/fault_risk_summary.csv")[:3]:
            self.assertIn(f"{float(row['Value']) * 100:.2f}%", final)

    def test_citation_uses_actual_repository(self):
        citation = (ROOT / "CITATION.cff").read_text()
        self.assertIn('repository-code: "https://github.com/abdulbasitbehlim/IndPenSim-penicillin-soft-sensor"', citation)
        self.assertIn("license: MIT", citation)
        self.assertNotIn("YOUR_USERNAME", citation)

    def test_retired_publishing_guides_are_absent(self):
        retired = ("GITHUB_UPLOAD_GUIDE", "UPLOAD_CHECKLIST")
        for path in ROOT.rglob("*.md"):
            text = path.read_text(encoding="utf-8")
            for name in retired:
                self.assertNotIn(name, text, str(path.relative_to(ROOT)))
                self.assertNotIn(name, path.name)
        self.assertFalse((ROOT / "docs/REPRODUCBILITY").exists())
        self.assertFalse((ROOT / "test/test_repository.py").exists())

    def test_local_heading_links_resolve(self):
        for path in ROOT.rglob("*.md"):
            for target in re.findall(r"\]\(([^)]+)\)", path.read_text(encoding="utf-8")):
                if target.startswith(("http://", "https://", "mailto:")) or "#" not in target:
                    continue
                filename, anchor = target.split("#", 1)
                destination = path if not filename else path.parent / unquote(filename)
                if destination.suffix == ".md" and anchor:
                    self.assertTrue(destination.is_file(), target)
                    self.assertIn(unquote(anchor), heading_ids(destination.read_text(encoding="utf-8")), f"{path}: {target}")


if __name__ == "__main__":
    unittest.main()
