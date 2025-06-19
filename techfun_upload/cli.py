import os
import sys
import requests
import argparse
import time
from tqdm import tqdm
from requests_toolbelt.multipart.encoder import MultipartEncoder, MultipartEncoderMonitor

# Declare constants
DOMAIN = "https://file.techfun.me"
ALT_DOMAIN = "https://file.nigga.church"
CHUNK_SIZE = 95 * 1024 * 1024  # 95 MB
MAX_SIZE = 540 * CHUNK_SIZE  # ~50 GB

def format_size(bytes):
    """Translate bytes to human-readable units"""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes < 1024:
            return f"{bytes:.2f} {unit}"
        bytes /= 1024
    return f"{bytes:.2f} PB"

def upload_file(file_path, nigga_mode=False):
    """Upload file to TechFun's server"""
    # Get filename and size
    filename = os.path.basename(file_path)
    file_size = os.path.getsize(file_path)
    
    print(f"File: {filename} ({format_size(file_size)})")
    
    # Check file size
    if file_size > MAX_SIZE:
        print("File size exceeds max limit (50 GB).")
        sys.exit(1)
    
    token = ""
    total_chunks = (file_size + CHUNK_SIZE - 1) // CHUNK_SIZE
    uploaded_size = 0
    failed_attempts = 0

    with tqdm(total=file_size, unit='B', unit_scale=True, desc="Uploading") as pbar:
        with open(file_path, 'rb') as f:
            for i in range(total_chunks):
                chunk = f.read(CHUNK_SIZE)
                base_offset = i * CHUNK_SIZE
                failed_attempts = 0

                while failed_attempts < 10:
                    try:
                        if failed_attempts: 
                            time.sleep(2)

                        # Reset progress bar in case of failed attempt
                        pbar.n = base_offset
                        pbar.refresh()

                        # Prepare request
                        url = f"{DOMAIN}/upload?token={token}"
                        if i == total_chunks - 1:
                            url += "&done=true"
                        
                        # Create progress callback to update pbar
                        def callback(monitor):
                            current_bytes = base_offset + monitor.bytes_read
                            pbar.update(current_bytes - pbar.n)
                        
                        # Setup multipart encoder to include callback
                        fields = {'file': (filename, chunk, 'application/octet-stream')}
                        encoder = MultipartEncoder(fields=fields)
                        monitor = MultipartEncoderMonitor(encoder, callback)
                        headers = {'Content-Type': monitor.content_type}

                        response = requests.post(url, data=monitor, headers=headers)
                        
                        # Handle response
                        if response.status_code == 200:
                            token = response.json().get('token', '')
                            uploaded_size += len(chunk)
                            failed_attempts = 0
                            break
                        else:
                            failed_attempts += 1
                    except Exception as e:
                        failed_attempts += 1
                
                if failed_attempts >= 10:
                    print("Upload failed after 10 attempts")
                    sys.exit(1)
    
    # Return url
    if nigga_mode:
        return f"{ALT_DOMAIN}/{token}"
    return f"{DOMAIN}/file/{token}"

def main():
    parser = argparse.ArgumentParser(description='Upload files to TechFun server')
    parser.add_argument('-n', '--nigga', action='store_true', help='Use dark mode URL instead of light mode URL')
    parser.add_argument('file', help='Path to file to upload')
    args = parser.parse_args()
    
    try:
        if not os.path.exists(args.file):
            print(f"File not found: {args.file}")
            sys.exit(1)
        
        result = upload_file(args.file, args.nigga)
        print("\nUpload successful!")
        print(result)
        sys.exit(0)
    except Exception as e:
        print(f"\nError: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
