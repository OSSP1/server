# import pandas as pd
# import torch
from transformers import BartForConditionalGeneration
# from kobart import get_pytorch_kobart_model, get_kobart_tokenizer
# from tqdm import tqdm
# from torchtext.data.metrics import bleu_score
from transformers import AutoTokenizer #, AutoModelForSeq2SeqLM



def remove_duplicate_words(string):
    words = string.split()
    result = []
    for word in words:
        
        if word == "<unk>":
            continue
        
        if len(result) == 0 or word != result[-1]:
            result.append(word)
    return ' '.join(result)


def remove_inner_word(string):
    words = string.split()
    result = []
    for idx in range(0, len(words)-1):
        if words[idx] in words[idx+1]:
            continue
        else:
            result.append(words[idx])
    
    result.append(words[-1])
    
    return ' '.join(result)
    


# tokenizer = get_kobart_tokenizer()
tokenizer = AutoTokenizer.from_pretrained("eunjin/kobart_jeju_translator")


# 표준어 -> 제주어
def s2d(sent):
    print(sent, "표준어 to 제주어")
    model = BartForConditionalGeneration.from_pretrained('/workspace/OSSP1/s2d')
    model.eval()
    model.to('cuda')
    # print('>> model set')
    inputs=tokenizer(sent,return_tensors='pt')
    outputs=model.generate(inputs['input_ids'].to('cuda'), eos_token_id=1, max_length=64, num_beams=5)
    generation =  tokenizer.decode(outputs[0])
    
    cleaned_generation = generation.replace("<usr> ", "").replace("</s>", "").replace("안녕하세요", "안녕허우꽈").replace("엄마", "어멍").replace("아빠", "아방").replace("할머니", "할망")\
    .replace("할아버지", "하르방").replace("<usr>", "")
    
    answer = remove_duplicate_words(cleaned_generation)
    
    answer2 = remove_inner_word(answer)
    
    return answer2

# 제주어 -> 표준어
def d2s(sent):
    print(sent, "제주어 to 표준어")
    model = BartForConditionalGeneration.from_pretrained('/workspace/OSSP1/d2s')
    model.eval()
    model.to('cuda')
    # print('>> model set')
    inputs=tokenizer(sent,return_tensors='pt')  
    outputs=model.generate(inputs['input_ids'].to('cuda'), eos_token_id=1, max_length=64, num_beams=5)
    generation =  tokenizer.decode(outputs[0])
    
    cleaned_generation = generation.replace("<usr> ", "").replace("</s>", "").replace("혼저옵서예", "어서오세요").replace("<usr>", "")
    
    answer = remove_duplicate_words(cleaned_generation)
    
    answer2 = remove_inner_word(answer)
    
    return answer2
    # return cleaned_generation