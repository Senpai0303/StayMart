#!/usr/bin/env python3
"""
Adversarial Environment, Cross-Tier Interconnect & Network Protocol Audit
Milestone 4 Challenger 2 (Empirical Verification Harness)
"""

import os
import re
import json
import urllib.parse

def run_audit():
    results = {
        "env_var_audit": {},
        "ml_env_var_audit": {},
        "ssl_protocol_audit": {},
        "vercel_rewrite_stress": {},
        "api_js_client_audit": {},
        "jvm_memory_audit": {}
    }

    # -------------------------------------------------------------
    # 1. Environment Variable Integrity Audit
    # -------------------------------------------------------------
    app_yml_path = os.path.join("src", "main", "resources", "application.yml")
    render_yaml_path = "render.yaml"
    deployment_md_path = "DEPLOYMENT.md"

    with open(app_yml_path, "r", encoding="utf-8") as f:
        app_yml_content = f.read()

    # Find all ${VAR_NAME:...} or ${VAR_NAME} in application.yml
    spring_env_vars = set(re.findall(r"\$\{([A-Z0-9_]+)", app_yml_content))

    with open(render_yaml_path, "r", encoding="utf-8") as f:
        render_yaml_content = f.read()

    services = render_yaml_content.split("- type: web")
    render_backend_vars = set(re.findall(r"key:\s*([A-Za-z0-9_]+)", services[1]))
    render_ml_vars = set(re.findall(r"key:\s*([A-Za-z0-9_]+)", services[2]))

    with open(deployment_md_path, "r", encoding="utf-8") as f:
        deployment_content = f.read()

    # Check Spring Boot properties against render.yaml and DEPLOYMENT.md
    spring_check = {}
    for var in sorted(spring_env_vars):
        in_render = var in render_backend_vars
        in_docs = f"`{var}`" in deployment_content or var in deployment_content
        spring_check[var] = {
            "in_application_yml": True,
            "in_render_yaml": in_render,
            "in_deployment_md": in_docs
        }
    results["env_var_audit"]["spring_boot"] = spring_check

    # Check ML Service environment variables in config.py / app.py
    with open(os.path.join("ml-service", "config.py"), "r", encoding="utf-8") as f:
        ml_config_content = f.read()

    ml_env_vars = set(re.findall(r"os\.getenv\(['\"]([A-Za-z0-9_]+)['\"]", ml_config_content))
    ml_check = {}
    for var in sorted(ml_env_vars):
        in_render = var in render_ml_vars
        in_docs = f"`{var}`" in deployment_content
        ml_check[var] = {
            "in_ml_config": True,
            "in_render_yaml": in_render,
            "in_deployment_md": in_docs
        }
    results["ml_env_var_audit"] = ml_check

    # -------------------------------------------------------------
    # 2. SSL & Database Protocol Verification
    # -------------------------------------------------------------
    tidb_ssl_docs = {
        "useSSL_specified": "useSSL=true" in deployment_content,
        "sslMode_specified": "sslMode=VERIFY_IDENTITY" in deployment_content,
        "allowPublicKeyRetrieval": "allowPublicKeyRetrieval=true" in deployment_content,
        "mysql_cli_ssl_mode": "--ssl-mode=VERIFY_IDENTITY" in deployment_content,
        "tls_explanation_present": "SSL / TLS Encryption Handshake" in deployment_content
    }
    results["ssl_protocol_audit"] = tidb_ssl_docs

    # -------------------------------------------------------------
    # 3. Vercel Rewrite Rules & Regex Preservation Stress
    # -------------------------------------------------------------
    with open("vercel.json", "r", encoding="utf-8") as f:
        vercel_root = json.load(f)

    test_urls = [
        "/api/properties",
        "/api/properties/14",
        "/api/properties/14/rooms",
        "/api/products?categoryId=2&locationId=1&status=AVAILABLE",
        "/api/recommendations/properties/trending?city=Dehradun&limit=8",
        "/api/locations/cities",
        "/api/files/test-uuid.jpg",
        "/uploads/test-image.png",
        "/api",
        "/search-properties.html?city=Dehradun",
        "/css/global.css",
        "/index.html"
    ]

    def simulate_vercel_rewrites(rules, path_with_query):
        url_parts = urllib.parse.urlsplit(path_with_query)
        path = url_parts.path
        query = url_parts.query

        for rule in rules.get("rewrites", []):
            pattern = "^" + rule["source"] + "$"
            match = re.match(pattern, path)
            if match:
                dest = rule["destination"]
                for i, group in enumerate(match.groups(), 1):
                    dest = dest.replace(f"${i}", group)
                if query:
                    dest = dest + ("&" if "?" in dest else "?") + query
                return {"matched_source": rule["source"], "resolved_destination": dest}
        return {"matched_source": None, "resolved_destination": path_with_query}

    rewrite_results = {}
    for url in test_urls:
        res = simulate_vercel_rewrites(vercel_root, url)
        rewrite_results[url] = res

    results["vercel_rewrite_stress"] = rewrite_results

    # -------------------------------------------------------------
    # 4. Frontend api.js BASE_URL Fallback Audit
    # -------------------------------------------------------------
    with open(os.path.join("frontend", "js", "api.js"), "r", encoding="utf-8") as f:
        api_js_content = f.read()

    api_js_audit = {
        "has_isLocal_detection": "window.location.hostname === 'localhost'" in api_js_content,
        "has_window_override": "window.STAYMART_API_URL" in api_js_content,
        "has_localStorage_override": "localStorage.getItem('STAYMART_API_URL')" in api_js_content,
        "hardcoded_fallback": re.search(r":\s*\((.*?)\);", api_js_content, re.DOTALL).group(1) if re.search(r":\s*\((.*?)\);", api_js_content, re.DOTALL) else None
    }
    results["api_js_client_audit"] = api_js_audit

    # -------------------------------------------------------------
    # 5. JVM Memory Guardrails Audit
    # -------------------------------------------------------------
    with open("Dockerfile", "r", encoding="utf-8") as f:
        dockerfile_content = f.read()

    jvm_audit = {
        "has_Xmx384m": "-Xmx384m" in dockerfile_content,
        "has_Xms128m": "-Xms128m" in dockerfile_content,
        "has_UseSerialGC": "-XX:+UseSerialGC" in dockerfile_content,
        "has_dynamic_PORT_sh_c": "sh -c" in dockerfile_content and "PORT:-8080" in dockerfile_content
    }
    results["jvm_memory_audit"] = jvm_audit

    print(json.dumps(results, indent=2))
    return results

if __name__ == "__main__":
    run_audit()
