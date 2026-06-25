from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
import io
import base64

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"status": "띠부실메이커 AI 정상 작동 중!"}

@app.post("/pixelate")
async def pixelate_image(file: UploadFile = File(...)):
    try:
        request_object_content = await file.read()
        img = Image.open(io.BytesIO(request_object_content))
        img = img.convert("RGBA")
        
        # 🌟 최신 버전에 맞춘 픽셀화 리사이징 문법 (Image.Resampling 사용)
        pixel_size = 64
        img_small = img.resize((pixel_size, pixel_size), resample=Image.Resampling.BILINEAR)
        img_quantized = img_small.quantize(colors=16).convert("RGBA")
        img_retro = img_quantized.resize((300, 300), resample=Image.Resampling.NEAREST)
        
        img_byte_arr = io.BytesIO()
        img_retro.save(img_byte_arr, format='PNG')
        img_byte_arr = img_byte_arr.getvalue()
        base64_encoded = base64.b64encode(img_byte_arr).decode('utf-8')
        
        return {"pixel_image": f"data:image/png;base64,{base64_encoded}"}
    except Exception as e:
        # 🌟 서버에서 에러가 나면, 원인을 숨기지 않고 바로 앱으로 쏴줍니다!
        return {"error": f"서버 에러 발생: {str(e)}"}
