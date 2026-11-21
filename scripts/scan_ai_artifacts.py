#!/usr/bin/env python3
"""
scripts/scan_ai_artifacts.py
Adversarial automated scanner for AI artifacts, forbidden buzzwords,
and hallucinated technical claims across StayMart repository.
"""

import os
import sys
import json
import re
from pathlib import Path

# Repository root
REPO_ROOT = Path(__file__).resolve().parent.parent

# Target scopes to scan
TARGET_DIRECTORIES = [
    REPO_ROOT / "report",
    REPO_ROOT / "frontend",
    REPO_ROOT / "database",
]

TARGET_FILES = [
    REPO_ROOT / "scripts" / "compile_report_pdf.py",
    REPO_ROOT / "README.md",
]

# Blacklisted expressions explicitly mandated by Milestone 3 specification:
BLACKLIST_PATTERNS = [
    {
        "id": "transient_demographic_cohorts",
        "name": "Transient demographic cohorts",
        "pattern": r"\btransient\s+demographic(\s+cohorts)?\b",
        "flags": re.IGNORECASE,
        "category": "mandated",
        "scope": "all",
    },
    {
        "id": "interdependent_necessities",
        "name": "Interdependent necessities",
        "pattern": r"\binterdependent\s+necessities\b",
        "flags": re.IGNORECASE,
        "category": "mandated",
        "scope": "all",
    },
    {
        "id": "structural_bottlenecks",
        "name": "Structural bottlenecks",
        "pattern": r"\bstructural\s+bottlenecks\b",
        "flags": re.IGNORECASE,
        "category": "mandated",
        "scope": "all",
    },
    {
        "id": "bespoke_glassmorphism",
        "name": "Bespoke glassmorphism",
        "pattern": r"\bbespoke\s+glassmorphism\b",
        "flags": re.IGNORECASE,
        "category": "mandated",
        "scope": "all",
    },
    {
        "id": "bespoke_non_generic",
        "name": "Bespoke, non-generic",
        "pattern": r"\bbespoke[,\s]+non-generic\b",
        "flags": re.IGNORECASE,
        "category": "mandated",
        "scope": "all",
    },
    {
        "id": "tfidf_ai_algorithm",
        "name": "TF-IDF AI algorithm",
        "pattern": r"\bTF-?IDF\s+AI\s+algorithm\b",
        "flags": re.IGNORECASE,
        "category": "mandated",
        "scope": "all",
    },
    {
        "id": "marketplace_inc",
        "name": "Marketplace Inc.",
        "pattern": r"\bMarketplace\s+Inc\.?\b",
        "flags": re.IGNORECASE,
        "category": "mandated",
        "scope": "all",
    },
    {
        "id": "in_contemporary_urban",
        "name": "In contemporary urban",
        "pattern": r"\bin\s+contemporary\s+urban\b",
        "flags": re.IGNORECASE,
        "category": "mandated",
        "scope": "all",
    },
    {
        "id": "prohibitive_capital_expenditures",
        "name": "Prohibitive capital expenditures",
        "pattern": r"\bprohibitive\s+capital\s+expenditures\b",
        "flags": re.IGNORECASE,
        "category": "mandated",
        "scope": "all",
    },
    {
        "id": "virtual_thread_scheduling",
        "name": "Virtual thread scheduling",
        "pattern": r"\bvirtual\s+thread\s+scheduling\b",
        "flags": re.IGNORECASE,
        "category": "mandated",
        "scope": "all",
    },
    {
        "id": "java_21_claim",
        "name": "Java 21 backend claim",
        "pattern": r"\bJava\s+21\b(?!\s*\(?(optional|or\s+later|compatibility|compatible|LTS\s+bytecode|bytecode)\)?)",
        "flags": re.IGNORECASE,
        "category": "mandated",
        "scope": "report_and_readme",
    },
    {
        "id": "dark_mode_glassmorphic",
        "name": "Dark-mode glassmorphic",
        "pattern": r"\bdark-?mode\s+glassmorphic\b",
        "flags": re.IGNORECASE,
        "category": "mandated",
        "scope": "all",
    },
    {
        "id": "slate_dark_hex",
        "name": "Slate dark (#0f172a) in UI themes",
        "pattern": r"\bslate\s+dark\s+\(#0f172a\)",
        "flags": re.IGNORECASE,
        "category": "mandated",
        "scope": "all",
    },
    {
        "id": "pivotal",
        "name": "Pivotal (generic AI filler)",
        "pattern": r"\bpivotal\b",
        "flags": re.IGNORECASE,
        "category": "mandated",
        "scope": "all",
    },
    {
        "id": "delve_into",
        "name": "Delve into",
        "pattern": r"\bdelve\s+into\b",
        "flags": re.IGNORECASE,
        "category": "mandated",
        "scope": "all",
    },
    {
        "id": "seamlessly_marketing",
        "name": "Seamlessly in marketing copy",
        "pattern": r"\bseamlessly\b",
        "flags": re.IGNORECASE,
        "category": "mandated",
        "scope": "marketing_only",  # Scanned in frontend/ and README marketing copy
    },
    # Extended adversarial patterns:
    {
        "id": "hyper_local_socioeconomic",
        "name": "Hyper-local socioeconomic",
        "pattern": r"\bhyper-?local\s+socioeconomic\b",
        "flags": re.IGNORECASE,
        "category": "extended_adversarial",
        "scope": "all",
    },
    {
        "id": "tapestry_filler",
        "name": "Tapestry AI filler",
        "pattern": r"\b(rich\s+)?tapestry\b",
        "flags": re.IGNORECASE,
        "category": "extended_adversarial",
        "scope": "all",
    },
    {
        "id": "testament_filler",
        "name": "Testament AI filler",
        "pattern": r"\bstands\s+as\s+a\s+testament\b",
        "flags": re.IGNORECASE,
        "category": "extended_adversarial",
        "scope": "all",
    },
    {
        "id": "holistic_buzzword",
        "name": "Holistic buzzword",
        "pattern": r"\bholistic\b",
        "flags": re.IGNORECASE,
        "category": "extended_adversarial",
        "scope": "all",
    },
]

