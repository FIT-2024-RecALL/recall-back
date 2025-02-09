from fastapi import APIRouter, HTTPException, UploadFile, File
from fastapi.responses import StreamingResponse, Response
from urllib.parse import quote

from app import repositories
from app.schemas import FileUploadedScheme

from .dependencies import DBConnection, UserID


router = APIRouter(
    prefix='/storage',
    tags=['storage']
)


@router.get('/{user_id}/{filename}', response_class=StreamingResponse)
def get_file(user_id: int, filename: str):
    
    full_path = f'{user_id}/{filename}'
    if not repositories.is_file_exists(full_path):
        raise HTTPException(404, "File not found")
    try:
        return StreamingResponse(
            repositories.get_file_stream(full_path),
            media_type="application/octet-stream",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )
    except ValueError as e:
        raise HTTPException(404, f"File not found: {str(e)}")


@router.get('/', response_model=list[FileUploadedScheme])
async def list_files(conn: DBConnection, user_id: UserID):
    try:
        await repositories.check_user_id(conn, user_id)
    except ValueError as e:
        raise HTTPException(401, str(e))
    return [
        FileUploadedScheme(url=f"/storage/{quote(obj.object_name)}", filename=obj.object_name.split('/')[1])
        for obj in repositories.get_files_list(user_id)
    ]


@router.post('/', response_model=FileUploadedScheme)
async def add_file(conn: DBConnection, user_id: UserID, file: UploadFile = File(...)):
    try:
        await repositories.check_user_id(conn, user_id)
    except ValueError as e:
        raise HTTPException(401, str(e))

    try:
        obj = repositories.upload_file(user_id, file)
        return FileUploadedScheme(
            url=f"/storage/{quote(obj.object_name)}",
            filename=obj.object_name.split('/')[1]
        )
    except ValueError as e:
        raise HTTPException(409, f"Failed to upload file: {str(e)}")


@router.delete('/{filename}', status_code=200)
async def delete_file(conn: DBConnection, user_id: UserID, filename: str):
    try:
        await repositories.check_user_id(conn, user_id)
    except ValueError as e:
        raise HTTPException(401, str(e))

    full_path = f'{user_id}/{filename}'
    if not repositories.is_file_exists(full_path):
        raise HTTPException(404, "File not found")
    try:
        repositories.delete_file(full_path)
        return Response(status_code=200)
    except ValueError as e:
        raise HTTPException(404, f"Failed to delete file: {str(e)}")
