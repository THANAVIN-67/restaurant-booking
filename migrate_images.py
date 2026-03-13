#!/usr/bin/env python3
"""
Script to upload all images from local static folder to Cloudinary
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
import cloudinary
import cloudinary.uploader

# Load environment variables
load_dotenv()

# Configure Cloudinary
cloudinary.config(
    cloud_name=os.getenv('CLOUDINARY_CLOUD_NAME'),
    api_key=os.getenv('CLOUDINARY_API_KEY'),
    api_secret=os.getenv('CLOUDINARY_API_SECRET')
)

static_folder = 'static'

# Get all image files
image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.webp'}
image_files = [f for f in os.listdir(static_folder) 
               if os.path.isfile(os.path.join(static_folder, f)) 
               and Path(f).suffix.lower() in image_extensions]

print(f"🖼️  Found {len(image_files)} image files to upload")
print()

uploaded_count = 0
failed_count = 0

for filename in sorted(image_files):
    image_path = os.path.join(static_folder, filename)
    
    try:
        print(f"⬆️  Uploading {filename}...", end=' ')
        
        upload_result = cloudinary.uploader.upload(
            image_path,
            folder='yumpooma_menu',  # remove trailing slash
            public_id=Path(filename).stem,
            resource_type='auto'
        )
        
        image_url = upload_result['secure_url']
        
        print(f"✅")
        print(f"    🔗 {image_url}")
        uploaded_count += 1
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        failed_count += 1

print()
print("=" * 80)
print("📊 Upload Summary:")
print(f"   ✅ Uploaded: {uploaded_count}")
print(f"   ❌ Failed: {failed_count}")
print("=" * 80)

if failed_count == 0:
    print("\n🎉 All images uploaded successfully!")
else:
    print(f"\n⚠️  Upload completed with {failed_count} error(s)!")


