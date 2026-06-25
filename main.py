from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
import io
import base64

app = FastAPI()

# 폰(앱)에서 서버에 접속할 수 있도록 문을 열어주는 설정 (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"status": "띠부실메이커 AI 서버 정상 가동 중! 🚀"}

@app.post("/pixelate")
async def pixelate_image(file: UploadFile = File(...)):
    try:
        # 1. 앱에서 보낸 원본 사진 읽기
        request_object_content = await file.read()
        img = Image.open(io.BytesIO(request_object_content))
        
        # 투명도 채널(RGBA) 유지 설정
        img = img.convert("RGBA")
        
        # 2. [픽셀 아트 효과] 이미지를 64x64 크기로 확 줄여서 도트(깍두기)화 시키기
        pixel_size = 64
        img_small = img.resize((pixel_size, pixel_size), resample=Image.BILINEAR)
        
        # 3. [레트로 감성] 사용할 색상을 딱 16가지로 강제 제한 (색상 단순화)
        img_quantized = img_small.quantize(colors=16).convert("RGBA")
        
        # 4. 띠부실 크기(300x300)로 픽셀이 깨지지 않게(NEAREST) 다시 늘리기
        img_retro = img_quantized.resize((300, 300), resample=Image.NEAREST)
        
        # 5. 완성된 이미지를 폰으로 보내기 위해 글자 형태(Base64)로 변환
        img_byte_arr = io.BytesIO()
        img_retro.save(img_byte_arr, format='PNG')
        img_byte_arr = img_byte_arr.getvalue()
        base64_encoded = base64.b64encode(img_byte_arr).decode('utf-8')
        
        # 앱이 바로 쓸 수 있는 이미지 URL 주소 형태로 리턴!
        return {"pixel_image": f"data:image/png;base64,{base64_encoded}"}
        
    except Exception as e:
        return {"error": str(e)}
