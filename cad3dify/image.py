import base64
import os
from typing import Literal

from pydantic import BaseModel

ImageTypes = Literal["jpg", "jpeg", "png", "gif"]


class ImageData(BaseModel):
    """Image data class

    Args:
        data (str): Image data (base64 encoded)
        type (ImageTypes): Image file extension
    """

    data: str
    type: ImageTypes

    @classmethod
    def load_from_file(cls, file_path: str) -> "ImageData":
        """Load image data from file

        Args:
            file_path (str): Path to the image file

        Returns:
            ImageData: Image data
        """
        with open(file_path, "rb") as f:
            data = base64.b64encode(f.read()).decode("utf-8")
        return cls(data=data, type=os.path.splitext(file_path)[1][1:])
