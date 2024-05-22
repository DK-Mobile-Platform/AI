import utils.text_generate as text_generate
import utils.summarize as summarize
from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.responses import JSONResponse
from pydub import AudioSegment
app = FastAPI()
from utils.voice_preprocessing import split_audio
import base64
import os


@app.post("/AI_process/")
async def AI_process_start(user_id):
    try:
        print("AI_process_start is start")
        #file_name is path for process
        main_directory = os.path.join("data", user_id)
        folder_path=os.path.join(main_directory,'voice')
        voice_text=text_generate.text_generate(folder_path,'korean')

        print("text_generate is finish")
        print(f'text is {voice_text}')


        folder_path=os.path.dirname(folder_path)
        folder_path=os.path.join(folder_path,'tmp')
        text_path = os.path.join(folder_path,'text')
        #save text voice_text to text_path 'data.txt'
        with open(os.path.join(text_path,'data.txt'), 'w', encoding='utf-8') as file:
            file.write(voice_text)

        image_path = os.path.join(folder_path,'img')
        summarize_text=summarize.summarize(voice_text,image_path)

        print("summarize finish")
        with open(os.path.join(text_path,'summarize.txt'), 'w', encoding='utf-8') as file:
            file.write(summarize_text)

        # Return both the summary and the image as a JSON response
        return JSONResponse(content={"predicted_title": summarize_text})



    except Exception as e:
        return JSONResponse(status_code=500, content={"message": f"Error: {str(e)}"})

import time
@app.post("/Audio_preprocess/")
async def Audio_preprocess(file: UploadFile = File(...), user_id: str = Form(...)):
    try:
        print("Audio_preprocess is start")

        main_directory = os.path.join("data", user_id)

        # 저장할 오디오 파일 경로
        audio_file_path = os.path.join(main_directory, "uploaded_audio.wav")

        # 업로드된 파일을 저장
        with open(audio_file_path, "wb") as audio_file:
            audio_file.write(await file.read())

        # 파일 경로 출력
        print("Saved audio file:", audio_file_path)

        audio =  AudioSegment.from_file(audio_file_path,format='m4a')

        folder_dir = os.path.join(main_directory, "voice")
        os.makedirs(folder_dir, exist_ok=True)
        # Start splitting audio
        split_audio(audio, folder_dir)

        return JSONResponse(status_code=200, content={"message": "Audio processing completed successfully."})

    except Exception as e:
        print("Error occurred:", str(e))
        return JSONResponse(status_code=500, content={"message": f"Error: {str(e)}"})

@app.post("/User_initial/")
async def User_initial(user_id: str = Form(...)):
    try:
        # Define the main directory path using the user_id
        main_directory = os.path.join("data", user_id)

        # Ensure the main directory exists
        if not os.path.exists(main_directory):
            os.makedirs(main_directory)


        return JSONResponse(status_code=200, content={"message": "Directories created successfully."})

    except Exception as e:
        return JSONResponse(status_code=500, content={"message": f"Error: {str(e)}"})


@app.post("/Get_User_text_data/")
async def Get_User_text_data(user_id: str = Form(...),folder_name: str = Form(...)):
    try:
        main_directory = os.path.join("data", user_id)
        folder_directory = os.path.join(main_directory,folder_name) # tmp 아니고 인자값으로 받게
        text_directory = os.path.join(folder_directory, "text")
        img_directory = os.path.join(folder_directory, "img")

        # Check if the directories exist
        if not os.path.exists(text_directory) or not os.path.exists(img_directory):
            return JSONResponse(status_code=404, content={"message": "Data not found for the specified user."})

        print(text_directory,img_directory)
        # Read text data
        text_file_path = os.path.join(text_directory, "data.txt")
        if os.path.exists(text_file_path):
            with open(text_file_path, 'r',encoding='utf-8') as text_file:
                text_data = text_file.read()
        else:
            text_data = None
        print("finish get text data")
        # Read image data (if exists)
        img_base64 = None
        img_files = os.listdir(img_directory)
        if img_files:
            # Assuming only one image file exists
            image_path = os.path.join(img_directory, img_files[0])
            with open(image_path, "rb") as img_file:
                img_base64 = base64.b64encode(img_file.read()).decode()

        print("finish get image data")

        return JSONResponse(status_code=200, content={"text_data": text_data, "image_base64": img_base64})

    except Exception as e:
        return JSONResponse(status_code=500, content={"message": f"Error: {str(e)}"})





@app.post("/Save_user_data/")
async def Save_user_data(user_id: str = Form(...),folder_name: str = Form(...)):
    try:
        main_directory = os.path.join("data", user_id)
        # 기존의 'tmp' 폴더 경로
        old_folder_path = os.path.join(main_directory, 'tmp')

        # 새로운 폴더 이름으로 변경할 폴더 경로
        new_folder_path = os.path.join(main_directory, folder_name)
        # 'tmp' 폴더를 새로운 이름으로 변경

        os.rename(old_folder_path, new_folder_path)

        # 변경된 폴더 경로를 반환하거나 성공 상태를 클라이언트에게 반환할 수 있습니다.
        return JSONResponse(status_code=200, content={"message":"save finish"})

    except Exception as e:
        return JSONResponse(status_code=500, content={"message": f"Error: {str(e)}"})


if __name__ == "__main__":
    import uvicorn

    # uvicorn을 사용하여 FastAPI 서버 실행
    uvicorn.run(app, host="*********", port=8000)

