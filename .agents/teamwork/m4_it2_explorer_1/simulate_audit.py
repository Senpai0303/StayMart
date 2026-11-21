import re

with open("src/main/resources/application.yml", "r", encoding="utf-8") as f:
    app_yml = f.read()

spring_env_vars = set(re.findall(r"\$\{([A-Z0-9_]+)", app_yml))

# Proposed render.yaml content
with open(".agents/teamwork/m4_it2_explorer_1/validate_blueprint.py", "r") as f:
    lines = f.read()
import yaml
proposed_yaml = re.search(r'proposed_yaml = """(.*?)"""', lines, re.DOTALL).group(1)

services = proposed_yaml.split("- type: web")
render_backend_vars = set(re.findall(r"key:\s*([A-Za-z0-9_]+)", services[1]))

print("Spring Boot environment variables in application.yml:")
for v in sorted(spring_env_vars):
    in_p = v in render_backend_vars
    print(f"  {v}: in proposed render.yaml = {in_p}")

assert "UPLOAD_BASE_URL" in render_backend_vars
assert "ML_BASE_URL" in render_backend_vars
print("Audit check for render.yaml: PASS")
