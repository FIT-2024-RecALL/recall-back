from fastapi import APIRouter, HTTPException, UploadFile, File
from fastapi.responses import StreamingResponse, Response
from urllib.parse import quote

from app import crud
from app.helpers import DBConnection, UserID
from app.schemas import FileUploadedScheme


router = APIRouter(
    prefix='/storage',
    tags=['storage']
)


@router.get('/{user_id}/{filename}', response_class=StreamingResponse)
def get_file(user_id: int, filename: str):
    
    full_path = f'{user_id}/{filename}'
    if not crud.is_file_exists(full_path):
        raise HTTPException(404, "File not found")
    try:
        return StreamingResponse(
            crud.get_file_stream(full_path),
            media_type="application/octet-stream",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )
    except ValueError as e:
        raise HTTPException(404, f"File not found: {str(e)}")


@router.get('/', response_model=list[FileUploadedScheme])
async def list_files(conn: DBConnection, user_id: UserID):
    try:
        await crud.check_user_id(conn, user_id)
    except ValueError as e:
        raise HTTPException(401, str(e))
    return [
        FileUploadedScheme(url=f"/storage/{quote(obj.object_name)}")
        for obj in crud.get_files_list(user_id)
    ]


@router.post('/', response_model=FileUploadedScheme)
async def add_file(conn: DBConnection, user_id: UserID, file: UploadFile = File(...)):
    try:
        await crud.check_user_id(conn, user_id)
    except ValueError as e:
        raise HTTPException(401, str(e))

    try:
        obj = crud.upload_file(user_id, file)
        return FileUploadedScheme(
            url=f"/storage/{quote(obj.object_name)}"
        )
    except ValueError as e:
        raise HTTPException(409, f"Failed to upload file: {str(e)}")


@router.delete('/{filename}', status_code=200)
async def delete_file(conn: DBConnection, user_id: UserID, filename: str):
    try:
        await crud.check_user_id(conn, user_id)
    except ValueError as e:
        raise HTTPException(401, str(e))

    full_path = f'{user_id}/{filename}'
    if not crud.is_file_exists(full_path):
        raise HTTPException(404, "File not found")
    try:
        crud.delete_file(full_path)
        return Response(status_code=200)
    except ValueError as e:
        raise HTTPException(404, f"Failed to delete file: {str(e)}")
