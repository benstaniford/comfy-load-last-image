#!/usr/bin/env python3
"""
Installation script for the Load Most Recent Image ComfyUI node.
This script helps users install the node into their ComfyUI installation.
"""

import os
import sys
import shutil
import argparse
from pathlib import Path


def find_comfyui_directory():
    """Try to find ComfyUI directory automatically"""
    possible_paths = [
        # Windows common locations
        r"C:\Users\%USERNAME%\ComfyUI",
        r"C:\ComfyUI",
        r"C:\Program Files\ComfyUI",
        r"C:\Users\%USERNAME%\Programs\ComfyUI",
        # Linux/Mac common locations
        "/opt/ComfyUI",
        "/usr/local/ComfyUI",
        "~/ComfyUI",
        "~/Programs/ComfyUI",
        # Current directory
        "./ComfyUI",
        "../ComfyUI",
    ]
    
    for path in possible_paths:
        expanded_path = os.path.expandvars(os.path.expanduser(path))
        if os.path.exists(expanded_path) and os.path.isdir(expanded_path):
            custom_nodes_path = os.path.join(expanded_path, "custom_nodes")
            if os.path.exists(custom_nodes_path):
                return expanded_path
    
    return None


def install_node(comfyui_path, source_path):
    """Install the node to ComfyUI custom_nodes directory"""
    custom_nodes_path = os.path.join(comfyui_path, "custom_nodes")
    target_path = os.path.join(custom_nodes_path, "comfy-load-last-image")
    
    if not os.path.exists(custom_nodes_path):
        print(f"❌ Custom nodes directory not found: {custom_nodes_path}")
        return False
    
    try:
        # Remove existing installation if it exists
        if os.path.exists(target_path):
            print(f"🔄 Removing existing installation at {target_path}")
            shutil.rmtree(target_path)
        
        # Copy the node files
        print(f"📁 Installing node to {target_path}")
        shutil.copytree(source_path, target_path)
        
        # Create requirements.txt in the target directory if it doesn't exist
        requirements_path = os.path.join(target_path, "requirements.txt")
        if not os.path.exists(requirements_path):
            with open(requirements_path, "w") as f:
                f.write("torch>=1.9.0\n")
                f.write("torchvision>=0.10.0\n")
                f.write("Pillow>=8.0.0\n")
                f.write("numpy>=1.21.0\n")
        
        print("✅ Node installed successfully!")
        print(f"📍 Installation location: {target_path}")
        print("🔄 Please restart ComfyUI to load the new node.")
        
        return True
        
    except Exception as e:
        print(f"❌ Error installing node: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(description="Install Load Most Recent Image node for ComfyUI")
    parser.add_argument("--comfyui-path", type=str, help="Path to ComfyUI installation")
    parser.add_argument("--source-path", type=str, default=".", help="Path to node source code")
    
    args = parser.parse_args()
    
    print("🚀 ComfyUI Load Most Recent Image Node Installer")
    print("=" * 50)
    
    # Determine source path
    source_path = os.path.abspath(args.source_path)
    if not os.path.exists(source_path):
        print(f"❌ Source path does not exist: {source_path}")
        sys.exit(1)
    
    # Check if this looks like our node directory
    required_files = ["load_most_recent_image.py", "__init__.py"]
    for file in required_files:
        if not os.path.exists(os.path.join(source_path, file)):
            print(f"❌ Required file not found: {file}")
            print(f"Make sure you're running this from the node directory.")
            sys.exit(1)
    
    # Determine ComfyUI path
    comfyui_path = args.comfyui_path
    if not comfyui_path:
        print("🔍 Searching for ComfyUI installation...")
        comfyui_path = find_comfyui_directory()
        
        if not comfyui_path:
            print("❌ Could not find ComfyUI installation automatically.")
            print("Please specify the path using --comfyui-path")
            sys.exit(1)
        else:
            print(f"✅ Found ComfyUI at: {comfyui_path}")
    
    # Validate ComfyUI path
    if not os.path.exists(comfyui_path):
        print(f"❌ ComfyUI path does not exist: {comfyui_path}")
        sys.exit(1)
    
    # Install the node
    success = install_node(comfyui_path, source_path)
    
    if success:
        print("\n🎉 Installation completed successfully!")
        print("Next steps:")
        print("1. Restart ComfyUI")
        print("2. Look for 'Load Most Recent Image' in the image category")
        print("3. Set the folder_path parameter to a folder containing images")
        print("4. Enjoy automatic loading of the most recent image!")
    else:
        print("\n❌ Installation failed!")
        sys.exit(1)


if __name__ == "__main__":
    main()
