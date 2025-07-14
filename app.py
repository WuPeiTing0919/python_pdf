from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import uuid, os

app = FastAPI()

os.makedirs("static", exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")

# ✅ 註冊中文字體（請確保字體檔案存在）
font_path = "NotoSansTC-Medium.ttf"  # 或使用微軟系統內建：msjh.ttc（微軟正黑體）
if os.path.exists(font_path):
    pdfmetrics.registerFont(TTFont("MyFont", font_path))
    font_name = "MyFont"
else:
    font_name = "Helvetica"  # fallback

class TextRequest(BaseModel):
    content: str

@app.post("/generate-pdf")
def generate_pdf(data: TextRequest, request: Request):
    filename = f"{uuid.uuid4()}.pdf"
    filepath = os.path.join("static", filename)

    c = canvas.Canvas(filepath)
    c.setFont(font_name, 12)
    c.drawString(100, 750, data.content[:1000])
    c.save()

    return {
        "url": str(request.base_url) + f"static/{filename}"
    }
