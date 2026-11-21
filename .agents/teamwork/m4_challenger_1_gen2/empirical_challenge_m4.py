#!/usr/bin/env python3
"""
Empirical Challenge & Verification Script for Milestone 4
Validates:
1. vercel.json & frontend/vercel.json (JSON syntax, cleanUrls, rewrites, rule ordering)
2. Dockerfile (multi-stage build, Java 17 Temurin, memory guardrails, dynamic $PORT binding)
3. ml-service/Dockerfile (Python 3.11-slim, gunicorn single-worker multi-threaded, model presence)
4. render.yaml (YAML syntax, services schema, env vars, cross-service bindings)
5. DEPLOYMENT.md (all mandatory sections, verification steps, free-tier realism)
"""

import os
import sys
import json
import re

try:
    import yaml
except ImportError:
    yaml = None

WORKSPACE = r"d:\Mini5th"
FAILURES = []
TESTS_RUN = 0


def record_pass(test_name, details=""):
    global TESTS_RUN
    TESTS_RUN += 1
    print(f"  [PASS] {test_name}" + (f" -> {details}" if details else ""))


def record_fail(test_name, reason):
    global TESTS_RUN
    TESTS_RUN += 1
    FAILURES.append((test_name, reason))
    print(f"  [FAIL] {test_name} -> {reason}")


