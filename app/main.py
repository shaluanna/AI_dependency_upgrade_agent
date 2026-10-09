from fastapi import FastAPI
from pydantic import BaseModel

from app.service import (
    analyze_project_dependencies,
    report_to_dict
)


app = FastAPI(
    title="AI Dependency Upgrade Agent",
    version="1.0.0"
)


class AnalyzeRequest(BaseModel):
    project_path: str
    run_tests: bool = True


@app.get("/")
def root():
    return {
        "message": "AI Dependency Upgrade and Compatibility Agent"
    }


@app.post("/analyze")
def analyze(request: AnalyzeRequest):
    report = analyze_project_dependencies(
        project_path=request.project_path,
        run_project_tests=request.run_tests
    )

    return report_to_dict(report)