import os
import glob
from PIL import Image, ImageOps
import torch
import numpy as np
from pathlib import Path

# ComfyUI specific imports - these will be available when running in ComfyUI
try:
    import folder_paths
except ImportError:
    # This is expected when developing outside of ComfyUI
    folder_paths = None


class LoadMostRecentImage:
    """
    A ComfyUI node that loads the most recent image from a specified folder.
    Similar to the built-in Load Image node but automatically selects the newest file.
    """
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "folder_path": ("STRING", {
                    "default": "",
                    "multiline": False,
                    "placeholder": "Enter folder path..."
                }),
            },
            "optional": {
                "image_extensions": ("STRING", {
                    "default": "jpg,jpeg,png,bmp,tiff,tif,webp",
                    "multiline": False,
                    "placeholder": "Comma-separated extensions"
                }),
            }
        }
    
    RETURN_TYPES = ("IMAGE", "MASK")
    RETURN_NAMES = ("image", "mask")
    FUNCTION = "load_most_recent_image"
    CATEGORY = "image"
    
    def load_most_recent_image(self, folder_path, image_extensions="jpg,jpeg,png,bmp,tiff,tif,webp"):
        """
        Load the most recent image from the specified folder.
        
        Args:
            folder_path: Path to the folder containing images
            image_extensions: Comma-separated list of image extensions to look for
            
        Returns:
            tuple: (image_tensor, mask_tensor)
        """
        # Validate folder path
        if not folder_path or not os.path.exists(folder_path):
            raise ValueError(f"Folder path does not exist: {folder_path}")
        
        if not os.path.isdir(folder_path):
            raise ValueError(f"Path is not a directory: {folder_path}")
        
        # Parse extensions
        extensions = [ext.strip().lower() for ext in image_extensions.split(",")]
        extensions = [ext if ext.startswith('.') else f".{ext}" for ext in extensions]
        
        # Find all image files
        image_files = []
        for ext in extensions:
            pattern = os.path.join(folder_path, f"*{ext}")
            image_files.extend(glob.glob(pattern))
            # Also check uppercase extensions
            pattern = os.path.join(folder_path, f"*{ext.upper()}")
            image_files.extend(glob.glob(pattern))
        
        if not image_files:
            raise ValueError(f"No image files found in folder: {folder_path}")
        
        # Find the most recent file by modification time
        most_recent_file = max(image_files, key=os.path.getmtime)
        
        print(f"Loading most recent image: {most_recent_file}")
        
        # Load the image
        try:
            image = Image.open(most_recent_file)
            
            # Convert to RGB if necessary
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Convert to tensor format expected by ComfyUI
            image_array = np.array(image).astype(np.float32) / 255.0
            image_tensor = torch.from_numpy(image_array)[None,]  # Add batch dimension
            
            # Create mask - ComfyUI expects a mask even if we don't have alpha
            if 'A' in Image.open(most_recent_file).mode:
                # If original image has alpha channel, use it as mask
                original_image = Image.open(most_recent_file)
                if original_image.mode == 'RGBA':
                    alpha = original_image.split()[-1]
                    mask_array = np.array(alpha).astype(np.float32) / 255.0
                    mask_tensor = torch.from_numpy(mask_array)[None,]
                else:
                    # Create a white mask (fully opaque)
                    mask_array = np.ones((image_array.shape[0], image_array.shape[1]), dtype=np.float32)
                    mask_tensor = torch.from_numpy(mask_array)[None,]
            else:
                # Create a white mask (fully opaque)
                mask_array = np.ones((image_array.shape[0], image_array.shape[1]), dtype=np.float32)
                mask_tensor = torch.from_numpy(mask_array)[None,]
            
            return (image_tensor, mask_tensor)
            
        except Exception as e:
            raise ValueError(f"Error loading image {most_recent_file}: {str(e)}")
    
    @classmethod
    def IS_CHANGED(cls, folder_path, image_extensions="jpg,jpeg,png,bmp,tiff,tif,webp"):
        """
        Check if the most recent image in the folder has changed.
        This helps ComfyUI know when to reload the node.
        """
        if not folder_path or not os.path.exists(folder_path):
            return float("NaN")
        
        try:
            # Parse extensions
            extensions = [ext.strip().lower() for ext in image_extensions.split(",")]
            extensions = [ext if ext.startswith('.') else f".{ext}" for ext in extensions]
            
            # Find all image files
            image_files = []
            for ext in extensions:
                pattern = os.path.join(folder_path, f"*{ext}")
                image_files.extend(glob.glob(pattern))
                pattern = os.path.join(folder_path, f"*{ext.upper()}")
                image_files.extend(glob.glob(pattern))
            
            if not image_files:
                return float("NaN")
            
            # Return the modification time of the most recent file
            most_recent_file = max(image_files, key=os.path.getmtime)
            return os.path.getmtime(most_recent_file)
            
        except Exception:
            return float("NaN")


# Export the node class
NODE_CLASS_MAPPINGS = {
    "LoadMostRecentImage": LoadMostRecentImage
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "LoadMostRecentImage": "Load Most Recent Image"
}
