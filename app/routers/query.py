from fastapi import APIRouter, UploadFile, File
from CNN import cHDF
from PIL import Image
import io

router = APIRouter(
    prefix='/query'
)


@router.post('upload')
async def query_upload(file: UploadFile = File(...)):
    byte_data = await file.read()
    image = Image.open(io.BytesIO(byte_data))
    cHDF.record(image)
