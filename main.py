import utils.text_generate as text_generate
import utils.summarize as summarize
from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.responses import JSONResponse
from pydub import AudioSegment
app = FastAPI()
from utils.voice_preprocessing import split_audio
import base64
import os
from datetime import datetime
import shutil
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
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            print(f"Directory '{folder_path}' created.")
        else:
            print(f"Directory '{folder_path}' already exists.")


        #save text voice_text to text_path 'data.txt'
        with open(os.path.join(folder_path,'data.txt'), 'w', encoding='utf-8') as file:
            file.write(voice_text)

        summarize_text,img_base64=summarize.summarize(voice_text,folder_path)

        print("summarize finish")
        with open(os.path.join(folder_path,'summarize.txt'), 'w', encoding='utf-8') as file:
            file.write(summarize_text)

        # Return both the summary and the image as a JSON response
        return JSONResponse(content={"summarize_text": summarize_text,"image": img_base64})



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
        main_directory = os.path.join("data", user_id)

        if not os.path.exists(main_directory):
            os.makedirs(main_directory)

        folder_path = os.path.join(main_directory,"기본폴더")
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        return JSONResponse(status_code=200, content={"message": "Directories created successfully."})

    except Exception as e:
        return JSONResponse(status_code=500, content={"message": f"Error: {str(e)}"})



@app.post("/Get_User_text_data/home")
async def Get_User_text_data_text(user_id: str = Form(...),folder_name: str = Form(...),date: str = Form(...),file_name: str = Form(...)):
    try:
        main_directory = os.path.join("data", user_id)
        folder_directory = os.path.join(main_directory,folder_name) # tmp 아니고 인자값으로 받게
        date_directory = os.path.join(folder_directory, date)  # tmp 아니고 인자값으로 받게
        file_directory = os.path.join(date_directory, file_name)

        text_file_path = os.path.join(file_directory, "data.txt")
        if os.path.exists(text_file_path):
            with open(text_file_path, 'r',encoding='utf-8') as text_file:
                text_data = text_file.read()
        else:
            text_data = None
        print("finish get text data")
        return JSONResponse(status_code=200, content={"text_data": text_data})

    except Exception as e:
        return JSONResponse(status_code=500, content={"message": f"Error: {str(e)}"})

@app.post("/Get_User_text_data/folder")
async def Get_User_text_data_folder(user_id: str = Form(...),folder_name: str = Form(...),date: str = Form(...),file_name: str = Form(...)):
    try:
        main_directory = os.path.join("data", user_id)
        folder_directory = os.path.join(main_directory,folder_name) # tmp 아니고 인자값으로 받게
        date_directory = os.path.join(folder_directory, date)  # tmp 아니고 인자값으로 받게
        file_directory = os.path.join(date_directory, file_name)

        text_file_path = os.path.join(file_directory, "summarize.txt")
        if os.path.exists(text_file_path):
            with open(text_file_path, 'r',encoding='utf-8') as text_file:
                text_data = text_file.read()
        else:
            text_data = None
        print("finish get text data")

        img_directory = os.path.join(file_directory, "image.png")

        with open(img_directory, "rb") as img_file:
            img_base64 = base64.b64encode(img_file.read()).decode()


        return JSONResponse(status_code=200, content={"text_data": text_data, "image":img_base64})

    except Exception as e:
        return JSONResponse(status_code=500, content={"message": f"Error: {str(e)}"})



@app.post("/Save_user_data/")
async def Save_user_data(user_id: str = Form(...),folder_name: str = Form(...),file_name: str = Form(...)):
    try:
        main_directory = os.path.join("data", user_id) # data/user_id
        # 기존의 'tmp' 폴더 경로
        old_folder_path = os.path.join(main_directory, 'tmp') #data/user_id/tmp

        folder_name= os.path.join(main_directory,folder_name) #data/user_id/foler_name
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)

        now = datetime.now()
        date_str = now.strftime("%Y-%m-%d")
        new_date_folder_path = os.path.join(folder_name,date_str) # data/user_id/foler_name/yymmdd
        if not os.path.exists(new_date_folder_path):
            os.makedirs(new_date_folder_path)
        new_file_folder_path = os.path.join(new_date_folder_path,file_name) # data/user_id/foler_name/yymmdd/file_name
        if not os.path.exists(new_file_folder_path):
            os.makedirs(new_file_folder_path)


        for filename in os.listdir(old_folder_path):
            old_file_path = os.path.join(old_folder_path, filename)
            new_file_path = os.path.join(new_file_folder_path, filename)
            if os.path.isfile(old_file_path):
                shutil.move(old_file_path, new_file_path)








        # 변경된 폴더 경로를 반환하거나 성공 상태를 클라이언트에게 반환할 수 있습니다.
        return JSONResponse(status_code=200, content={"message":"save finish"})

    except Exception as e:
        return JSONResponse(status_code=500, content={"message": f"Error: {str(e)}"})


if __name__ == "__main__":
    import uvicorn

    # uvicorn을 사용하여 FastAPI 서버 실행

    uvicorn.run(app, host="", port=8000)

