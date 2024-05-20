import text_generate
import summarize
import ujson
import urllib
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
import shutil
import os
app = FastAPI()


@app.post("/uploadfile/")
async def upload_file(file: UploadFile = File(...)):
    try:
        # 업로드된 파일이 음성 파일인지 확인 (확장자에 따라)
        allowed_extensions = ("wav", "mp3", "ogg")  # 허용된 음성 파일 형식
        file_extension = file.filename.split(".")[-1]
        if file_extension not in allowed_extensions:
            raise HTTPException(status_code=400, detail="Unsupported file format. Supported formats: wav, mp3, ogg")

        # 파일 저장할 경로 지정 (현재 디렉토리의 uploads 폴더에 저장)
        with open(os.path.join("uploads", file.filename), "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        return JSONResponse(status_code=200, content={"message": "File uploaded successfully"})
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": f"Error: {str(e)}"})
#디비에 현재 파일 이름 

@app.post("/AI_process/")
async def AI_process_start(file_name):
    try:
        print("AI_process_start is start")
        #file_name is path for process
        input_file_path_='uploads/'
        output_file_path_='output/'
        # voice_text=text_generate.text_generate(input_file_path=input_file_path_,
        #                             output_file_path=output_file_path_,
        #                             languagecode='korean')
        voice_text= ("머신러닝은 데이터 과학과 컴퓨터 공학의 교차점에 위치한 분야로, 컴퓨터가 데이터로부터 패턴을 발견하고 학습하여 작업을 자동화하거나 예측하는 기술입니다."
                     " 또한 머신러닝은 자율 주행 자동차, 음성 인식, 언어 번역, 추천 시스템 등 다양한 응용 분야에서 혁신을 이끌고 있습니다. 이러한 기술의 발전은 데이터의 양과 품질이"
                     " 증가함에 따라 더욱 가속화되고 있으며, 머신러닝은 미래의 기술과 산업을 선도하는 핵심 역할을 수행할 것으로 기대됩니다.")






        print("text_generate is finish")
        print(f'text is {voice_text}')
        
        summarize_text=summarize.summarize(voice_text)

        print(summarize_text)
        
        

    except Exception as e:
        return JSONResponse(status_code=500, content={"message": f"Error: {str(e)}"})



if __name__ == "__main__":
    import uvicorn

    # uvicorn을 사용하여 FastAPI 서버 실행
    uvicorn.run(app, host="localhost", port=8000)

