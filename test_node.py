#!/usr/bin/env python3
"""
Test script for the Load Most Recent Image node.
This script can be used to test the node functionality outside of ComfyUI.
"""

import os
import sys
import tempfile
import shutil
from PIL import Image
import numpy as np
import torch

# Add the current directory to the path so we can import our module
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from load_most_recent_image import LoadMostRecentImage


def create_test_images(test_dir):
    """Create test images with different timestamps"""
    print(f"Creating test images in {test_dir}")
    
    # Create some test images
    for i, color in enumerate([(255, 0, 0), (0, 255, 0), (0, 0, 255)]):
        img = Image.new('RGB', (100, 100), color)
        img_path = os.path.join(test_dir, f"test_image_{i}.png")
        img.save(img_path)
        print(f"Created: {img_path}")
        
        # Add small delay to ensure different timestamps
        import time
        time.sleep(0.1)
    
    return test_dir


def test_load_most_recent_image():
    """Test the Load Most Recent Image node"""
    print("Testing Load Most Recent Image node...")
    
    # Create a temporary directory with test images
    with tempfile.TemporaryDirectory() as temp_dir:
        test_dir = create_test_images(temp_dir)
        
        # Initialize the node
        node = LoadMostRecentImage()
        
        try:
            # Test loading the most recent image
            result = node.load_most_recent_image(test_dir)
            image_tensor, mask_tensor = result
            
            print(f"Image tensor shape: {image_tensor.shape}")
            print(f"Mask tensor shape: {mask_tensor.shape}")
            
            # Verify the tensors are in the expected format
            assert len(image_tensor.shape) == 4, f"Expected 4D tensor, got {len(image_tensor.shape)}D"
            assert len(mask_tensor.shape) == 3, f"Expected 3D mask tensor, got {len(mask_tensor.shape)}D"
            assert image_tensor.shape[0] == 1, f"Expected batch size 1, got {image_tensor.shape[0]}"
            assert image_tensor.shape[3] == 3, f"Expected 3 color channels, got {image_tensor.shape[3]}"
            
            print("✅ Basic loading test passed!")
            
            # Test IS_CHANGED functionality
            timestamp = node.IS_CHANGED(test_dir)
            print(f"IS_CHANGED returned: {timestamp}")
            assert not np.isnan(timestamp), "IS_CHANGED should return a valid timestamp"
            
            print("✅ IS_CHANGED test passed!")
            
            # Test with custom extensions
            result2 = node.load_most_recent_image(test_dir, "png,jpg")
            print("✅ Custom extensions test passed!")
            
            print("🎉 All tests passed!")
            
        except Exception as e:
            print(f"❌ Test failed: {e}")
            return False
    
    return True


def test_error_conditions():
    """Test error conditions"""
    print("\nTesting error conditions...")
    
    node = LoadMostRecentImage()
    
    # Test with non-existent directory
    try:
        node.load_most_recent_image("/non/existent/directory")
        print("❌ Should have raised error for non-existent directory")
        return False
    except ValueError as e:
        print(f"✅ Correctly raised error for non-existent directory: {e}")
    
    # Test with empty directory
    with tempfile.TemporaryDirectory() as temp_dir:
        try:
            node.load_most_recent_image(temp_dir)
            print("❌ Should have raised error for empty directory")
            return False
        except ValueError as e:
            print(f"✅ Correctly raised error for empty directory: {e}")
    
    print("🎉 Error condition tests passed!")
    return True


if __name__ == "__main__":
    print("=" * 50)
    print("Load Most Recent Image Node Test")
    print("=" * 50)
    
    # Check if required dependencies are available
    try:
        import torch
        import numpy as np
        from PIL import Image
        print("✅ All dependencies available")
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        sys.exit(1)
    
    # Run tests
    success = True
    success &= test_load_most_recent_image()
    success &= test_error_conditions()
    
    if success:
        print("\n🎉 All tests completed successfully!")
    else:
        print("\n❌ Some tests failed!")
        sys.exit(1)
