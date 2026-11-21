# Multi-stage Docker build for StayMart Spring Boot backend
# Stage 1: Build stage with Maven and Eclipse Temurin JDK 17
FROM maven:3.9.6-eclipse-temurin-17 AS build
WORKDIR /app

# Cache Maven dependencies layer
COPY pom.xml .
RUN mvn dependency:go-offline -B

# Copy application source code and compile production JAR artifact
COPY src ./src
RUN mvn clean package -DskipTests

# Stage 2: Minimal runtime image with Eclipse Temurin JRE 17 Jammy
FROM eclipse-temurin:17-jre-jammy
WORKDIR /app

# Copy compiled JAR from build stage
COPY --from=build /app/target/staymart-0.0.1-SNAPSHOT.jar app.jar

# Memory guardrails for 512MB RAM free cloud tiers (Render / Koyeb)
# -Xmx384m caps heap to leave headroom for metaspace and OS threads
# -XX:+UseSerialGC minimizes GC thread memory overhead
ENV JAVA_TOOL_OPTIONS="-Xmx384m -Xms128m -XX:+UseSerialGC"
ENV PORT=8080

EXPOSE 8080

# Handle Render / Koyeb dynamic $PORT environment variable binding
ENTRYPOINT ["sh", "-c", "java $JAVA_TOOL_OPTIONS -Dserver.port=${PORT:-8080} -jar app.jar"]
