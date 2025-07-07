# ComfyUI Load Most Recent Image Node

A custom ComfyUI node that automatically loads the most recent image from a specified folder. This node is similar to the built-in "Load Image" node but automatically selects the newest file based on modification timestamp.

## Features

- 🔄 Automatically loads the most recent image from a specified folder
- 🖼️ Supports multiple image formats (JPG, PNG, BMP, TIFF, WebP, etc.)
- 📁 Configurable folder path input
- 🎭 Provides both image and mask outputs
- ⚡ Efficient file scanning with timestamp-based selection
- 🔍 Customizable image file extensions

## Installation

### Method 1: Git Clone (Recommended)
1. Navigate to your ComfyUI custom nodes directory:
   ```bash
   cd ComfyUI/custom_nodes/
   ```

2. Clone this repository:
   ```bash
   git clone https://github.com/your-username/comfy-load-last-image.git
   ```

3. Restart ComfyUI

### Method 2: Manual Installation
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

## Requirements

- ComfyUI
- Python 3.8+
- PIL (Pillow)
- torch
- numpy

## License

MIT License - see LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

If you encounter any issues, please create an issue on the GitHub repository.
