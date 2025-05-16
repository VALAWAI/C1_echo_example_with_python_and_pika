FROM python:3-slim

# Configurations used in the 'MessageService'
ENV RABBITMQ_HOST=mov-mq
ENV RABBITMQ_PORT=5672.
ENV RABBITMQ_USERNAME=mov.
ENV RABBITMQ_PASSWORD=password
ENV RABBITMQ_MAX_RETRIES=100
ENV RABBITMQ_RETRY_SLEEP=3
	
# Configurations used in the  '__main__'
ENV LOG_DIR=logs
ENV LOG_CONSOLE_LEVEL=DEBUG
ENV LOG_FILE_LEVEL=DEBUG
ENV LOG_FILE_MAX_BYTES=1000000
ENV LOG_FILE_BACKUP_COUNT=5
ENV LOG_FILE_NAME=log_messages.txt

# Configurations used in the 'MOVService'
ENV COMPONET_ID_FILE_NAME=component_id.json

WORKDIR /app

# Copy VALAWAY component files
COPY *.md .
COPY LICENSE .
COPY asyncapi.yaml .

# Copy code and install dependencies
COPY pyproject.toml .
COPY src/ src/
RUN pip install -e .

# Check the component is registered
HEALTHCHECK CMD test -s /app/{$LOG_DIR:-logs}/{$COMPONET_ID_FILE_NAME:-component_id.json}

# Start the component
CMD ["python", "src/c1_echo_example_with_python_and_pika"] 
