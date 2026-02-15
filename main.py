from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from ultralytics import YOLO
import io
from PIL import Image

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # بيسمح لأي أبلكيشن يكلم السيرفر (مهم جداً للـ MVP)
    allow_credentials=True,
    allow_methods=["*"],  # بيسمح بكل أنواع الطلبات (GET, POST, etc)
    allow_headers=["*"],
)

# 1. تحميل الموديل - تأكدي إن ملف الـ .pt في نفس الفولدر
# لو لسه معندكيش ملفك الخاص، اكتبي "yolov8n.pt" وهينزل لوحده للتجربة
model = YOLO("best.pt") 

@app.get("/")
def home():
    return {"status": "Smart Wheelchair API is Online"}

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    # 2. قراءة الصورة اللي جاية من الـ API
    request_object_content = await file.read()
    img = Image.open(io.BytesIO(request_object_content))

    # 3. تشغيل الموديل على الصورة
    results = model(img)
    
    # 4. تجميع النتائج بشكل نضيف
    detections = []
    for r in results:
        for box in r.boxes:
            detections.append({
                "object": model.names[int(box.cls)],
                "confidence": round(float(box.conf), 2),
                "location": box.xyxy.tolist() # إحداثيات المربع
            })

    return {"found": detections}