import os
import glob
from PIL import Image
import torch
import numpy as np

class LoadMostRecentImage:
    """
    A ComfyUI node that loads images from a specified folder by recency.
    Similar to the built-in Load Image node but automatically selects files by timestamp.
    
    Features:
    - Index 0 = most recent image
    - Index 1 = second most recent image
    - Index 2 = third most recent image, etc.
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
                "index": ("INT", {
                    "default": 0,
                    "min": 0,
                    "max": 1000,
                    "step": 1,
                    "display": "number"
                }),
            }
        }
    
    RETURN_TYPES = ("IMAGE", "MASK")
    RETURN_NAMES = ("image", "mask")
    FUNCTION = "load_most_recent_image"
    CATEGORY = "image"
    OUTPUT_NODE = False
    
    def load_most_recent_image(self, folder_path, image_extensions="jpg,jpeg,png,bmp,tiff,tif,webp", index=0):
        """
        Load the most recent image from the specified folder.
        
        Args:
            folder_path: Path to the folder containing images
            image_extensions: Comma-separated list of image extensions to look for
            index: Index of the image to load (0 = most recent, 1 = second most recent, etc.)
            
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
        
        # Sort files by modification time (most recent first)
        image_files.sort(key=os.path.getmtime, reverse=True)
        
        # Validate index
        if index >= len(image_files):
            raise ValueError(f"Index {index} is out of range. Only {len(image_files)} image(s) found in folder.")
        
        # Select the image at the specified index
        selected_file = image_files[index]
        
        print(f"Loading image at index {index}: {selected_file}")
        
        # Load and validate the image
        try:
            # First, validate the image file
            self._validate_image_file(selected_file)
            
            # Load the image
            image = Image.open(selected_file)

            # Convert image based on mode
            if image.mode == 'I':
                # 32-bit integer mode
                image = image.point(lambda i: i * (1 / 255))
            
            if 'transparency' in image.info:
                # Handle transparency
                image = image.convert('RGBA')
            
            if image.mode == 'RGBA':
                # Extract alpha channel for mask
                alpha = image.split()[-1]
                mask = np.array(alpha).astype(np.float32) / 255.0
                mask = 1.0 - mask  # Invert mask for ComfyUI convention
                image = image.convert('RGB')
            else:
                # Convert to RGB
                image = image.convert('RGB')
                # Create default mask (all white/opaque)
                mask = np.ones((image.height, image.width), dtype=np.float32)
            
            # Convert image to tensor
            image_array = np.array(image).astype(np.float32) / 255.0
            image_tensor = torch.from_numpy(image_array)[None,]  # Add batch dimension
            
            # Convert mask to tensor
            mask_tensor = torch.from_numpy(mask)[None,]  # Add batch dimension
            
            return (image_tensor, mask_tensor)
            
        except Exception as e:
            raise ValueError(f"Error loading image {selected_file}: {str(e)}")
    
    def _validate_image_file(self, image_path):
        """
        Validate that the image file is valid and can be opened.
        This mirrors the validation logic from ComfyUI's built-in LoadImage node.
        """
        try:
            with Image.open(image_path) as img:
                # Try to load the image data to ensure it's valid
                img.load()
                # Check if it's a valid image format
                if img.format not in ['JPEG', 'PNG', 'BMP', 'TIFF', 'WEBP', 'GIF']:
                    raise ValueError(f"Unsupported image format: {img.format}")
        except Exception as e:
            raise ValueError(f"Invalid image file: {os.path.basename(image_path)} - {str(e)}")
    
    @classmethod
    def VALIDATE_INPUTS(cls, folder_path, image_extensions="jpg,jpeg,png,bmp,tiff,tif,webp", index=0):
        """
        Validate inputs before execution.
        This method is called by ComfyUI to validate the node inputs.
        """
        # Validate folder path
        if not folder_path:
            return "Folder path cannot be empty"
        
        if not os.path.exists(folder_path):
            return f"Folder path does not exist: {folder_path}"
        
        if not os.path.isdir(folder_path):
            return f"Path is not a directory: {folder_path}"
        
        # Validate index
        if index < 0:
            return f"Index must be non-negative, got: {index}"
        
        # Parse extensions
        try:
            extensions = [ext.strip().lower() for ext in image_extensions.split(",")]
            extensions = [ext if ext.startswith('.') else f".{ext}" for ext in extensions]
        except Exception as e:
            return f"Invalid image extensions format: {str(e)}"
        
        # Find all image files
        image_files = []
        for ext in extensions:
            pattern = os.path.join(folder_path, f"*{ext}")
            image_files.extend(glob.glob(pattern))
            pattern = os.path.join(folder_path, f"*{ext.upper()}")
            image_files.extend(glob.glob(pattern))
        
        if not image_files:
            return f"No image files found in folder: {folder_path}"
        
        # Check if index is within range
        if index >= len(image_files):
            return f"Index {index} is out of range. Only {len(image_files)} image(s) found in folder."
        
        # Sort files by modification time (most recent first)
        image_files.sort(key=os.path.getmtime, reverse=True)
        
        # Find the file at the specified index and validate it
        try:
            selected_file = image_files[index]
            
            # Validate the image file
            with Image.open(selected_file) as img:
                img.load()
                if img.format not in ['JPEG', 'PNG', 'BMP', 'TIFF', 'WEBP', 'GIF']:
                    return f"Unsupported image format: {img.format}"
                    
        except Exception as e:
            return f"Error validating image at index {index}: {str(e)}"
        
        return True
    
    @classmethod
    def IS_CHANGED(cls, folder_path, image_extensions="jpg,jpeg,png,bmp,tiff,tif,webp", index=0):
        """
        Check if the image at the specified index in the folder has changed.
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
            
            # Sort files by modification time (most recent first)
            image_files.sort(key=os.path.getmtime, reverse=True)
            
            # Check if index is within range
            if index >= len(image_files):
                return float("NaN")
            
            # Return the modification time of the file at the specified index
            selected_file = image_files[index]
            return os.path.getmtime(selected_file)
            
        except Exception:
            return float("NaN")


# Export the node class
NODE_CLASS_MAPPINGS = {
    "LoadMostRecentImage": LoadMostRecentImage
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "LoadMostRecentImage": "Load Most Recent Image"
}
