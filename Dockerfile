FROM python:3.11-slim

# Install Java (required for PlantUML) and other dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    openjdk-21-jre-headless \
    wget \
    ca-certificates \
    graphviz \
    && rm -rf /var/lib/apt/lists/*

# Download PlantUML
ENV PLANTUML_VERSION=1.2024.7
ENV PLANTUML_JAR=/opt/plantuml.jar
RUN wget --no-check-certificate -O ${PLANTUML_JAR} \
    https://github.com/plantuml/plantuml/releases/download/v${PLANTUML_VERSION}/plantuml-${PLANTUML_VERSION}.jar

# Install Python dependencies
RUN pip install --no-cache-dir --trusted-host pypi.org --trusted-host files.pythonhosted.org requests

# Create working directories
RUN mkdir -p /input /output

# Copy application files
COPY puml_processor.py /app/
COPY server.py /app/
COPY azure_wiki_publisher.py /app/
COPY entrypoint.sh /app/

# Make scripts executable
RUN chmod +x /app/*.py /app/entrypoint.sh

WORKDIR /app

# Set environment variables
ENV INPUT_DIR=/input
ENV OUTPUT_DIR=/output
ENV PORT=8080
ENV SERVE_DIR=/output

# Expose port for web server
EXPOSE 8080

# Use entrypoint script
ENTRYPOINT ["/app/entrypoint.sh"]
CMD ["serve"]
