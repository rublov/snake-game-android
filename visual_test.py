"""
Visual Testing Script for Snake Game
Uses Pillow to capture screenshots and compare images for
visual regression testing.
"""

import os
from PIL import Image, ImageChops
import pygame


def capture_screenshot(filename="screenshot.png"):
    """
    Capture a screenshot of the current Pygame window.
    Note: This requires the game to be running and
    pygame.display.get_surface() to work.
    """
    try:
        screen = pygame.display.get_surface()
        if screen:
            # Convert Pygame surface to PIL Image
            screenshot = Image.frombytes(
                'RGB', screen.get_size(),
                pygame.image.tostring(screen, 'RGB')
            )
            screenshot.save(filename)
            print(f"Screenshot saved as {filename}")
        else:
            print("No Pygame surface available. "
                  "Make sure the game is running.")
    except Exception as e:
        print(f"Error capturing screenshot: {e}")


def compare_images(image1_path, image2_path, diff_path="diff.png"):
    """
    Compare two images and save the difference if they are different.
    Returns True if images are identical, False otherwise.
    """
    try:
        img1 = Image.open(image1_path)
        img2 = Image.open(image2_path)

        # Ensure images are the same size
        if img1.size != img2.size:
            print("Images have different sizes, cannot compare.")
            return False

        # Calculate difference
        diff = ImageChops.difference(img1, img2)

        # Check if there are any differences
        if diff.getbbox() is None:
            print("Images are identical.")
            return True
        else:
            # Save difference image
            diff.save(diff_path)
            print(f"Images differ. Difference saved as {diff_path}")
            return False

    except Exception as e:
        print(f"Error comparing images: {e}")
        return False


def run_visual_test():
    """
    Example visual test: Capture screenshot and compare with baseline.
    """
    baseline_image = "baseline_screenshot.png"

    # Capture current screenshot
    capture_screenshot("current_screenshot.png")

    # If baseline exists, compare
    if os.path.exists(baseline_image):
        if compare_images(baseline_image, "current_screenshot.png"):
            print("Visual test passed: No changes detected.")
        else:
            print("Visual test failed: Changes detected.")
    else:
        print(f"Baseline image not found. Saving current as {baseline_image}")
        os.rename("current_screenshot.png", baseline_image)


if __name__ == "__main__":
    # Note: This script should be run while the game is active
    # For automated testing, integrate into the game loop or use threading

    print("Visual Testing Script")
    print("Make sure the Snake Game is running before capturing screenshots.")
    run_visual_test()
