#!/usr/bin/env python3
"""
Empirical adversarial test suite for Milestone 1 (Frontend Design Skill Installation).
Author: m1_chal_1 (teamwork_challenger)
"""

import os
import sys
import json
import hashlib
import subprocess
from pathlib import Path

def run_tests():
    failures = []
    print("=" * 60)
    print("STARTING EMPIRICAL ADVERSARIAL CHALLENGE TEST SUITE (M1)")
    print("=" * 60)

    # ---------------------------------------------------------
    # Test 1: File Existence, Type, and Permissions
    # ---------------------------------------------------------
    print("\n[TEST 1] File Existence, Read Permissions & Size Thresholds")
    repo_root = Path(r"d:\Mini5th").resolve()
    skill_dir = repo_root / ".agents" / "skills" / "frontend-design"
    skill_file = skill_dir / "SKILL.md"
    license_file = skill_dir / "LICENSE.txt"
    lock_file = repo_root / "skills-lock.json"

    targets = [
        (skill_file, "SKILL.md", 8000, 15000),
        (license_file, "LICENSE.txt", 9000, 20000),
        (lock_file, "skills-lock.json", 50, 5000),
    ]

    for path, name, min_sz, max_sz in targets:
        try:
            if not path.exists():
                failures.append(f"Existence failure: {name} not found at {path}")
                print(f"  [-] FAIL: {name} does not exist at {path}")
                continue
            if not path.is_file():
                failures.append(f"Type failure: {name} is not a regular file")
                print(f"  [-] FAIL: {name} is not a regular file")
                continue
            
            size = path.stat().st_size
            if size < min_sz or size > max_sz:
                failures.append(f"Size failure: {name} size {size} not in [{min_sz}, {max_sz}]")
                print(f"  [-] FAIL: {name} size {size} out of bounds [{min_sz}, {max_sz}]")
            else:
                print(f"  [+] PASS: {name} exists, size={size} bytes (bounds: [{min_sz}, {max_sz}])")

            # Test byte-level reading
            with open(path, "rb") as f:
                raw_bytes = f.read()
                if len(raw_bytes) != size:
                    failures.append(f"Read integrity failure: {name} read {len(raw_bytes)} != {size}")
                else:
                    print(f"  [+] PASS: {name} byte-level read verified ({len(raw_bytes)} bytes)")
        except Exception as e:
            failures.append(f"Exception checking {name}: {e}")
            print(f"  [-] ERROR: {name} check raised {e}")

    # ---------------------------------------------------------
    # Test 2: Directory Cleanliness & No Zero-Byte / Corrupted Files
    # ---------------------------------------------------------
    print("\n[TEST 2] Directory Integrity & Cleanliness")
    try:
        entries = list(skill_dir.iterdir())
        entry_names = {e.name for e in entries}
        print(f"  [+] Found entries in {skill_dir.name}: {entry_names}")
        for entry in entries:
            if entry.is_file():
                sz = entry.stat().st_size
                if sz == 0:
                    failures.append(f"Zero-byte file detected: {entry.name}")
                    print(f"  [-] FAIL: Zero-byte file: {entry.name}")
                else:
                    print(f"  [+] PASS: Entry {entry.name} is non-zero ({sz} bytes)")
    except Exception as e:
        failures.append(f"Exception inspecting directory: {e}")
        print(f"  [-] ERROR: Directory inspection failed: {e}")

    # ---------------------------------------------------------
    # Test 3: SKILL.md Frontmatter & Content Adversarial Check
    # ---------------------------------------------------------
    print("\n[TEST 3] SKILL.md Frontmatter & Content Integrity")
    try:
        with open(skill_file, "r", encoding="utf-8") as f:
            content = f.read()

        if not content.startswith("---"):
            failures.append("SKILL.md does not start with '---' YAML frontmatter delimiter")
            print("  [-] FAIL: Missing initial '---'")
        else:
            print("  [+] PASS: SKILL.md begins with '---'")

        parts = content.split("---", 2)
        if len(parts) < 3:
            failures.append("SKILL.md does not have closing '---' delimiter")
            print("  [-] FAIL: Missing closing '---'")
        else:
            frontmatter_raw = parts[1]
            body = parts[2]
            
            # Check required YAML frontmatter properties
            has_name = "name: frontend-design" in frontmatter_raw
            has_desc = "description:" in frontmatter_raw
            has_lic = "license:" in frontmatter_raw

            if not has_name:
                failures.append("SKILL.md frontmatter missing 'name: frontend-design'")
                print("  [-] FAIL: Missing 'name: frontend-design'")
            else:
                print("  [+] PASS: Frontmatter contains 'name: frontend-design'")

            if not has_desc:
                failures.append("SKILL.md frontmatter missing 'description:'")
                print("  [-] FAIL: Missing 'description:'")
            else:
                print("  [+] PASS: Frontmatter contains 'description'")

            if not has_lic:
                failures.append("SKILL.md frontmatter missing 'license:'")
                print("  [-] FAIL: Missing 'license:'")
            else:
                print("  [+] PASS: Frontmatter contains 'license'")

            # Check body content semantics (Anthropic guidance keywords)
            key_guidelines = [
                "Typography",
                "Color",
                "Layout",
                "Spacing",
                "animation",
            ]
            for kw in key_guidelines:
                if kw.lower() not in body.lower():
                    failures.append(f"SKILL.md missing guideline concept: {kw}")
                    print(f"  [-] FAIL: Skill body missing concept: {kw}")
                else:
                    print(f"  [+] PASS: Skill body includes guidance on '{kw}'")

            print(f"  [+] PASS: SKILL.md body size={len(body)} characters")
    except Exception as e:
        failures.append(f"Exception checking SKILL.md: {e}")
        print(f"  [-] ERROR: SKILL.md check failed: {e}")

    # ---------------------------------------------------------
    # Test 4: LICENSE.txt Content Check
    # ---------------------------------------------------------
    print("\n[TEST 4] LICENSE.txt Semantic Validation")
    try:
        with open(license_file, "r", encoding="utf-8") as f:
            lic_text = f.read()
        if "Apache License" not in lic_text or "Version 2.0" not in lic_text:
            failures.append("LICENSE.txt does not contain Apache License Version 2.0 header")
            print("  [-] FAIL: LICENSE.txt missing Apache 2.0 header")
        else:
            print("  [+] PASS: LICENSE.txt contains valid Apache License 2.0 text")
    except Exception as e:
        failures.append(f"Exception checking LICENSE.txt: {e}")
        print(f"  [-] ERROR: LICENSE.txt check failed: {e}")

    # ---------------------------------------------------------
    # Test 5: skills-lock.json Schema & Structure Check
    # ---------------------------------------------------------
    print("\n[TEST 5] skills-lock.json Schema & Structure")
    try:
        with open(lock_file, "r", encoding="utf-8") as f:
            lock_json = json.load(f)

        if not isinstance(lock_json, dict):
            failures.append("skills-lock.json root is not a JSON object")
            print("  [-] FAIL: Root is not an object")
        else:
            print("  [+] PASS: skills-lock.json is a valid JSON object")

        if lock_json.get("version") != 1:
            failures.append(f"skills-lock.json version {lock_json.get('version')} != 1")
            print("  [-] FAIL: Incorrect version")
        else:
            print("  [+] PASS: skills-lock.json version == 1")

        skills = lock_json.get("skills")
        if not isinstance(skills, dict):
            failures.append("skills-lock.json 'skills' property is not an object")
            print("  [-] FAIL: 'skills' property is not an object")
        elif "frontend-design" not in skills:
            failures.append("skills-lock.json does not register 'frontend-design'")
            print("  [-] FAIL: 'frontend-design' not registered in 'skills'")
        else:
            fd = skills["frontend-design"]
            print(f"  [+] Found skills['frontend-design']: {fd}")
            expected_props = {
                "source": "anthropics/skills",
                "sourceType": "github",
                "skillPath": "skills/frontend-design/SKILL.md",
            }
            for prop, val in expected_props.items():
                if fd.get(prop) != val:
                    failures.append(f"skills-lock.json property mismatch: {prop}='{fd.get(prop)}' != '{val}'")
                    print(f"  [-] FAIL: {prop} mismatch")
                else:
                    print(f"  [+] PASS: {prop} == '{val}'")

            computed_hash = fd.get("computedHash")
            if not computed_hash or len(computed_hash) != 64:
                failures.append(f"computedHash is not 64-char SHA-256 hash: {computed_hash}")
                print("  [-] FAIL: invalid computedHash length")
            else:
                print(f"  [+] PASS: computedHash is valid 64-char hex: {computed_hash}")

            # Verify what the hash actually corresponds to
            with open(skill_file, "rb") as f:
                sha_skill = hashlib.sha256(f.read()).hexdigest()
            print(f"  [i] SHA-256 of local SKILL.md: {sha_skill}")
            print(f"  [i] Lockfile computedHash:      {computed_hash}")
            if sha_skill == computed_hash:
                print("  [+] PASS: Lockfile computedHash EXACTLY matches local SKILL.md byte hash!")
            else:
                # Some CLIs hash the folder or normalized line endings, let's test LF vs CRLF
                with open(skill_file, "rb") as f:
                    crlf_to_lf = f.read().replace(b"\r\n", b"\n")
                    sha_lf = hashlib.sha256(crlf_to_lf).hexdigest()
                print(f"  [i] SHA-256 of LF-normalized SKILL.md: {sha_lf}")
                if sha_lf == computed_hash:
                    print("  [+] PASS: computedHash matches LF-normalized SKILL.md hash!")
                else:
                    print("  [i] Note: computedHash may correspond to repo tree or specific upstream commit hash.")
    except Exception as e:
        failures.append(f"Exception checking skills-lock.json: {e}")
        print(f"  [-] ERROR: skills-lock.json check failed: {e}")

    # ---------------------------------------------------------
    # Test 6: CLI Telemetry via `npx -y skills@latest list --json`
    # ---------------------------------------------------------
    print("\n[TEST 6] CLI Telemetry (`npx -y skills@latest list --json`)")
    try:
        cmd = ["npx.cmd", "-y", "skills@latest", "list", "--json"]
        print(f"  [i] Running command: {' '.join(cmd)}")
        res = subprocess.run(
            cmd,
            cwd=str(repo_root),
            capture_output=True,
            text=True,
            timeout=30
        )
        print(f"  [i] Exit code: {res.returncode}")
        if res.returncode != 0:
            failures.append(f"CLI command failed with exit code {res.returncode}: {res.stderr}")
            print(f"  [-] FAIL: CLI command stderr: {res.stderr}")
        else:
            cli_output = res.stdout.strip()
            print(f"  [i] Raw CLI stdout:\n{cli_output}")
            
            # Parse JSON
            cli_data = json.loads(cli_output)
            if not isinstance(cli_data, list):
                failures.append(f"CLI output is not a JSON list: {type(cli_data)}")
                print(f"  [-] FAIL: CLI output is not a list")
            else:
                fd_cli_matches = [x for x in cli_data if x.get("name") == "frontend-design"]
                if not fd_cli_matches:
                    failures.append("CLI output does not contain entry with name 'frontend-design'")
                    print("  [-] FAIL: 'frontend-design' not found in CLI list")
                else:
                    fd_cli = fd_cli_matches[0]
                    print(f"  [+] PASS: Found CLI entry: {json.dumps(fd_cli, indent=2)}")
                    
                    # Verify fields
                    if fd_cli.get("status") != "tracked":
                        failures.append(f"CLI status '{fd_cli.get('status')}' != 'tracked'")
                        print("  [-] FAIL: status != tracked")
                    else:
                        print("  [+] PASS: status == 'tracked'")

                    if fd_cli.get("scope") != "project":
                        failures.append(f"CLI scope '{fd_cli.get('scope')}' != 'project'")
                        print("  [-] FAIL: scope != project")
                    else:
                        print("  [+] PASS: scope == 'project'")

                    agents = fd_cli.get("agents", [])
                    if "Antigravity" not in agents:
                        failures.append(f"CLI agents '{agents}' does not include 'Antigravity'")
                        print("  [-] FAIL: Antigravity not in agents")
                    else:
                        print(f"  [+] PASS: 'Antigravity' registered in agents: {agents}")

                    cli_path = Path(fd_cli.get("path", ""))
                    if not cli_path.exists() or not cli_path.is_dir():
                        failures.append(f"CLI path '{cli_path}' does not resolve to existing directory")
                        print(f"  [-] FAIL: CLI path '{cli_path}' does not exist as directory")
                    else:
                        print(f"  [+] PASS: CLI path correctly resolves to existing directory: {cli_path}")
    except Exception as e:
        failures.append(f"Exception during CLI execution: {e}")
        print(f"  [-] ERROR: CLI execution failed: {e}")

    # ---------------------------------------------------------
    # Test 7: Windows Path Resolution & Cross-Platform Edge Cases
    # ---------------------------------------------------------
    print("\n[TEST 7] Windows Path Resolution & Normalization")
    test_paths = [
        r"d:\Mini5th\.agents\skills\frontend-design\SKILL.md",
        r"D:\Mini5th\.agents\skills\frontend-design\SKILL.md",
        r"d:/Mini5th/.agents/skills/frontend-design/SKILL.md",
        r"D:/Mini5th/.agents/skills/frontend-design/SKILL.md",
        r".\.agents\skills\frontend-design\SKILL.md",
        r"./.agents/skills/frontend-design/SKILL.md",
    ]
    for p_str in test_paths:
        p = Path(p_str)
        if not p.is_absolute():
            p = (repo_root / p).resolve()
        if not p.exists():
            failures.append(f"Path format failed to resolve: {p_str}")
            print(f"  [-] FAIL: Path {p_str} did not resolve")
        else:
            print(f"  [+] PASS: Resolved {p_str} -> {p} (exists={p.exists()})")

    # ---------------------------------------------------------
    # Summary & Final Assessment
    # ---------------------------------------------------------
    print("\n" + "=" * 60)
    print("EMIRICAL ADVERSARIAL TEST SUMMARY")
    print("=" * 60)
    if failures:
        print(f"[VERDICT] REQUEST_CHANGES ({len(failures)} failures encountered)")
        for idx, f in enumerate(failures, 1):
            print(f"  {idx}. {f}")
        return False
    else:
        print("[VERDICT] APPROVE (All 7 test suites passed with 0 failures)")
        return True

if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
