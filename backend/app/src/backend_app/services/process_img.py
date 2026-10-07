import os
from io import BytesIO
from typing import BinaryIO
from PIL import Image, ImageOps
from uuid import uuid4

import warnings

Image.MAX_IMAGE_PIXELS = 20000000
warnings.simplefilter("error", Image.DecompressionBombWarning)
    
def remove_file(path: str) -> None:
    try:
        os.remove(path)
    except FileNotFoundError:
        pass
    except OSError:
        print(f"Failed to remove {path}")

class ProcessImgBadRequestError(Exception):
    pass

class ProcessImgPayloadError(Exception):
    pass

class ProcessImgMediaTypeError(Exception):
    pass

class ProcessImgStorageError(Exception):
    pass

class ProcessImg:
    def __init__(self) -> None:
        self.max_bytes = 5*1024*1024
        self.max_pixels = Image.MAX_IMAGE_PIXELS
        self.allowed_formats = ["JPEG", "PNG"]
        self.output_dir = "/app/src/shared/profile_pictures"
        os.makedirs(self.output_dir, exist_ok=True)

    def process_profile_pic(
        self,
        file: BinaryIO
    ) -> str:
        try:
            raw = file.read(self.max_bytes + 1)
            if len(raw) > self.max_bytes:
                raise ProcessImgPayloadError("Image is too large")

            with Image.open(BytesIO(raw)) as image:
                if image.format not in self.allowed_formats:
                    raise ProcessImgMediaTypeError("Unsupported image type, use a JPEG, JPG or PNG image")

                if image.width * image.height > self.max_pixels:
                    raise ProcessImgPayloadError("Image dimensions are too large")

                image.verify()

            with Image.open(BytesIO(raw)) as image:
                image = ImageOps.exif_transpose(image)
                image.load()

                if "A" in image.getbands() or "transparency" in image.info:
                    image = image.convert("RGBA")
                else:
                    image = image.convert("RGB")

                output = BytesIO()
                image.save(output, format="WEBP")
                safe_bytes = output.getvalue()
        
        except (
            ProcessImgPayloadError,
            ProcessImgMediaTypeError,
        ):
            raise

        except Exception as e:
            raise ProcessImgBadRequestError("Invalid or unsupported image") from e

        image_id = uuid4().hex
        path = os.path.join(self.output_dir, f"{image_id}.webp")

        try:
            with open(path, "wb") as dest:
                dest.write(safe_bytes)
        except OSError as e:
            remove_file(path)
            print("[process_profile_pic] Failed to write profile picture")
            raise ProcessImgStorageError("Storage unavailable, try again later") from e

        return image_id
