# AI

# 데이터
1. [한국어 대학강의](https://aihub.or.kr/aihubdata/data/view.do?currMenu=115&topMenu=100&aihubDataSe=data&dataSetSn=71627)
2. [문서요약 텍스트](https://aihub.or.kr/aihubdata/data/view.do?currMenu=115&topMenu=100&aihubDataSe=realm&dataSetSn=97)

# 모델(요약)
1. [korean text kobart-news](https://huggingface.co/ainize/kobart-news)
2. [korean stt git](https://github.com/topics/korean-stt)
3. 
# APIs
1. [무료 api 음성인식](https://aiopen.etri.re.kr/guide/Recognition)
```python
  import urllib3
  import json
  import base64
  openApiURL = "http://aiopen.etri.re.kr:8000/WiseASR/Recognition"
  accessKey = "e10d8f6a-3f5e-487c-8a87-01d2384e9b25"
  audioFilePath = "/content/U00099.wav"
  
  languageCode = "korean"
   
  file = open(audioFilePath, "rb")
  audioContents = base64.b64encode(file.read()).decode("utf8")
  file.close()
   
  requestJson = {    
      "argument": {
          "language_code": languageCode,
          "audio": audioContents
      }
  }
   
  http = urllib3.PoolManager()
  response = http.request(
      "POST",
      openApiURL,
      headers={"Content-Type": "application/json; charset=UTF-8","Authorization": accessKey},
      body=json.dumps(requestJson)
  )
   
  print("[responseCode] " + str(response.status))
  print("[responBody]")
  print(str(response.data,"utf-8"))
```
1. 
