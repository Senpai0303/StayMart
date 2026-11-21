import yaml

proposed_yaml = """services:
  # -------------------------------------------------------------
  # Tier 2: Spring Boot Backend REST API
  # -------------------------------------------------------------
  - type: web
    name: staymart-backend
    runtime: docker
    dockerfilePath: ./Dockerfile
    plan: free
    region: singapore
    healthCheckPath: /api/properties
    envVars:
      - key: PORT
        value: 8080
      - key: SPRING_PROFILES_ACTIVE
        value: prod
      - key: JAVA_TOOL_OPTIONS
        value: "-Xmx384m -Xms128m -XX:+UseSerialGC"
      - key: DB_URL
        sync: false
      - key: DB_USERNAME
        sync: false
      - key: DB_PASSWORD
        sync: false
      - key: JWT_SECRET
        generateValue: true
      - key: CORS_ORIGINS
        value: "https://staymart.vercel.app,https://staymart-frontend.vercel.app,http://localhost:5500,http://127.0.0.1:5500"
      - key: ML_BASE_URL
        value: "https://staymart-ml.onrender.com"
      - key: UPLOAD_DIR
        value: /tmp/uploads
      - key: UPLOAD_BASE_URL
        value: "https://staymart-backend.onrender.com"

  # -------------------------------------------------------------
  # Tier 3: Python Flask ML Recommendation Microservice
  # -------------------------------------------------------------
  - type: web
    name: staymart-ml
    runtime: docker
    dockerfilePath: ./ml-service/Dockerfile
    dockerContext: ./ml-service
    plan: free
    region: singapore
    healthCheckPath: /health
    envVars:
      - key: PORT
        value: 5000
      - key: DB_HOST
        sync: false
      - key: DB_PORT
        value: 4000
      - key: DB_USERNAME
        sync: false
      - key: DB_PASSWORD
        sync: false
      - key: DB_NAME
        value: staymart
      - key: DEFAULT_CITY
        value: Dehradun
"""

data = yaml.safe_load(proposed_yaml)
print(f"Services parsed: {len(data['services'])}")
for service in data['services']:
    print(f"Service: {service['name']}")
    for env in service['envVars']:
        print(f"  {env['key']} -> {env.get('value', 'sync:' + str(env.get('sync', env.get('generateValue'))))}")

backend_vars = {env['key']: env.get('value') for env in data['services'][0]['envVars']}
assert backend_vars['UPLOAD_BASE_URL'] == "https://staymart-backend.onrender.com"
assert backend_vars['ML_BASE_URL'] == "https://staymart-ml.onrender.com"
print("All assertions passed successfully!")
