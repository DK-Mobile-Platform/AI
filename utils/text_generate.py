import urllib3
import json
import base64
import os
from openai import OpenAI
import re
openApiURL = "http://aiopen.etri.re.kr:8000/WiseASR/Recognition"
accessKey = "e10d8f6a-3f5e-487c-8a87-01d2384e9b25"
api_key="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"

 # path : data path to save , languagecode("korean") : language for translate

def text_generate(folder_path,languagecode):
    # 해당 폴더 내의 파일 목록을 불러옵니다.
    # file_list = os.listdir(folder_path)
    # languageCode = languagecode
    # result_txt=''
    # for file in file_list:
    #     print("file name",file)
    #
    #     audioFilePath= os.path.join(folder_path,str(file))
    #     file = open(audioFilePath, "rb")
    #     audioContents = base64.b64encode(file.read()).decode("utf8")
    #     file.close()
    #
    #     requestJson = {
    #         "argument": {
    #             "language_code": languageCode,
    #             "audio": audioContents
    #         }
    #     }
    #
    #
    #     http = urllib3.PoolManager()
    #     response = http.request(
    #         "POST",
    #         openApiURL,
    #         headers={"Content-Type": "application/json; charset=UTF-8", "Authorization": accessKey},
    #         body=json.dumps(requestJson)
    #     )
    #
    #
    #     result = str(response.data, "utf-8")
    #     print(result)
    #
    #     parsed_data = json.loads(result)
    #     recognized_value = parsed_data.get("return_object", {}).get("recognized", "")
    #
    #     print(recognized_value)
    #
    #
    #     result_txt+=' '
    #     result_txt+=recognized_value
    result_txt = ''
    file_list = sorted(os.listdir(folder_path), key=lambda x: int(re.findall(r'\d+', x)[0]))
    for file in file_list:
        client = OpenAI(api_key=api_key)
        print("file name",file)

        audio_file = open(os.path.join(folder_path,file), "rb")
        transcription = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file
        )
        print(transcription.text)
        result_txt+=transcription.text
    return result_txt

    # # 파일 경로 설정
    # output_file_path = output_file_path+"/output.txt" # "output.txt"

    # # result_txt에 저장된 값을 텍스트 파일에 씁니다.
    # with open(output_file_path, "w", encoding="utf-8") as output_file:
    #     for recognized_value in result_txt:
    #         output_file.write(recognized_value + "\n")
