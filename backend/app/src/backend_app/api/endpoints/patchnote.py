from fastapi import APIRouter
from fastapi.responses import HTMLResponse

from backend_app.patchnotes import read_patchnote

router = APIRouter()

CURRENT_VERSION = "18.3"

cached_patchnote = {}

@router.get("/latest", response_class=HTMLResponse)
def get_patchnote():
	if CURRENT_VERSION not in cached_patchnote:
		cached_patchnote[CURRENT_VERSION] = read_patchnote(CURRENT_VERSION)

	return cached_patchnote[CURRENT_VERSION] or "<p style='color: red;'>ERR: No patchnote available...</p>"