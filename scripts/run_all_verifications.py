#!/usr/bin/env python3
"""
scripts/run_all_verifications.py
=============================================================================
StayMart Unified Master Verification Runner (Milestone 5 - Feature 27)
=============================================================================

Sequentially executes the complete automated verification pipeline:
  1. Spring Boot Backend Tests:      python scripts/run_backend_tests.py (13 JUnit 5 tests)
  2. Headless Chrome Viewport Tests: node scripts/run_viewport_tests.js (30 viewports 320px–1920px)
  3. Navigation & DOM Verification:  python scripts/verify_m1_navigation.py (8 test suites)
  4. AI Artifact Pattern Scanner:    python scripts/scan_ai_artifacts.py (87 target files)
  5. Cloud Deployment & Audit:       python scripts/test_m4_adversarial_audit.py (render.yaml, vercel.json)
  6. Academic PDF Report Compiler:   python scripts/compile_report_pdf.py (StayMart_Project_Report.pdf)
  7. Multi-Tier API Smoke Suite:     python scripts/run_smoke_tests.py (REST, DTO, JPA, Flask ML)

Outputs a comprehensive executive summary dashboard and exits with code 0 iff
all 7 suites pass with 0 defects.
"""

import os
import sys
import time
import json
import subprocess
import argparse
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


class SuiteResult:
    def __init__(self, index, name, command, tests_run=0, passed=0, failed=0, duration=0.0, return_code=0, stdout="", stderr=""):
        self.index = index
        self.name = name
        self.command = command
        self.tests_run = tests_run
        self.passed = passed
        self.failed = failed
        self.duration = duration
        self.return_code = return_code
        self.stdout = stdout
        self.stderr = stderr
        self.status = "PASS" if (return_code == 0 and failed == 0) else "FAIL"


def execute_suite(index, name, cmd, parser_fn):
    # Support simulated adversarial failure injection without modifying repository files
    if os.environ.get("STAYMART_SIMULATE_SUITE_FAIL") == str(index):
        cmd = [sys.executable, "-c", "import sys; sys.stderr.write('FATAL: Injected simulated adversarial audit violation!\\n'); sys.exit(1)"]

    print("\n" + "=" * 90)
    print(f"[{index}/7] RUNNING SUITE: {name}")
    print(f"Command: {' '.join(cmd)}")
    print("=" * 90)

    start_time = time.time()
    try:
        proc = subprocess.run(
            cmd,
            cwd=str(REPO_ROOT),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace"
        )
        duration = time.time() - start_time
        stdout = proc.stdout or ""
        stderr = proc.stderr or ""
        ret_code = proc.returncode

        # Print output to console for real-time visibility
        if stdout:
            # Print indented sample or full if brief
            lines = stdout.strip().splitlines()
            if len(lines) > 25:
                for line in lines[:10]:
                    print(f"  | {line}")
                print(f"  | ... [{len(lines) - 20} lines truncated for brevity] ...")
                for line in lines[-10:]:
                    print(f"  | {line}")
            else:
                for line in lines:
                    print(f"  | {line}")

        if stderr and ret_code != 0:
            print("  STDERR:")
            for line in stderr.strip().splitlines()[:15]:
                print(f"    ! {line}")

        # Parse suite metrics
        tests_run, passed, failed = parser_fn(ret_code, stdout, stderr)

        status_str = "PASS" if (ret_code == 0 and failed == 0) else "FAIL"
        print(f"\n---> SUITE {index} COMPLETED: {status_str} ({passed}/{tests_run} passed, duration: {duration:.2f}s)")

        return SuiteResult(
            index=index,
            name=name,
            command=' '.join(cmd),
            tests_run=tests_run,
            passed=passed,
            failed=failed,
            duration=duration,
            return_code=ret_code,
            stdout=stdout,
            stderr=stderr
        )

    except Exception as ex:
        duration = time.time() - start_time
        print(f"\n---> SUITE {index} EXCEPTION: {ex}")
        return SuiteResult(
            index=index,
            name=name,
            command=' '.join(cmd),
            tests_run=1,
            passed=0,
            failed=1,
            duration=duration,
            return_code=1,
            stdout="",
            stderr=str(ex)
        )


# =============================================================================
# Suite Metric Parsers
# =============================================================================

def parse_backend_tests(ret_code, stdout, stderr):
    # Expecting 13 JUnit 5 tests
    tests_run = 13
    passed = 13 if ret_code == 0 else 0
    failed = 0 if ret_code == 0 else 13

    # Try extracting exact numbers from JUnit console
    for line in stdout.splitlines():
        if "tests successful" in line:
            parts = line.split()
            if len(parts) >= 2 and parts[1].isdigit():
                passed = int(parts[1])
        if "tests failed" in line:
            parts = line.split()
            if len(parts) >= 2 and parts[1].isdigit():
                failed = int(parts[1])
        if "tests found" in line:
            parts = line.split()
            if len(parts) >= 2 and parts[1].isdigit():
                tests_run = int(parts[1])

    return tests_run, passed, failed


