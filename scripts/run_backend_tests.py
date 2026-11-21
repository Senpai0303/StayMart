import glob
import os
import subprocess
import sys

print("=== Compiling StayMart Backend Test Suites ===")

m2 = r'C:\Users\divya\.m2\repository'
jars = glob.glob(m2 + '/**/*.jar', recursive=True)
os.makedirs('target/test-classes', exist_ok=True)
cp = ';'.join(jars) + ';target/classes;target/test-classes'

with open('test_compile.args', 'w', encoding='utf-8') as f:
    f.write('-cp\n' + cp + '\n')

test_sources = glob.glob('src/test/java/**/*.java', recursive=True)
print(f"Found {len(test_sources)} test source files:")
for s in test_sources:
    print(f"  - {s}")

cmd_compile = ['javac', '@test_compile.args', '-d', 'target/test-classes'] + test_sources
res_compile = subprocess.run(cmd_compile, capture_output=True, text=True)

if os.path.exists('test_compile.args'):
    os.remove('test_compile.args')

if res_compile.returncode != 0:
    print("Compilation failed:")
    print(res_compile.stderr)
    sys.exit(1)

print("Compilation successful!")
print("=== Running StayMart Backend Tests via JUnit 5 Launcher ===")

with open('test_run.args', 'w', encoding='utf-8') as f:
    f.write('-cp\n' + cp + '\n')

cmd_run = ['java', '@test_run.args', 'com.staymart.TestRunner']
res_run = subprocess.run(cmd_run, capture_output=True, text=True)

if os.path.exists('test_run.args'):
    os.remove('test_run.args')

print(res_run.stdout)
if res_run.stderr:
    print(res_run.stderr)

if res_run.returncode == 0:
    print("SUCCESS: All backend tests passed!")
else:
    print(f"FAILURE: Backend tests exited with code {res_run.returncode}")
    sys.exit(res_run.returncode)
