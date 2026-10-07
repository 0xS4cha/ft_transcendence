def read_patchnote(version: str, language: str) -> str | None:
	try:
		with open(f"/app/src/backend_app/patchnotes/{version}_{language.lower()}.html", 'r') as f:
			return f.read()
	except (FileNotFoundError, OSError, PermissionError):
		return None