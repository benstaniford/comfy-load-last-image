"""
ComfyUI Load Most Recent Image Node

A custom node for ComfyUI that loads the most recent image from a specified folder.
"""

from .load_most_recent_image import LoadMostRecentImage

NODE_CLASS_MAPPINGS = {
    "LoadMostRecentImage": LoadMostRecentImage
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "LoadMostRecentImage": "Load Most Recent Image"
}

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]
