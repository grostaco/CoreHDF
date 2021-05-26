from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, status
from ..dependencies import get_current_active_user
from ..sql_app.schemas import User, LogResponse

from typing import Optional

from CNN import cHDF, cLog
from PIL import Image
from enum import Enum
import io
import json

router = APIRouter(
    prefix='/query'
)


class Permissions(Enum) :
    LOG = 1
    UPLOAD = 2


@router.post('/upload')
async def query_upload(file: UploadFile = File(...), current_user: User = Depends(get_current_active_user)):
    if (current_user.permissions & Permissions.UPLOAD.value) == Permissions.UPLOAD.value :
        byte_data = await file.read()
        image = Image.open(io.BytesIO(byte_data))
        cHDF.record(image)
        return
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Insufficient permission',
        headers={'WWW-Authenticate': 'Bearer'},
    )


@router.get('/logs')
async def query_logs(limit: int, selector: Optional[str] = 'All', current_user: User = Depends(get_current_active_user)) :
    if (current_user.permissions & Permissions.LOG.value) == Permissions.LOG.value :
        logs = None
        if selector == 'All' :
            logs = cLog.get_last_logs(limit, force_reload=True)
        elif selector == 'Detection':
            logs = cLog.get_detected(limit, force_reload=True)

        logs = [log.json() for log in logs]
        return logs

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Insufficient permission',
        headers={'WWW-Authenticate' : 'Bearer'},
    )
