# ComfyUI Load Most Recent Image Node

A custom ComfyUI node that automatically loads the most recent image from a specified folder. This node is similar to the built-in "Load Image" node but automatically selects the newest file based on modification timestamp.

## Features

- 🔄 Automatically loads the most recent image from a specified folder
- 🖼️ Supports multiple image formats (JPG, PNG, BMP, TIFF, WebP, GIF)
- 📁 Configurable folder path input
- 🎭 Provides both image and mask outputs (with proper alpha channel handling)
- ⚡ Efficient file scanning with timestamp-based selection
- 🔍 Customizable image file extensions
- ✅ Full ComfyUI validation and error handling
- 🔒 Robust image format validation and error reporting

## Installation

### Method 1: Using the Install Script (Recommended)
1. Download or clone this repository
2. Open a terminal/command prompt in the downloaded folder
3. Run the installation script:
   ```bash
   python install.py
   ```
   Or specify your ComfyUI path manually:
   ```bash
   python install.py --comfyui-path "C:\path\to\your\ComfyUI"
   ```
4. Restart ComfyUI

### Method 2: Git Clone
1. Navigate to your ComfyUI custom nodes directory:
   ```bash
   cd ComfyUI/custom_nodes/
   ```

2. Clone this repository:
   ```bash
   git clone https://github.com/your-username/comfy-load-last-image.git
   ```

3. Restart ComfyUI

### Method 3: Manual Installation
1. Download the repository as a ZIP file
2. Extract it to your `ComfyUI/custom_nodes/` directory
3. Restart ComfyUI

## Usage

1. Add the "Load Most Recent Image" node to your ComfyUI workflow
2. Set the `folder_path` parameter to the directory containing your images
3. Optionally customize the `image_extensions` parameter (default: "jpg,jpeg,png,bmp,tiff,tif,webp")
4. Connect the image and mask outputs to other nodes as needed

### Parameters

- **folder_path** (required): Path to the folder containing images
- **image_extensions** (optional): Comma-separated list of image file extensions to search for

### Outputs

- **image**: The loaded image as a tensor
- **mask**: The alpha channel as a mask (or a white mask if no alpha channel exists)

## Example Use Cases

- 🎨 Automatically load the latest generated image from an output folder
- 📸 Process the most recent screenshot or photo
- 🔄 Create workflows that automatically work with new images as they're added
- 🎬 Animation workflows that process the latest frame

## Technical Details

The node:
- Scans the specified folder for image files with the given extensions
- Selects the file with the most recent modification timestamp
- Loads the image using PIL and converts it to the format expected by ComfyUI
- Handles both RGB and RGBA images
- Provides proper mask output from alpha channels or creates a default white mask

## Troubleshooting

### "Invalid image file" Error
If you get an error like "Invalid image file: filename.png", this usually means:
1. The image file is corrupted or incomplete
2. The file has an unsupported format
3. The file extension doesn't match the actual content

**Solutions:**
- Check if the image opens correctly in an image viewer
- Try with a different image format (PNG is usually most reliable)
- Ensure the file is completely written (not still being created by another process)

### "No image files found" Error
This means the node couldn't find any images in the specified folder.

**Solutions:**
- Verify the folder path is correct
- Check the `image_extensions` parameter includes the formats you're using
- Ensure the folder actually contains image files

### Node Not Appearing in ComfyUI
If the node doesn't appear after installation:
1. Restart ComfyUI completely
2. Check the ComfyUI console for any error messages
3. Verify the node files are in the correct location (`ComfyUI/custom_nodes/comfy-load-last-image/`)
4. Make sure all required files (`__init__.py`, `load_most_recent_image.py`) are present

### Performance Issues
If the node is slow when scanning large folders:
- Consider organizing images into smaller subfolders
- Use more specific file extensions to reduce scanning time
- The node caches file information, so subsequent runs should be faster

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

If you encounter any issues, please create an issue on the GitHub repository with:
- Your ComfyUI version
- The error message (if any)
- A description of what you were trying to do
- Your operating system

## License

MIT License - see LICENSE file for details.
