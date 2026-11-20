"""
Report generation API endpoints
"""
from fastapi import APIRouter, Query, BackgroundTasks
from fastapi.responses import FileResponse
from typing import Optional
import uuid
from datetime import datetime

router = APIRouter(prefix="/reports", tags=["Reports"])

# In-memory task store (replace with DB in production)
_tasks = {}


@router.post("/generate")
async def generate_report(
    background_tasks: BackgroundTasks,
    data: dict,
):
    """Create a report generation task"""
    task_id = f"task-{uuid.uuid4().hex[:8]}"
    report_type = data.get("report_type", "comprehensive")
    start_date = data.get("start_date")
    end_date = data.get("end_date")
    include_charts = data.get("include_charts", True)
    include_tables = data.get("include_tables", True)

    _tasks[task_id] = {
        "task_id": task_id,
        "status": "pending",
        "progress": 0,
        "report_type": report_type,
        "start_date": start_date,
        "end_date": end_date,
        "created_at": datetime.utcnow().isoformat(),
    }

    # TODO: Actually trigger Celery task for report generation

    return {
        "task_id": task_id,
        "status": "pending",
        "message": f"Report generation started for {report_type}"
    }


@router.get("/status/{task_id}")
async def get_report_status(task_id: str):
    """Get report generation task status"""
    task = _tasks.get(task_id)
    if not task:
        return {"error": "Task not found", "task_id": task_id}

    # Simulate progress for demo
    if task["status"] == "pending":
        task["status"] = "processing"
        task["progress"] = 50
    elif task["status"] == "processing" and task["progress"] < 100:
        task["progress"] = min(100, task["progress"] + 30)

    if task["progress"] >= 100 and task["status"] != "completed":
        task["status"] = "completed"
        task["download_url"] = f"/api/v1/reports/download/{task_id}"

    return task


@router.get("/download/{task_id}")
async def download_report(task_id: str):
    """Download generated report"""
    task = _tasks.get(task_id)
    if not task or task["status"] != "completed":
        return {"error": "Report not ready or not found"}

    # TODO: Return actual Excel file
    return {"message": f"Download URL for report {task_id}", "task": task}


@router.get("/list")
async def list_reports(
    report_type: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
):
    """List all report tasks"""
    result = list(_tasks.values())
    if report_type:
        result = [t for t in result if t.get("report_type") == report_type]
    if status:
        result = [t for t in result if t.get("status") == status]
    return {"reports": result, "total": len(result)}
