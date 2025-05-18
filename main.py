from fastapi import FastAPI
from pydantic import BaseModel
import subprocess
import uuid
import os

app = FastAPI()

class CodeRequest(BaseModel):
    code: str

@app.post("/run")
def run_code(request: CodeRequest):
    temp_filename = f"/tmp/code_{uuid.uuid4().hex}.py"
    with open(temp_filename, "w") as f:
        f.write(request.code)

    try:
        result = subprocess.run(
            [
                "docker", "run", "--rm",
                "-i", "-v", f"{temp_filename}:/code.py",
                "python-runner-image"
            ],
            input=open(temp_filename, "rb").read(),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=5
        )
        os.remove(temp_filename)
        return {
            "stdout": result.stdout.decode(),
            "stderr": result.stderr.decode()
        }
    except subprocess.TimeoutExpired:
        return {"error": "Execution timed out."}
