# AI
# 프로세스

1. Data input (voice)
2. Data preprocessing
3. Data voice to text
4. text summarize



# 데이터
1. [한국어 대학강의](https://aihub.or.kr/aihubdata/data/view.do?currMenu=115&topMenu=100&aihubDataSe=data&dataSetSn=71627)
2. [문서요약 텍스트](https://aihub.or.kr/aihubdata/data/view.do?currMenu=115&topMenu=100&aihubDataSe=realm&dataSetSn=97)

# 모델(요약)
1. [korean text kobart-news](https://huggingface.co/ainize/kobart-news)
2. [korean stt git](https://github.com/topics/korean-stt)
3.  [hugging face(lcw99/t5-base-korean-text-summary)](https://huggingface.co/lcw99/t5-base-korean-text-summary)
4.  [hugging_face(eenzeenee/t5-small-korean-summarization)](https://huggingface.co/eenzeenee/t5-small-korean-summarization)

```python
from transformers import PreTrainedTokenizerFast, BartForConditionalGeneration
#  Load Model and Tokenize
tokenizer = PreTrainedTokenizerFast.from_pretrained("ainize/kobart-news")
model = BartForConditionalGeneration.from_pretrained("ainize/kobart-news")
# Encode Input Text

file_name= 'output.txt'
with open(file_name, "r", encoding="utf-8") as file:
    input_text = file.read()
    print("파일 내용:")
    print(input_text)
input_ids = tokenizer.encode(input_text, return_tensors="pt")
# Generate Summary Text Ids
summary_text_ids = model.generate(
    input_ids=input_ids,
    bos_token_id=model.config.bos_token_id,
    eos_token_id=model.config.eos_token_id,
    length_penalty=2.0,
    max_length=142,
    min_length=56,
    num_beams=4,
)
# Decoding Text
print("요약 : ")
print(tokenizer.decode(summary_text_ids[0], skip_special_tokens=True))



from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import nltk
nltk.download('punkt')

model_dir = "lcw99/t5-base-korean-text-summary"
tokenizer = AutoTokenizer.from_pretrained(model_dir)
model = AutoModelForSeq2SeqLM.from_pretrained(model_dir)

max_input_length = 512

text = input_text

inputs = ["summarize: " + text]

inputs = tokenizer(inputs, max_length=max_input_length, truncation=True, return_tensors="pt")
output = model.generate(**inputs, num_beams=8, do_sample=True, min_length=10, max_length=100)
decoded_output = tokenizer.batch_decode(output, skip_special_tokens=True)[0]
predicted_title = nltk.sent_tokenize(decoded_output.strip())[0]

print(predicted_title)


import nltk
nltk.download('punkt')
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

model = AutoModelForSeq2SeqLM.from_pretrained('eenzeenee/t5-small-korean-summarization')
tokenizer = AutoTokenizer.from_pretrained('eenzeenee/t5-small-korean-summarization')

prefix = "summarize: "
sample = '"'+text+'"'

inputs = [prefix + sample]


inputs = tokenizer(inputs, max_length=512, truncation=True, return_tensors="pt")
output = model.generate(**inputs, num_beams=3, do_sample=True, min_length=10, max_length=64)
decoded_output = tokenizer.batch_decode(output, skip_special_tokens=True)[0]
result = nltk.sent_tokenize(decoded_output.strip())[0]

print('RESULT >>', result)


```

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
2. 
