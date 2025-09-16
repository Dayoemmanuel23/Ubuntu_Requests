import os
import requests
from urllib.parse import urlparse, unquote
from pathlib import Path
from datetime import datetime

def create_directory(directory_name):
    """Create directory if it doesn't exist, respecting the community's shared space"""
    try:
        os.makedirs(directory_name, exist_ok=True)
        print(f"Directory '{directory_name}' is ready for community sharing.")
    except OSError as e:
        print(f"Error creating directory: {e}")
        return False
    return True

def extract_filename(url, content_type):
    """Extract or generate an appropriate filename with community respect"""
    # Try to get filename from URL
    path = urlparse(url).path
    filename = unquote(Path(path).name)
    
    # If no filename in URL, generate one based on content type and timestamp
    if not filename or '.' not in filename:
        extension = get_extension_from_content_type(content_type)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"community_image_{timestamp}{extension}"
    else:
        # Ensure the filename is safe for the community's shared space
        filename = sanitize_filename(filename)
    
    return filename

def get_extension_from_content_type(content_type):
    """Map content type to appropriate file extension"""
    extension_map = {
        'image/jpeg': '.jpg',
        'image/jpg': '.jpg',
        'image/png': '.png',
        'image/gif': '.gif',
        'image/webp': '.webp',
        'image/svg+xml': '.svg',
        'image/tiff': '.tiff',
        'image/bmp': '.bmp'
    }
    return extension_map.get(content_type, '.jpg')  # Default to jpg if unknown

def sanitize_filename(filename):
    """Make filename safe for community storage"""
    # Remove any path components and keep only the base name
    filename = os.path.basename(filename)
    # Replace problematic characters with underscores
    for char in [' ', '<', '>', ':', '"', '/', '\\', '|', '?', '*']:
        filename = filename.replace(char, '_')
    # Limit length to respect community storage
    if len(filename) > 100:
        name, ext = os.path.splitext(filename)
        filename = name[:100-len(ext)] + ext
    return filename

def download_image(url, directory="Fetched_Images"):
    """Respectfully fetch and save an image from our global community"""
    # Create directory for community sharing
    if not create_directory(directory):
        return False
    
    try:
        print(f"Connecting to our global community at {url}...")
        # Respectfully request the resource with appropriate headers
        headers = {
            'User-Agent': 'UbuntuImageFetcher/1.0 (Community Image Sharing Tool)'
        }
        response = requests.get(url, headers=headers, timeout=30)
        
        # Check for HTTP errors with respect
        response.raise_for_status()
        
        # Determine content type with fallback
        content_type = response.headers.get('content-type', '').split(';')[0]
        
        # Extract or generate filename
        filename = extract_filename(url, content_type)
        filepath = os.path.join(directory, filename)
        
        # Save the image with community appreciation
        with open(filepath, 'wb') as f:
            f.write(response.content)
        
        print(f"Successfully saved community image: {filename}")
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"Respectfully, we couldn't connect to the community resource: {e}")
    except Exception as e:
        print(f"An unexpected error occurred while sharing: {e}")
    
    return False

def main():
    """Main function that embodies the Ubuntu spirit"""
    print("=" * 60)
    print("Ubuntu Image Fetcher: I am because we are")
    print("=" * 60)
    print("This tool connects to our global community,")
    print("respectfully fetches shared images, and")
    print("organizes them for later appreciation.")
    print("=" * 60)
    
    # Prompt user for community resource
    url = input("Please enter the URL of the community image: ").strip()
    
    if not url:
        print("No URL provided. We need each other to thrive.")
        return
    
    # Fetch and save the image with Ubuntu spirit
    success = download_image(url)
    
    if success:
        print("\nThank you for sharing with our community!")
        print("The image has been saved for future appreciation.")
    else:
        print("\nThough we faced challenges, our community remains strong.")
        print("Please try again with a different resource.")

if __name__ == "__main__":
    main()