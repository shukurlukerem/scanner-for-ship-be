# app/utils.py
import qrcode
import base64
from io import BytesIO

def generate_qr_base64(text: str) -> str:
    qr = qrcode.make(text)
    buffer = BytesIO()
    qr.save(buffer, format="PNG")
    base64_qr = base64.b64encode(buffer.getvalue()).decode("utf-8")
    return f"data:image/png;base64,{base64_qr}"
