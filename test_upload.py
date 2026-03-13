import cloudinary, cloudinary.uploader, os
from dotenv import load_dotenv

load_dotenv()
# configure explicitly OR rely on CLOUDINARY_URL variable
cloudinary.config(
    cloud_name=os.getenv('CLOUDINARY_CLOUD_NAME'),
    api_key=os.getenv('CLOUDINARY_API_KEY'),
    api_secret=os.getenv('CLOUDINARY_API_SECRET')
)
print('env url', os.getenv('CLOUDINARY_URL'))
print('config', os.getenv('CLOUDINARY_CLOUD_NAME'), os.getenv('CLOUDINARY_API_KEY'))
print('secret length', len(os.getenv('CLOUDINARY_API_SECRET')))
try:
    res = cloudinary.uploader.upload('static/1.jpg')
    print('result', res)
except Exception as e:
    print('error', e)
