FROM python:3.11-slim

RUN useradd -m runner
USER runner
WORKDIR /home/runner

COPY run_code.py .

ENTRYPOINT ["python", "run_code.py"]
