from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
import io
import base64
from rembg import remove # 🌟 배경 제거 마법사 부품 추가!

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
    return {"status": "띠부실메이커 AI (누끼 기능 탑재) 정상 작동 중!"}

@app.post("/pixelate")
async def pixelate_image(file: UploadFile = File(...)):
    try:
        request_object_content = await file.read()
        
        # 1. 🌟 AI를 이용해 배경을 투명하게 날려버립니다 (누끼 따기)
        no_bg_bytes = remove(request_object_content)
        
        # 2. 배경이 지워진 이미지를 엽니다
        img = Image.open(io.BytesIO(no_bg_bytes))
        img = img.convert("RGBA")
        
        # 3. 요청하신 128x128 사이즈로 픽셀 아트로 변환합니다
        pixel_size = 128
        img_small = img.resize((pixel_size, pixel_size), resample=Image.Resampling.BILINEAR)
        img_quantized = img_small.quantize(colors=16).convert("RGBA")
        img_retro = img_quantized.resize((300, 300), resample=Image.Resampling.NEAREST)
        
        img_byte_arr = io.BytesIO()
        img_retro.save(img_byte_arr, format='PNG')
        img_byte_arr = img_byte_arr.getvalue()
        base64_encoded = base64.b64encode(img_byte_arr).decode('utf-8')
        
        return {"pixel_image": f"data:image/png;base64,{base64_encoded}"}
    except Exception as e:
        return {"error": f"서버 에러 발생: {str(e)}"}
