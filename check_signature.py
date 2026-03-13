import hashlib, os
from dotenv import load_dotenv
load_dotenv()
secret = os.getenv('CLOUDINARY_API_SECRET')
for ts in [1773300298]:
    s = f"timestamp={ts}{secret}"
    print('compute', hashlib.sha1(s.encode()).hexdigest())
    # show secret for debugging
print('secret used:', secret)