def parse_viewport_tests(ret_code, stdout, stderr):
    tests_run = 30
    if ret_code != 0:
        return tests_run, 0, tests_run

    # Check JSON result file if present
    json_path = REPO_ROOT / "scripts" / "viewport_test_results.json"
    if json_path.exists():
        try:
            with open(json_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            vp_checks = data.get("viewportChecks", [])
            defects = data.get("defectsIdentified", [])
            total = len(vp_checks) if vp_checks else tests_run
            failed = len([c for c in vp_checks if c.get("status") == "FAIL"]) + len(defects)
            passed = total - failed
            return total, max(passed, 0), failed
        except Exception:
            pass

    # Fallback to output parsing
    tests_run = 30
    passed = 30 if ret_code == 0 and "OVERALL VERDICT: APPROVE" in stdout else 0
    failed = tests_run - passed
    return tests_run, passed, failed


def parse_navigation_tests(ret_code, stdout, stderr):
    # Expecting 8 test suites
    tests_run = 8
    passed = 8 if ret_code == 0 and "VERDICT: APPROVE" in stdout else 0
    failed = tests_run - passed

    for line in stdout.splitlines():
        if "Total Test Suites Passed:" in line:
            m = line.split(":")[-1].strip().split("/")
            if len(m) == 2:
                passed = int(m[0].strip())
                tests_run = max(int(m[1].strip()), passed)
        if "Total Defects Found:" in line:
            failed = int(line.split(":")[-1].strip())

    return tests_run, passed, failed


def parse_ai_artifacts(ret_code, stdout, stderr):
    scanned = 87
    if ret_code != 0:
        return scanned, 0, scanned

    # Check JSON result file
    json_path = REPO_ROOT / "scripts" / "scan_ai_artifacts_results.json"
    if json_path.exists():
        try:
            with open(json_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            scanned = data.get("files_scanned_count", scanned)
            violations = data.get("total_findings", 0)
            return scanned, max(scanned - violations, 0), violations
        except Exception:
            pass

    scanned = 87
    passed = scanned if ret_code == 0 else 0
    failed = scanned - passed
    return scanned, passed, failed


def parse_deployment_audit(ret_code, stdout, stderr):
    # test_m4_adversarial_audit outputs json with audit sections
    try:
        data = json.loads(stdout.strip())
        spring_vars = len(data.get("env_var_audit", {}).get("spring_boot", {}))
        ml_vars = len(data.get("ml_env_var_audit", {}))
        ssl_checks = len(data.get("ssl_protocol_audit", {}))
        rewrites = len(data.get("vercel_rewrite_stress", {}))
        api_checks = len(data.get("api_js_client_audit", {}))
        jvm_checks = len(data.get("jvm_memory_audit", {}))
        total_checks = spring_vars + ml_vars + ssl_checks + rewrites + api_checks + jvm_checks
        failed = 0 if ret_code == 0 else total_checks
        return total_checks, total_checks - failed, failed
    except Exception:
        tests_run = 35
        passed = tests_run if ret_code == 0 else 0
        return tests_run, passed, tests_run - passed


def parse_pdf_compiler(ret_code, stdout, stderr):
    pdf_path = REPO_ROOT / "StayMart_Project_Report.pdf"
    exists = pdf_path.exists() and pdf_path.stat().st_size > 1000000
    tests_run = 1
    passed = 1 if (ret_code == 0 and exists) else 0
    failed = 1 - passed
    return tests_run, passed, failed


def parse_smoke_tests(ret_code, stdout, stderr):
    tests_run = 96
    if ret_code != 0:
        return tests_run, 0, tests_run

    json_path = REPO_ROOT / "scripts" / "smoke_test_results.json"
    if json_path.exists():
        try:
            with open(json_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            total = data.get("total_tests", tests_run)
            passed = data.get("passed_tests", tests_run)
            failed = data.get("failed_tests", 0)
            return total, passed, failed
        except Exception:
            pass

    tests_run = 96
    passed = tests_run if ret_code == 0 else 0
    failed = tests_run - passed
    return tests_run, passed, failed


# =============================================================================
# Dashboard Renderer
# =============================================================================

def render_dashboard(suite_results, total_duration):
    total_run = sum(s.tests_run for s in suite_results)
    total_passed = sum(s.passed for s in suite_results)
    total_failed = sum(s.failed for s in suite_results)
    all_passed = (total_failed == 0 and all(s.return_code == 0 for s in suite_results))

    col_idx = 4
    col_name = 38
    col_run = 11
    col_pass = 8
    col_fail = 8
    col_dur = 14
    col_stat = 8

    sep_line = "+" + "-" * col_idx + "+" + "-" * col_name + "+" + "-" * col_run + "+" + "-" * col_pass + "+" + "-" * col_fail + "+" + "-" * col_dur + "+" + "-" * col_stat + "+"
    double_sep = "=" * (len(sep_line))

    print("\n" + double_sep)
    header_title = "STAYMART MASTER VERIFICATION DASHBOARD (MILESTONE 5)"
    print(header_title.center(len(sep_line)))
    print(double_sep)

    header = f"| {'#':<{col_idx-2}} | {'TEST SUITE':<{col_name-2}} | {'TESTS RUN':<{col_run-2}} | {'PASSED':<{col_pass-2}} | {'FAILED':<{col_fail-2}} | {'DURATION':<{col_dur-2}} | {'STATUS':<{col_stat-2}} |"
    print(header)
    print(sep_line)

    for s in suite_results:
        row = f"| {s.index:<{col_idx-2}} | {s.name:<{col_name-2}} | {s.tests_run:<{col_run-2}} | {s.passed:<{col_pass-2}} | {s.failed:<{col_fail-2}} | {f'{s.duration:.2f}s':<{col_dur-2}} | {s.status:<{col_stat-2}} |"
        print(row)

    print(sep_line)

    overall_status = "PASS" if all_passed else "FAIL"
    passed_suites = sum(1 for s in suite_results if (getattr(s, "status", None) == "PASS" if not isinstance(s, dict) else s.get("status") == "PASS"))
    summary_label = f"TOTAL: {passed_suites}/{len(suite_results)} SUITES PASSED ({total_passed}/{total_run} TESTS, {total_failed} FAILURES)"
    summary_row = f"| {summary_label:<{col_idx + col_name + col_run + col_pass + col_fail - 3}} | {f'{total_duration:.2f}s':<{col_dur-2}} | {overall_status:<{col_stat-2}} |"
    print(summary_row)
    print(double_sep)

    # Save summary json
    summary_file = REPO_ROOT / "scripts" / "master_verification_summary.json"
    summary_data = {
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "overall_verdict": overall_status,
        "total_suites": len(suite_results),
        "suites_passed": sum(1 for s in suite_results if s.status == "PASS"),
        "suites_failed": sum(1 for s in suite_results if s.status == "FAIL"),
        "total_tests_run": total_run,
        "total_tests_passed": total_passed,
        "total_tests_failed": total_failed,
        "total_duration_seconds": round(total_duration, 2),
        "suites": [
            {
                "index": s.index,
                "name": s.name,
                "command": s.command,
                "tests_run": s.tests_run,
                "passed": s.passed,
                "failed": s.failed,
                "duration_seconds": round(s.duration, 2),
                "return_code": s.return_code,
                "status": s.status
            }
            for s in suite_results
        ]
    }
    summary_file.write_text(json.dumps(summary_data, indent=2), encoding="utf-8")
    print(f"\nMaster verification report written to: {summary_file.relative_to(REPO_ROOT)}")

    return all_passed


# =============================================================================
# Main Verification Pipeline
# =============================================================================

def main():
    parser = argparse.ArgumentParser(description="StayMart Unified Master Verification Runner")
    parser.add_argument("--skip-pdf", action="store_true", help="Skip PDF compilation (for fast verification runs)")
    args = parser.parse_args()

    python_bin = sys.executable

    suites = [
        (1, "Spring Boot Backend Tests (JUnit 5)", [python_bin, "scripts/run_backend_tests.py"], parse_backend_tests),
        (2, "Headless Chrome Viewports (320px-1920px)", ["node", "scripts/run_viewport_tests.js"], parse_viewport_tests),
        (3, "Navigation & DOM Link Verification", [python_bin, "scripts/verify_m1_navigation.py"], parse_navigation_tests),
        (4, "AI Artifact Pattern Scanner (87 files)", [python_bin, "scripts/scan_ai_artifacts.py"], parse_ai_artifacts),
        (5, "Cloud Deployment & Manifest Audit", [python_bin, "scripts/test_m4_adversarial_audit.py"], parse_deployment_audit),
        (6, "Academic PDF Report Compiler", [python_bin, "scripts/compile_report_pdf.py"], parse_pdf_compiler),
        (7, "Multi-Tier API Smoke Test Suite", [python_bin, "scripts/run_smoke_tests.py"], parse_smoke_tests),
    ]

    if args.skip_pdf:
        suites = [s for s in suites if s[0] != 6]

    print("=" * 90)
    print("STAYMART UNIFIED MASTER VERIFICATION PIPELINE (MILESTONE 5)")
    print(f"Total Suites to Execute: {len(suites)}")
    print(f"Working Directory:       {REPO_ROOT}")
    print("=" * 90)

    overall_start = time.time()
    results = []

    for idx, name, cmd, parser_fn in suites:
        res = execute_suite(idx, name, cmd, parser_fn)
        results.append(res)
        if res.status != "PASS":
            print(f"\n[ALERT] Suite '{name}' FAILED with exit code {res.return_code}!")
            # Note: We continue running all suites so developer gets the complete report

    total_duration = time.time() - overall_start
    all_passed = render_dashboard(results, total_duration)

    if all_passed:
        print("\nSUCCESS: All automated verification suites passed cleanly (Exit Code 0).\n")
        sys.exit(0)
    else:
        print("\nFAILURE: One or more verification suites failed. Check diagnosis above (Exit Code 1).\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
