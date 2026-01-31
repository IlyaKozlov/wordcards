import logging
import os
import shutil
import tempfile
import zipfile
from pathlib import Path
from typing import Dict

from fastapi import BackgroundTasks, UploadFile, File, HTTPException
from fastapi.routing import APIRouter
from starlette.responses import FileResponse

db_route = APIRouter()
logger = logging.getLogger(__name__)
path = Path(__file__).parent.parent.parent.parent / "db"


@db_route.get("")
def get_db(background_task: BackgroundTasks) -> FileResponse:
    tmpdir_obj = tempfile.TemporaryDirectory()
    background_task.add_task(tmpdir_obj.cleanup)
    tmpdir = Path(tmpdir_obj.name)
    zip_path = tmpdir / "db.zip"
    # Create a zip archive containing the entire `path` directory (including empty dirs)
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for dirpath, _, filenames in os.walk(path):
            dirpath = Path(dirpath)
            # Add directory entry (ensures empty directories are preserved)
            rel_dir = dirpath.relative_to(path.parent).as_posix() + "/"
            zf.writestr(rel_dir, b"")
            for file_name in filenames:
                file_path = dirpath / file_name
                archive_name = file_path.relative_to(path.parent).as_posix()
                zf.write(str(file_path), archive_name)
    # Read the created zip file into memory and return as response content
    return FileResponse(zip_path)


@db_route.post("")
def apply_db(
    upload_file: UploadFile = File(...), background_task: BackgroundTasks = None
) -> Dict[str, str]:

    try:
        # Open uploaded file as a zip archive
        with zipfile.ZipFile(upload_file.file) as zf:
            for member in zf.infolist():
                member_name = member.filename
                # Skip empty names
                if not member_name:
                    continue
                # Use POSIX-style path parts from the archive entry
                member_path = Path(member_name)
                parts = member_path.parts
                # If the archive root folder equals our `path` folder name, strip it
                if parts and parts[0] == path.name:
                    rel_path = Path(*parts[1:]) if len(parts) > 1 else Path()
                else:
                    rel_path = Path(*parts)
                # If the resulting relative path is empty (e.g., archive only had top-level folder), skip
                if str(rel_path) == "":
                    continue
                dest_path = (path / rel_path).resolve()
                # Prevent zip-slip: ensure destination is inside the intended `path`
                if not str(dest_path).startswith(str(path.resolve())):
                    raise HTTPException(
                        status_code=400,
                        detail=f"Illegal path in archive: {member_name}",
                    )
                # Create directories for entries that are directories or for file parents
                if member_name.endswith("/"):
                    dest_path.mkdir(parents=True, exist_ok=True)
                    continue
                dest_path.parent.mkdir(parents=True, exist_ok=True)
                # Extract file content
                with zf.open(member) as src, open(dest_path, "wb") as dst:
                    shutil.copyfileobj(src, dst)
                return {"detail": "archive extracted"}
    except zipfile.BadZipFile:
        raise HTTPException(
            status_code=400, detail="Uploaded file is not a valid zip archive"
        )
    finally:
        try:
            upload_file.file.close()
        except Exception:
            pass
