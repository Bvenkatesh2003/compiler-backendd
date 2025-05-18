# main.py
from fastapi import FastAPI, Request
from pydantic import BaseModel
import docker
import uuid
import os

app = FastAPI()
client = docker.from_env()

class CodeRequest(BaseModel):
    code: str

@app.post("/run")
async def run_code(req: CodeRequest):
    filename = f"/tmp/{uuid.uuid4().hex}.py"
    with open(filename, "w") as f:
        f.write(req.code)

    try:
        container = client.containers.run(
            image="python:3.10-slim",
            command=f"python {os.path.basename(filename)}",
            volumes={"/tmp": {"bind": "/app", "mode": "ro"}},
            working_dir="/app",
            stdin_open=True,
            stdout=True,
            stderr=True,
            remove=True,
            mem_limit="100m",
            network_disabled=True
        )

        return {"output": container.decode("utf-8")}

    except docker.errors.ContainerError as e:
        return {"output": e.stderr.decode("utf-8") if e.stderr else str(e)}
    finally:
        os.remove(filename)
