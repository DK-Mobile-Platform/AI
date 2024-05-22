from transformers import PreTrainedTokenizerFast, BartForConditionalGeneration,AutoTokenizer
# tokenizer = PreTrainedTokenizerFast.from_pretrained("ainize/kobart-news")
# model = BartForConditionalGeneration.from_pretrained("ainize/kobart-news")
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from matplotlib import rc
import nltk
import io
import base64
from fastapi.responses import JSONResponse
import os
nltk.download('punkt')

model_dir = "lcw99/t5-base-korean-text-summary"
tokenizer = AutoTokenizer.from_pretrained(model_dir)
model = AutoModelForSeq2SeqLM.from_pretrained(model_dir)

def summarize(text,image_path):
    try:


        # input_ids = tokenizer.encode(text, return_tensors="pt")
        # # Generate Summary Text Ids
        # summary_text_ids = model.generate(
        #     input_ids=input_ids,
        #     bos_token_id=model.config.bos_token_id,
        #     eos_token_id=model.config.eos_token_id,
        #     length_penalty=2.0,
        #     max_length=142,
        #     min_length=56,
        #     num_beams=4,
        # )
        # # Decoding Text
        # decoding_text=tokenizer.decode(summary_text_ids[0], skip_special_tokens=True)
        # print("요약 : ")
        # print(decoding_text)



        max_input_length = 512



        inputs = ["summarize: " + text]

        inputs = tokenizer(inputs, max_length=max_input_length, truncation=True, return_tensors="pt")
        output = model.generate(**inputs, num_beams=8, do_sample=True, min_length=10, max_length=100)
        decoded_output = tokenizer.batch_decode(output, skip_special_tokens=True)[0]
        predicted_title = nltk.sent_tokenize(decoded_output.strip())[0]

        print("predicted_title",predicted_title)
        #,family="AppleGothic"
        wordcloud_text = WordCloud(width=800, height=400, background_color='white',font_path="C:\Windows\Fonts\H2HDRM.TTF").generate(text)#,font_path='AppleGothic'
        print("draw wordcloud_text")
        img_buffer = io.BytesIO()
        plt.figure(figsize=(10, 5))
        plt.imshow(wordcloud_text, interpolation='bilinear')
        plt.axis('off')
        plt.title('Original Text Word Cloud')
        plt.savefig(os.path.join(image_path,'image.png'), format='png')
        plt.close()
        print("draw plot")

        #img_buffer.seek(0)  # Rewind the buffer to the beginning

        #img_base64 = base64.b64encode(img_buffer.getvalue()).decode('utf-8')


        return predicted_title

    except Exception as e:
        print(e)
        return JSONResponse(status_code=500, content={"message": f"Error: {str(e)}"})


