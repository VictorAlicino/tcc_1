"""QR Code Generator"""
import qrcode.image.svg
import os
from jose import JWTError, jwt
from configurations.config import CONFIG

def generate_guest_acess(server_id: str, device_id: str) -> str:
    """Generate a QR code for guest access."""
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    cypher_suite = jwt.encode({"server_id": server_id, "device_id": device_id}, CONFIG['api-secrets']['secret_key'], algorithm="HS256")
    qr.add_data(cypher_suite)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    
    os.makedirs(f'assets/qr_codes/{server_id}', exist_ok=True)
    img.save(f'assets/qr_codes/{server_id}/{device_id}.png')
    return f'assets/qr_codes/{server_id}/{device_id}.png'