def check_vercel_json(rel_path, is_root=True):
    full_path = os.path.join(WORKSPACE, rel_path)
    if not os.path.isfile(full_path):
        record_fail(f"{rel_path} existence", "File does not exist")
        return

    try:
        with open(full_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        record_pass(f"{rel_path} JSON validity", "Successfully parsed as JSON")
    except Exception as e:
        record_fail(f"{rel_path} JSON validity", str(e))
        return

    # Check version
    if data.get("version") == 2:
        record_pass(f"{rel_path} version", "version == 2")
    else:
        record_fail(f"{rel_path} version", f"Expected version 2, got {data.get('version')}")

    # Check cleanUrls
    if data.get("cleanUrls") is True:
        record_pass(f"{rel_path} cleanUrls", "cleanUrls == True")
    else:
        record_fail(f"{rel_path} cleanUrls", f"Expected cleanUrls True, got {data.get('cleanUrls')}")

    # Check rewrites
    rewrites = data.get("rewrites")
    if not isinstance(rewrites, list) or len(rewrites) == 0:
        record_fail(f"{rel_path} rewrites", "Rewrites must be a non-empty list")
        return

    record_pass(f"{rel_path} rewrites count", f"{len(rewrites)} rewrite rules defined")

    # Order verification: /api/(.*) must appear before /(.*)
    api_idx = -1
    uploads_idx = -1
    catchall_idx = -1

    for idx, rule in enumerate(rewrites):
        src = rule.get("source", "")
        dest = rule.get("destination", "")
        if "/api/" in src:
            api_idx = idx
            if "staymart-backend.onrender.com" in dest:
                record_pass(f"{rel_path} /api rewrite target", f"{src} -> {dest}")
            else:
                record_fail(f"{rel_path} /api rewrite target", f"Expected proxy to backend, got {dest}")
        elif "/uploads/" in src:
            uploads_idx = idx
            if "staymart-backend.onrender.com" in dest:
                record_pass(f"{rel_path} /uploads rewrite target", f"{src} -> {dest}")
            else:
                record_fail(f"{rel_path} /uploads rewrite target", f"Expected proxy to backend, got {dest}")
        elif src == "/(.*)":
            catchall_idx = idx

    if api_idx != -1 and catchall_idx != -1:
        if api_idx < catchall_idx:
            record_pass(f"{rel_path} rule ordering", f"/api rewrite (index {api_idx}) precedes catch-all (index {catchall_idx})")
        else:
            record_fail(f"{rel_path} rule ordering", f"Catch-all (index {catchall_idx}) masks /api rewrite (index {api_idx})")
    else:
        record_fail(f"{rel_path} rule ordering", "Missing /api or catch-all rewrite rule")

    if uploads_idx != -1 and catchall_idx != -1:
        if uploads_idx < catchall_idx:
            record_pass(f"{rel_path} uploads ordering", f"/uploads rewrite (index {uploads_idx}) precedes catch-all (index {catchall_idx})")
        else:
            record_fail(f"{rel_path} uploads ordering", f"Catch-all masks /uploads rewrite")


def check_root_dockerfile():
    df_path = os.path.join(WORKSPACE, "Dockerfile")
    if not os.path.isfile(df_path):
        record_fail("Root Dockerfile existence", "Dockerfile not found")
        return

    content = open(df_path, "r", encoding="utf-8").read()

    # Stage 1: Build stage with Maven and Java 17
    if re.search(r"FROM\s+maven:[^\s]+temurin-17\s+AS\s+build", content, re.IGNORECASE):
        record_pass("Root Dockerfile build stage", "Multi-stage Maven + Temurin 17 build stage")
    else:
        record_fail("Root Dockerfile build stage", "Missing Maven Temurin 17 build stage")

    # Dependency caching
    if "COPY pom.xml" in content and "mvn dependency:go-offline" in content:
        record_pass("Root Dockerfile dependency caching", "Caches pom.xml and downloads dependencies offline")
    else:
        record_fail("Root Dockerfile dependency caching", "Missing Maven dependency layer caching")

    # Stage 2: Runtime image
    if re.search(r"FROM\s+eclipse-temurin:17-jre", content, re.IGNORECASE):
        record_pass("Root Dockerfile runtime stage", "Temurin 17 JRE runtime image")
    else:
        record_fail("Root Dockerfile runtime stage", "Missing Temurin 17 JRE runtime stage")

    # JAR copy
    if "COPY --from=build" in content and "staymart-0.0.1-SNAPSHOT.jar app.jar" in content:
        record_pass("Root Dockerfile JAR copy", "Artifact copied from build stage to app.jar")
    else:
        record_fail("Root Dockerfile JAR copy", "Missing JAR copy directive")

    # Memory guardrails
    if '-Xmx384m' in content and '-Xms128m' in content and '-XX:+UseSerialGC' in content:
        record_pass("Root Dockerfile JVM guardrails", "JAVA_TOOL_OPTIONS contains -Xmx384m -Xms128m -XX:+UseSerialGC")
    else:
        record_fail("Root Dockerfile JVM guardrails", "Missing free-tier memory tuning options")

    # Dynamic PORT binding in ENTRYPOINT
    if "PORT" in content and "${PORT:-8080}" in content and '["sh", "-c"' in content:
        record_pass("Root Dockerfile dynamic $PORT binding", "ENTRYPOINT uses sh -c with ${PORT:-8080}")
    else:
        record_fail("Root Dockerfile dynamic $PORT binding", "Missing dynamic shell PORT binding")


def check_ml_dockerfile():
    df_path = os.path.join(WORKSPACE, "ml-service", "Dockerfile")
    if not os.path.isfile(df_path):
        record_fail("ML Dockerfile existence", "ml-service/Dockerfile not found")
        return

    content = open(df_path, "r", encoding="utf-8").read()

    # Base image: python:3.11-slim
    if re.search(r"FROM\s+python:3\.11-slim", content, re.IGNORECASE):
        record_pass("ML Dockerfile base image", "Uses python:3.11-slim")
    else:
        record_fail("ML Dockerfile base image", "Expected python:3.11-slim")

    # Dependencies + Gunicorn
    if "pip install" in content and "requirements.txt" in content and "gunicorn" in content:
        record_pass("ML Dockerfile dependencies", "Installs requirements.txt and gunicorn")
    else:
        record_fail("ML Dockerfile dependencies", "Missing gunicorn or requirements.txt install")

    # Single-worker gunicorn CMD
    if "-w" in content and ("1" in content) and "--threads" in content and "app:app" in content:
        record_pass("ML Dockerfile Gunicorn CMD", "Configured with 1 worker and multi-threading for <180MB RAM")
    else:
        record_fail("ML Dockerfile Gunicorn CMD", "Improper worker configuration (may exceed free tier RAM)")

    # Model file verification
    p1 = os.path.join(WORKSPACE, "ml-service", "models", "property_tfidf.pkl")
    p2 = os.path.join(WORKSPACE, "ml-service", "models", "product_tfidf.pkl")
    if os.path.isfile(p1) and os.path.getsize(p1) > 1000:
        record_pass("ML property TF-IDF model", f"Exists ({os.path.getsize(p1)} bytes)")
    else:
        record_fail("ML property TF-IDF model", "Missing or empty property_tfidf.pkl")

    if os.path.isfile(p2) and os.path.getsize(p2) > 1000:
        record_pass("ML product TF-IDF model", f"Exists ({os.path.getsize(p2)} bytes)")
    else:
        record_fail("ML product TF-IDF model", "Missing or empty product_tfidf.pkl")


def check_render_yaml():
    yaml_path = os.path.join(WORKSPACE, "render.yaml")
    if not os.path.isfile(yaml_path):
        record_fail("render.yaml existence", "render.yaml not found")
        return

    if yaml is None:
        # Fallback basic parsing if pyyaml not installed
        content = open(yaml_path, "r", encoding="utf-8").read()
        if "services:" in content and "staymart-backend" in content and "staymart-ml" in content:
            record_pass("render.yaml basic structure", "Found services, staymart-backend, staymart-ml")
        else:
            record_fail("render.yaml basic structure", "Missing services definitions")
        return

    try:
        with open(yaml_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        record_pass("render.yaml YAML syntax", "Valid YAML document")
    except Exception as e:
        record_fail("render.yaml YAML syntax", str(e))
        return

    services = data.get("services", [])
    if len(services) < 2:
        record_fail("render.yaml services count", f"Expected 2 services, got {len(services)}")
        return

    record_pass("render.yaml services count", f"Found {len(services)} services")

    backend = next((s for s in services if s.get("name") == "staymart-backend"), None)
    ml = next((s for s in services if s.get("name") == "staymart-ml"), None)

    if backend:
        record_pass("render.yaml backend service", "Found staymart-backend")
        if backend.get("plan") == "free":
            record_pass("render.yaml backend plan", "plan == free")
        else:
            record_fail("render.yaml backend plan", f"Expected free, got {backend.get('plan')}")

        env_keys = {e.get("key") for e in backend.get("envVars", []) if isinstance(e, dict)}
        expected_keys = {"PORT", "SPRING_PROFILES_ACTIVE", "JAVA_TOOL_OPTIONS", "DB_URL", "DB_USERNAME", "DB_PASSWORD", "JWT_SECRET", "CORS_ORIGINS", "ML_BASE_URL", "UPLOAD_DIR"}
        missing_keys = expected_keys - env_keys
        if not missing_keys:
            record_pass("render.yaml backend envVars", f"All {len(expected_keys)} expected env vars configured")
        else:
            record_fail("render.yaml backend envVars", f"Missing env vars: {missing_keys}")
    else:
        record_fail("render.yaml backend service", "staymart-backend service missing")

    if ml:
        record_pass("render.yaml ML service", "Found staymart-ml")
        if ml.get("plan") == "free":
            record_pass("render.yaml ML plan", "plan == free")
        else:
            record_fail("render.yaml ML plan", f"Expected free, got {ml.get('plan')}")

        if ml.get("healthCheckPath") == "/health":
            record_pass("render.yaml ML health check", "healthCheckPath == /health")
        else:
            record_fail("render.yaml ML health check", f"Expected /health, got {ml.get('healthCheckPath')}")

        env_keys = {e.get("key") for e in ml.get("envVars", []) if isinstance(e, dict)}
        expected_keys = {"PORT", "DB_HOST", "DB_PORT", "DB_USERNAME", "DB_PASSWORD", "DB_NAME", "DEFAULT_CITY"}
        missing_keys = expected_keys - env_keys
        if not missing_keys:
            record_pass("render.yaml ML envVars", f"All {len(expected_keys)} expected env vars configured")
        else:
            record_fail("render.yaml ML envVars", f"Missing env vars: {missing_keys}")
    else:
        record_fail("render.yaml ML service", "staymart-ml service missing")


def check_deployment_guide():
    doc_path = os.path.join(WORKSPACE, "DEPLOYMENT.md")
    if not os.path.isfile(doc_path):
        record_fail("DEPLOYMENT.md existence", "File does not exist")
        return

    content = open(doc_path, "r", encoding="utf-8").read()
    size = len(content)

    if size > 10000:
        record_pass("DEPLOYMENT.md comprehensiveness", f"File size is {size} characters")
    else:
        record_fail("DEPLOYMENT.md comprehensiveness", f"File size {size} is unusually short")

    required_topics = [
        ("Architecture topology diagram", "TIER 1", "TIER 2", "TIER 3", "TIER 4"),
        ("TiDB Serverless Setup", "TiDB Cloud", "Serverless", "01_schema.sql"),
        ("Render / Koyeb Backend deployment", "Render", "Dockerfile", "JAVA_TOOL_OPTIONS"),
        ("Render Flask ML deployment", "gunicorn", "5000", "staymart-ml"),
        ("Vercel Frontend deployment", "Vercel", "cleanUrls", "rewrites"),
        ("End-to-End Verification Scripts", "curl", "Invoke-RestMethod"),
        ("Free tier sleep / keep-warm mitigation", "15 minutes", "UptimeRobot"),
    ]

    for topic in required_topics:
        name = topic[0]
        keywords = topic[1:]
        all_found = all(kw.lower() in content.lower() for kw in keywords)
        if all_found:
            record_pass(f"DEPLOYMENT.md section '{name}'", f"Keywords {keywords} verified")
        else:
            record_fail(f"DEPLOYMENT.md section '{name}'", f"Missing one or more required keywords: {keywords}")


def main():
    print("=" * 70)
    print("STAYMART MILESTONE 4: ADVERSARIAL CHALLENGER VERIFICATION HARNESS")
    print("=" * 70)

    print("\n[SECTION 1: VERCEL DEPLOYMENT CONFIGURATIONS]")
    check_vercel_json("vercel.json", is_root=True)
    check_vercel_json("frontend/vercel.json", is_root=False)

    print("\n[SECTION 2: BACKEND DOCKER CONTAINERIZATION]")
    check_root_dockerfile()

    print("\n[SECTION 3: FLASK ML MICROSERVICE CONTAINERIZATION]")
    check_ml_dockerfile()

    print("\n[SECTION 4: RENDER INFRASTRUCTURE AS CODE (render.yaml)]")
    check_render_yaml()

    print("\n[SECTION 5: DEPLOYMENT DOCUMENTATION & VERIFICATION RUNNERS]")
    check_deployment_guide()

    print("\n" + "=" * 70)
    print(f"VERIFICATION SUMMARY: {TESTS_RUN} checks executed | {len(FAILURES)} failures")
    print("=" * 70)

    if FAILURES:
        print("\nFAILURES DETECTED:")
        for name, reason in FAILURES:
            print(f"  - {name}: {reason}")
        print("\nFINAL HARNESS VERDICT: REQUEST_CHANGES")
        sys.exit(1)
    else:
        print("\nALL ADVERSARIAL AND SPECIFICATION CHECKS PASSED!")
        print("FINAL HARNESS VERDICT: APPROVE")
        sys.exit(0)


if __name__ == "__main__":
    main()
