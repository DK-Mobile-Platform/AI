from transformers import PreTrainedTokenizerFast, BartForConditionalGeneration,AutoTokenizer
tokenizer = PreTrainedTokenizerFast.from_pretrained("ainize/kobart-news")
model = BartForConditionalGeneration.from_pretrained("ainize/kobart-news")

def summarize(text):

    # file_name= 'output.txt'
    # with open(file_name, "r", encoding="utf-8") as file:
    #     input_text = file.read()
    #     print("파일 내용:")
    #     print(input_text)
    input_ids = tokenizer.encode(text, return_tensors="pt")
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
    decoding_text=tokenizer.decode(summary_text_ids[0], skip_special_tokens=True)
    print("요약 : ")
    print(decoding_text)

    return decoding_text
