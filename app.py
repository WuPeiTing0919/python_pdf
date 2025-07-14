from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.pdfmetrics import stringWidth
import uuid, os

app = FastAPI()

os.makedirs("static", exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")

pdfmetrics.registerFont(TTFont("TWFont", "NotoSansTC-Medium.ttf"))

class TextRequest(BaseModel):
    content: str

@app.post("/generate-pdf")
def generate_pdf(data: TextRequest, request: Request):
    filename = f"{uuid.uuid4()}.pdf"
    filepath = os.path.join("static", filename)

    c = canvas.Canvas(filepath, pagesize=A4)
    c.setFont("TWFont", 12)

    text_obj = c.beginText(50, 800)
    text_obj.setFont("TWFont", 12)

    max_line_width = A4[0] - 50 * 2  # 頁寬扣左右邊距

    for line in data.content.splitlines():
        while stringWidth(line, "TWFont", 12) > max_line_width:
            for i in range(len(line), 0, -1):
                if stringWidth(line[:i], "TWFont", 12) <= max_line_width:
                    text_obj.textLine(line[:i])
                    line = line[i:]
                    break
        text_obj.textLine(line)

    c.drawText(text_obj)
    c.showPage()
    c.save()

    return {
        "download_url": str(request.base_url).rstrip("/") + f"/static/{filename}"
    }
