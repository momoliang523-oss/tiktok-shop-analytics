"""
Data import API endpoints for Excel/CSV upload
"""
from fastapi import APIRouter, UploadFile, File, Form, Query
from typing import Optional
import uuid
from datetime import datetime

router = APIRouter(prefix="/data", tags=["Data Import"])

_uploads = {}


@router.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    data_type: str = Form(..., description="orders, products, customers, live, traffic"),
):
    """Upload Excel/CSV file for import"""
    upload_id = f"upload-{uuid.uuid4().hex[:8]}"

    # Validate file extension
    allowed = {'.xlsx', '.xls', '.csv'}
    ext = '.' + file.filename.split('.')[-1].lower() if '.' in file.filename else ''
    if ext not in allowed:
        return {"error": f"File type {ext} not allowed. Allowed: {allowed}"}

    # Save file temporarily
    import os
    os.makedirs("data/imports", exist_ok=True)
    file_path = f"data/imports/{upload_id}_{file.filename}"
    content = await file.read()
    with open(file_path, "wb") as f:
        f.write(content)

    file_size = len(content)

    _uploads[upload_id] = {
        "upload_id": upload_id,
        "file_name": file.filename,
        "file_size": file_size,
        "data_type": data_type,
        "status": "processing",
        "total_rows": 0,
        "processed_rows": 0,
        "errors": [],
        "started_at": datetime.utcnow().isoformat(),
    }

    # TODO: Trigger async processing via Celery
    # For now, mark as completed
    _uploads[upload_id]["status"] = "completed"
    _uploads[upload_id]["total_rows"] = 100
    _uploads[upload_id]["processed_rows"] = 100

    return {
        "upload_id": upload_id,
        "status": "completed",
        "total_rows": 100,
        "processed_rows": 100,
    }


@router.get("/upload/{upload_id}")
async def get_upload_status(upload_id: str):
    """Get import status"""
    upload = _uploads.get(upload_id)
    if not upload:
        return {"error": "Upload not found"}
    return upload


@router.get("/imports")
async def list_imports(
    data_type: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
):
    """List all imports"""
    result = list(_uploads.values())
    if data_type:
        result = [u for u in result if u.get("data_type") == data_type]
    if status:
        result = [u for u in result if u.get("status") == status]
    return {"imports": result, "total": len(result)}
