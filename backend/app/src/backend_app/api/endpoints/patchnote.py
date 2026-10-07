from fastapi import APIRouter, HTTPException, status
from fastapi.responses import HTMLResponse

from backend_app.patchnotes import read_patchnote

router = APIRouter()

CURRENT_VERSION = "18.3"

cached_patchnote = {}

@router.get("/latest", response_class=HTMLResponse)
def get_patchnote(lang: str = "EN"):
	if lang.strip().upper() not in ["EN", "ES", "FR"]:
		raise HTTPException(
			status_code=status.HTTP_400_BAD_REQUEST,
			detail="Invalid language"
		)
	language = lang.strip().upper()
	if CURRENT_VERSION not in cached_patchnote:
		cached_patchnote[CURRENT_VERSION] = {}
	if language not in cached_patchnote[CURRENT_VERSION]:
		cached_patchnote[CURRENT_VERSION][language] = read_patchnote(CURRENT_VERSION, language)

	return cached_patchnote[CURRENT_VERSION][language] or "<p style='color: red;'>ERR: No patchnote available...</p>"