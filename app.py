from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from reportlab.pdfgen import canvas
import uuid, os

app = FastAPI()

os.makedirs("static", exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")

class TextRequest(BaseModel):
    content: str

@app.post("/generate-pdf")
def generate_pdf(data: TextRequest):
    filename = f"{uuid.uuid4()}.pdf"
    filepath = os.path.join("static", filename)

    c = canvas.Canvas(filepath)
    c.setFont("Helvetica", 12)
    c.drawString(100, 750, data.content[:1000])  # 控制最多幾個字，否則會 overflow
    c.save()

    return {
        "url": f"/static/{filename}"
    }
