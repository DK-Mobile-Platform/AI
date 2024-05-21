import utils.text_generate as text_generate
import utils.summarize as summarize
import ujson
import urllib
from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.responses import JSONResponse
import shutil
import os
from pydub import AudioSegment
app = FastAPI()
from utils.voice_preprocessing import split_audio

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
        
        summarize_text,img_base64=summarize.summarize(voice_text)

        print(summarize_text)
        
        # Return both the summary and the image as a JSON response
        return JSONResponse(content={"predicted_title": summarize_text, "wordcloud_image": img_base64})
        
        

    except Exception as e:
        return JSONResponse(status_code=500, content={"message": f"Error: {str(e)}"})


@app.post("/Audio_preprocess/")
async def AI_process_start(file: UploadFile = File(...), output_dir: str = Form(...)):
    try:
        print("Audio_preprocess is start")
        
        # Read the uploaded file
        contents = await file.read()
        
        # Save the uploaded file temporarily
        temp_file_path = f"temp_{file.filename}"
        with open(temp_file_path, "wb") as temp_file:
            temp_file.write(contents)
        
        audio = AudioSegment.from_file(temp_file_path)
        
        
        split_audio(audio, output_dir)
        
        # Remove the temporary file
        os.remove(temp_file_path)
        
        return JSONResponse(status_code=200, content={"message": "Audio processing completed successfully."})

    except Exception as e:
        return JSONResponse(status_code=500, content={"message": f"Error: {str(e)}"})


if __name__ == "__main__":
    import uvicorn

    # uvicorn을 사용하여 FastAPI 서버 실행
    uvicorn.run(app, host="localhost", port=8000)