# Extensions to scan
TEXT_EXTENSIONS = {
    ".tex", ".html", ".js", ".css", ".sql", ".py", ".md", ".json", ".txt"
}

# Directories or files to ignore (e.g. node_modules, .git, binary pdfs, virtualenvs)
IGNORE_DIRS = {
    ".git", "node_modules", ".gemini", "__pycache__", ".agents", "venv", ".venv", "dist", "build"
}


def collect_target_files():
    files = set()
    for d in TARGET_DIRECTORIES:
        if not d.exists():
            continue
        for root, dirs, filenames in os.walk(d):
            dirs[:] = [dir_name for dir_name in dirs if dir_name not in IGNORE_DIRS]
            for fn in filenames:
                ext = os.path.splitext(fn)[1].lower()
                if ext in TEXT_EXTENSIONS:
                    files.add(Path(root) / fn)

    for f in TARGET_FILES:
        if f.exists():
            files.add(f)
    return sorted(list(files))


def check_scope_match(scope_type, file_path: Path):
    rel_path = file_path.relative_to(REPO_ROOT).as_posix()
    if scope_type == "all":
        return True
    elif scope_type == "marketing_only":
        # Scanned in frontend/ or README.md
        return rel_path.startswith("frontend/") or rel_path == "README.md"
    elif scope_type == "report_and_readme":
        return rel_path.startswith("report/") or rel_path == "README.md"
    return True


def scan_file(file_path: Path):
    rel_path = file_path.relative_to(REPO_ROOT).as_posix()
    try:
        content = file_path.read_text(encoding="utf-8", errors="replace")
    except Exception as e:
        return []

    lines = content.splitlines()
    findings = []

    for pattern_def in BLACKLIST_PATTERNS:
        if not check_scope_match(pattern_def["scope"], file_path):
            continue

        compiled_regex = re.compile(pattern_def["pattern"], pattern_def["flags"])
        for idx, line in enumerate(lines, 1):
            for match in compiled_regex.finditer(line):
                findings.append({
                    "pattern_id": pattern_def["id"],
                    "pattern_name": pattern_def["name"],
                    "category": pattern_def["category"],
                    "file": rel_path,
                    "line_number": idx,
                    "matched_text": match.group(0),
                    "line_snippet": line.strip()[:160],
                })

    return findings


def run_scanner():
    target_files = collect_target_files()
    all_findings = []
    file_counts = len(target_files)

    for file_path in target_files:
        matches = scan_file(file_path)
        all_findings.extend(matches)

    # Summarize per pattern
    summary = {}
    for p in BLACKLIST_PATTERNS:
        summary[p["id"]] = {
            "name": p["name"],
            "category": p["category"],
            "scope": p["scope"],
            "match_count": 0,
            "findings": []
        }

    for f in all_findings:
        summary[f["pattern_id"]]["match_count"] += 1
        summary[f["pattern_id"]]["findings"].append(f)

    # Split mandated vs extended
    mandated_violations = [f for f in all_findings if f["category"] == "mandated"]
    extended_violations = [f for f in all_findings if f["category"] == "extended_adversarial"]

    print("=" * 80)
    print("STAYMART REPOSITORY ADVERSARIAL AI ARTIFACT SCANNER")
    print("=" * 80)
    print(f"Total target files scanned: {file_counts}")
    print(f"Scanned directories: report/, frontend/, database/, scripts/compile_report_pdf.py, README.md")
    print("-" * 80)
    print(f"{'PATTERN NAME':<40} | {'CATEGORY':<20} | {'MATCH COUNT':<10}")
    print("-" * 80)

    for p in BLACKLIST_PATTERNS:
        p_id = p["id"]
        cnt = summary[p_id]["match_count"]
        status_marker = "PASS" if cnt == 0 else "FAIL"
        print(f"{p['name']:<40} | {p['category']:<20} | {cnt} ({status_marker})")

    print("=" * 80)
    print(f"Mandated Pattern Violations: {len(mandated_violations)}")
    print(f"Extended Pattern Violations: {len(extended_violations)}")
    print(f"Total Violations: {len(all_findings)}")
    print("=" * 80)

    if all_findings:
        print("\nVIOLATION DETAILS:")
        for idx, item in enumerate(all_findings, 1):
            print(f"[{idx}] {item['file']}:{item['line_number']} - {item['pattern_name']}")
            print(f"    Matched: '{item['matched_text']}'")
            print(f"    Snippet: {item['line_snippet']}\n")

    output_json = REPO_ROOT / "scripts" / "scan_ai_artifacts_results.json"
    result_data = {
        "files_scanned_count": file_counts,
        "scanned_files": [f.relative_to(REPO_ROOT).as_posix() for f in target_files],
        "total_findings": len(all_findings),
        "mandated_violations_count": len(mandated_violations),
        "extended_violations_count": len(extended_violations),
        "verdict": "PASS" if len(mandated_violations) == 0 else "FAIL",
        "pattern_summary": summary,
        "all_findings": all_findings,
    }

    output_json.write_text(json.dumps(result_data, indent=2), encoding="utf-8")
    print(f"Detailed scan results written to: {output_json.relative_to(REPO_ROOT)}")

    return 0 if len(mandated_violations) == 0 else 1


if __name__ == "__main__":
    sys.exit(run_scanner())
