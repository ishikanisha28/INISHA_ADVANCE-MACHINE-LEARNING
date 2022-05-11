# -*- coding: utf-8 -*-
"""FINAL20.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1oWk28BkzvE0N_MELAK6TQrVboa6nlloY

INSTALLING TRANSFORMER
"""

!pip install --upgrade transformers sentencepiece

"""INSTALLING SPACY AND SPACY TRANSFORMERS"""

!pip install https://github.com/explosion/spacy-models/releases/download/en_core_web_trf-3.2.0/en_core_web_trf-3.2.0-py3-none-any.whl

"""INSTALLING EN_CORE_WEB_SM FOR ENGLISH MODEL PIPLINE OPTIMIZE FOR CPU"""

!python -m spacy download en_core_web_sm

"""IMPORT SPACY"""

import spacy
from transformers import *

# sample text from Wikipedia
text = """Rabindranath Tagore FRAS (Bengali: রবীন্দ্রনাথ ঠাকুর, /rəˈbɪndrənɑːt tæˈɡɔːr/ (listen); 7 May 1861 – 7 August 1941) was a Bengali polymath who worked as a poet, writer, playwright, composer, philosopher, social reformer and painter. He reshaped Bengali literature and music as well as Indian art with Contextual Modernism in the late 19th and early 20th centuries. Author of the "profoundly sensitive, fresh and beautiful" poetry of Gitanjali, he became in 1913 the first non-European and the first lyricist to win the Nobel Prize in Literature. Tagore's poetic songs were viewed as spiritual and mercurial; however, his "elegant prose and magical poetry" remain largely unknown outside Bengal. He was a fellow of the Royal Asiatic Society. Referred to as "the Bard of Bengal", Tagore was known by sobriquets: Gurudev, Kobiguru, Biswakobi.[a]

A Bengali Brahmin from Calcutta with ancestral gentry roots in Burdwan district[9] and Jessore, Tagore wrote poetry as an eight-year-old. At the age of sixteen, he released his first substantial poems under the pseudonym Bhānusiṃha ("Sun Lion"), which were seized upon by literary authorities as long-lost classics. By 1877 he graduated to his first short stories and dramas, published under his real name. As a humanist, universalist, internationalist, and ardent anti-nationalist, he denounced the British Raj and advocated independence from Britain. As an exponent of the Bengal Renaissance, he advanced a vast canon that comprised paintings, sketches and doodles, hundreds of texts, and some two thousand songs; his legacy also endures in his founding of Visva-Bharati University."""

"""USING NER PIPELINE FOR CALLING THE MODEL"""

# load BERT model fine-tuned for Named Entity Recognition (NER)
ner = pipeline("ner", model="dslim/bert-base-NER")

"""EXTRACTING ENTITIES FROM TEXT"""

# perform inference on the transformer model
doc_ner = ner(text)
# print the output
doc_ner

"""Next, let's make a function that uses spaCy to visualize this Python dictionary:


"""

def get_entities_html(text, ner_result, title=None):
  """Visualize NER with the help of SpaCy"""
  ents = []
  for ent in ner_result:
    e = {}
    # add the start and end positions of the entity
    e["start"] = ent["start"]
    e["end"] = ent["end"]
    # add the score if you want in the label
    # e["label"] = f"{ent["entity"]}-{ent['score']:.2f}"
    e["label"] = ent["entity"]
    if ents and -1 <= ent["start"] - ents[-1]["end"] <= 1 and ents[-1]["label"] == e["label"]:
      # if the current entity is shared with previous entity
      # simply extend the entity end position instead of adding a new one
      ents[-1]["end"] = e["end"]
      continue
    ents.append(e)
  # construct data required for displacy.render() method
  render_data = [
    {
      "text": text,
      "ents": ents,
      "title": title,
    }
  ]
  spacy.displacy.render(render_data, style="ent", manual=True, jupyter=True)

# get HTML representation of NER of our text
get_entities_html(text, doc_ner)

"""O: Outside of a named entity. B-MIS: Beginning of a miscellaneous entity right after another miscellaneous entity. I-MIS: Miscellaneous entity. B-PER: Beginning of a person’s name right after another person’s name. I-PER: Person’s name. B-ORG: The beginning of an organization right after another organization. I-ORG: Organization. B-LOC: Beginning of a location right after another location. I-LOC: Location.

INSTALLING ROBERTA A BETTER MODEL TO CHECK
"""

# load roberta-large model
ner2 = pipeline("ner", model="xlm-roberta-large-finetuned-conll03-english")

# perform inference on this model
doc_ner2 = ner2(text)

# get HTML representation of NER of our text
get_entities_html(text, doc_ner2)

"""As you can see, now it's improved, naming Rabindranath Tagore as a single entity and also the district Jessore.


"""

#There are a lot of other models that were fine-tuned on the same dataset. Here's yet another one:

# load yet another roberta-large model
ner3 = pipeline("ner", model="Jean-Baptiste/roberta-large-ner-english")
# perform inference on this model
doc_ner3 = ner3(text)
# get HTML representation of NER of our text
get_entities_html(text, doc_ner3)

"""This model, however, only has PER, MISC, LOC, and ORG entities. SpaCy automatically colors the familiar entities.

To perform NER using SpaCy, we must first load the model using spacy.load() function:
"""

# load the English CPU-optimized pipeline
nlp = spacy.load("en_core_web_sm")

#We're loading the model we've downloaded. Make sure you download the model you want to use before loading it here. Next, let's generate our document:

# predict the entities
doc = nlp(text)

# display the doc with jupyter mode
spacy.displacy.render(doc, style="ent", jupyter=True)

"""This one looks much better, and there are a lot more entities (18) than the previous ones, namely CARDINAL, DATE, EVENT, FAC, GPE, LANGUAGE, LAW, LOC, MONEY, NORP, ORDINAL, ORG, PERCENT, PERSON, PRODUCT, QUANTITY, TIME, WORK_OF_ART


"""

#However, Calcutta was mistakenly labeled as an product, so let's use the Transformer model that spaCy is offering:

# load the English transformer pipeline (roberta-base) using spaCy
nlp_trf = spacy.load('en_core_web_trf')

#Let's perform inference and visualize the text:

# perform inference on the model
doc_trf = nlp_trf(text)
# display the doc with jupyter mode
spacy.displacy.render(doc_trf, style="ent", jupyter=True)

"""TRANSFORMERS"""

!pip install transformers
!pip install torch

from transformers import BertForQuestionAnswering
from transformers import BertTokenizer
import torch
import numpy as np

#Step 3: Load pre-trained Bert model
model = BertForQuestionAnswering.from_pretrained('bert-large-uncased-whole-word-masking-finetuned-squad')

tokenizer_for_bert = BertTokenizer.from_pretrained('bert-large-uncased-whole-word-masking-finetuned-squad')

def bert_question_answer(question, passage, max_len=500):
    
    """
    question: What is the name of YouTube Channel
    passage: Watch complete playlist of Natural Language Processing. Don't forget to like, share and subscribe my channel IG Tech Team
    """

    #Tokenize input question and passage 
    #Add special tokens - [CLS] and [SEP]
    input_ids = tokenizer_for_bert.encode (question, passage,  max_length= max_len, truncation=True)  
    """
    [101, 2054, 2003, 1996, 2171, 1997, 7858, 3149, 102, 3422, 3143, 2377, 9863, 1997, 3019, 2653, 6364, 1012, 
    2123, 1005, 1056, 5293, 2000, 2066, 1010, 3745, 1998, 4942, 29234, 2026, 3149, 1045, 2290, 6627, 2136, 102]
    """

    #Getting number of tokens in 1st sentence (question) and 2nd sentence (passage that contains answer)
    sep_index = input_ids.index(102) 
    len_question = sep_index + 1   
    len_passage = len(input_ids)- len_question  
    """
    8
    9
    27
    """
    #Need to separate question and passage
    #Segment ids will be 0 for question and 1 for passage
    segment_ids =  [0]*len_question + [1]*(len_passage)  
    """
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    """

    #Converting token ids to tokens
    tokens = tokenizer_for_bert.convert_ids_to_tokens(input_ids) 
    """
    tokens = ['[CLS]', 'what', 'is', 'the', 'name', 'of', 'youtube', 'channel', '[SEP]', 'watch', 'complete', 
    'play', '##list', 'of', 'natural', 'language', 'processing', '.', 'don', "'", 't', 'forget', 'to', 'like', 
    ',', 'share', 'and', 'sub', '##scribe', 'my', 'channel', 'i', '##g', 'tech', 'team', '[SEP]']
    """

    #Getting start and end scores for answer
    #Converting input arrays to torch tensors before passing to the model
    start_token_scores = model(torch.tensor([input_ids]), token_type_ids=torch.tensor([segment_ids]) )[0]
    end_token_scores = model(torch.tensor([input_ids]), token_type_ids=torch.tensor([segment_ids]) )[1]
    """
    tensor([[-5.9787, -3.0541, -7.7166, -5.9291, -6.8790, -7.2380, -1.8289, -8.1006,
         -5.9786, -3.9319, -5.6230, -4.1919, -7.2068, -6.7739, -2.3960, -5.9425,
         -5.6828, -8.7007, -4.2650, -8.0987, -8.0837, -7.1799, -7.7863, -5.1605,
         -8.2832, -5.1088, -8.1051, -5.3985, -6.7129, -1.4109, -3.2241,  1.5863,
         -4.9714, -4.1138, -5.9107, -5.9786]], grad_fn=<SqueezeBackward1>)
    tensor([[-2.1025, -2.9121, -5.9192, -6.7459, -6.4667, -5.6418, -1.4504, -3.1943,
         -2.1024, -5.7470, -6.3381, -5.8520, -3.4871, -6.7667, -5.4711, -3.9885,
         -1.2502, -4.0869, -6.4930, -6.3751, -6.1309, -6.9721, -7.5558, -6.4056,
         -6.7456, -5.0527, -7.3854, -7.0440, -4.3720, -3.8936, -2.1085, -5.8211,
         -2.0906, -2.2184,  1.4268, -2.1026]], grad_fn=<SqueezeBackward1>)
    """

    #Converting scores tensors to numpy arrays
    start_token_scores = start_token_scores.detach().numpy().flatten()
    end_token_scores = end_token_scores.detach().numpy().flatten()
    """
    [-5.978666  -3.0541189 -7.7166095 -5.929051  -6.878973  -7.238004
    -1.8289301 -8.10058   -5.9786286 -3.9319289 -5.6229596 -4.191908
    -7.20684   -6.773916  -2.3959794 -5.942456  -5.6827617 -8.700695
    -4.265001  -8.09874   -8.083673  -7.179875  -7.7863474 -5.16046
    -8.283156  -5.108819  -8.1051235 -5.3984528 -6.7128663 -1.4108785
    -3.2240815  1.5863497 -4.9714    -4.113782  -5.9107194 -5.9786243]

    [-2.1025064 -2.912148  -5.9192414 -6.745929  -6.466673  -5.641759
    -1.4504088 -3.1943028 -2.1024144 -5.747039  -6.3380575 -5.852047
    -3.487066  -6.7667046 -5.471078  -3.9884708 -1.2501552 -4.0868535
    -6.4929943 -6.375147  -6.130891  -6.972091  -7.5557766 -6.405638
    -6.7455807 -5.0527067 -7.3854156 -7.043977  -4.37199   -3.8935976
    -2.1084964 -5.8210607 -2.0906193 -2.2184045  1.4268283 -2.1025767]
    """
    #Getting start and end index of answer based on highest scores
    answer_start_index = np.argmax(start_token_scores)
    answer_end_index = np.argmax(end_token_scores)
    """
    31
    34
    """

    #Getting scores for start and end token of the answer
    start_token_score = np.round(start_token_scores[answer_start_index], 2)
    end_token_score = np.round(end_token_scores[answer_end_index], 2)
    """
    1.59
    1.43
    """

    #Combining subwords starting with ## and get full words in output. 
    #It is because tokenizer breaks words which are not in its vocab.
    answer = tokens[answer_start_index] 
    for i in range(answer_start_index + 1, answer_end_index + 1):
        if tokens[i][0:2] == '##':  
            answer += tokens[i][2:] 
        else:
            answer += ' ' + tokens[i]  
# If the answer didn't find in the passage
    if ( answer_start_index == 0) or (start_token_score < 0 ) or  (answer == '[SEP]') or ( answer_end_index <  answer_start_index):
        answer = "Sorry!, I could not find an answer in the passage."
    
    return (answer_start_index, answer_end_index, start_token_score, end_token_score,  answer)

#Testing function
bert_question_answer("What is the name of YouTube Channel", "Watch complete playlist of Natural Language Processing. Don't forget to like, share and subscribe my channel IG Tech Team ")



def bert_question_answer(question, passage, max_len=500):
    
    """
    question: What is the name of YouTube Channel
    passage: Watch complete playlist of Ishika Nisha. Don't forget to like, share and subscribe my channel IN Tech Team
    """
    #Tokenize input question and passage 
    #Add special tokens - [CLS] and [SEP]
    input_ids = tokenizer_for_bert.encode (question, passage,  max_length= max_len, truncation=True)  
    """
    [101, 2054, 2003, 1996, 2171, 1997, 7858, 3149, 102, 3422, 3143, 2377, 9863, 1997, 3019, 2653, 6364, 1012, 
    2123, 1005, 1056, 5293, 2000, 2066, 1010, 3745, 1998, 4942, 29234, 2026, 3149, 1045, 2290, 6627, 2136, 102]
    """
    #Getting number of tokens in 1st sentence (question) and 2nd sentence (passage that contains answer)
    sep_index = input_ids.index(102) 
    len_question = sep_index + 1   
    len_passage = len(input_ids)- len_question  
    """
    8
    93
    27
    """
    #Need to separate question and passage
    #Segment ids will be 0 for question and 1 for passage
    segment_ids =  [0]*len_question + [1]*(len_passage)  
    """
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    """
    #Converting token ids to tokens
    tokens = tokenizer_for_bert.convert_ids_to_tokens(input_ids) 
    """
    tokens = ['[CLS]', 'what', 'is', 'the', 'name', 'of', 'youtube', 'channel', '[SEP]', 'watch', 'complete', 
    'play', '##list', 'of', 'ishika', 'nisha', '.', 'don', "'", 't', 'forget', 'to', 'like', 
    ',', 'share', 'and', 'sub', '##scribe', 'my', 'channel', 'i', '##n', 'tech', 'team', '[SEP]']
    """
    #Getting start and end scores for answer
    #Converting input arrays to torch tensors before passing to the model
    start_token_scores = model(torch.tensor([input_ids]), token_type_ids=torch.tensor([segment_ids]) )[0]
    end_token_scores = model(torch.tensor([input_ids]), token_type_ids=torch.tensor([segment_ids]) )[1]
    """
    tensor([[-5.9787, -3.0541, -7.7166, -5.9291, -6.8790, -7.2380, -1.8289, -8.1006,
         -5.9786, -3.9319, -5.6230, -4.1919, -7.2068, -6.7739, -2.3960, -5.9425,
         -5.6828, -8.7007, -4.2650, -8.0987, -8.0837, -7.1799, -7.7863, -5.1605,
         -8.2832, -5.1088, -8.1051, -5.3985, -6.7129, -1.4109, -3.2241,  1.5863,
         -4.9714, -4.1138, -5.9107, -5.9786]], grad_fn=<SqueezeBackward1>)
    tensor([[-2.1025, -2.9121, -5.9192, -6.7459, -6.4667, -5.6418, -1.4504, -3.1943,
         -2.1024, -5.7470, -6.3381, -5.8520, -3.4871, -6.7667, -5.4711, -3.9885,
         -1.2502, -4.0869, -6.4930, -6.3751, -6.1309, -6.9721, -7.5558, -6.4056,
         -6.7456, -5.0527, -7.3854, -7.0440, -4.3720, -3.8936, -2.1085, -5.8211,
         -2.0906, -2.2184,  1.4268, -2.1026]], grad_fn=<SqueezeBackward1>)
    """
    #Converting scores tensors to numpy arrays
    start_token_scores = start_token_scores.detach().numpy().flatten()
    end_token_scores = end_token_scores.detach().numpy().flatten()
    """
    [-5.978666  -3.0541189 -7.7166095 -5.929051  -6.878973  -7.238004
    -1.8289301 -8.10058   -5.9786286 -3.9319289 -5.6229596 -4.191908
    -7.20684   -6.773916  -2.3959794 -5.942456  -5.6827617 -8.700695
    -4.265001  -8.09874   -8.083673  -7.179875  -7.7863474 -5.16046
    -8.283156  -5.108819  -8.1051235 -5.3984528 -6.7128663 -1.4108785
    -3.2240815  1.5863497 -4.9714    -4.113782  -5.9107194 -5.9786243]

    [-2.1025064 -2.912148  -5.9192414 -6.745929  -6.466673  -5.641759
    -1.4504088 -3.1943028 -2.1024144 -5.747039  -6.3380575 -5.852047
    -3.487066  -6.7667046 -5.471078  -3.9884708 -1.2501552 -4.0868535
    -6.4929943 -6.375147  -6.130891  -6.972091  -7.5557766 -6.405638
    -6.7455807 -5.0527067 -7.3854156 -7.043977  -4.37199   -3.8935976
    -2.1084964 -5.8210607 -2.0906193 -2.2184045  1.4268283 -2.1025767]
    """
    #Getting start and end index of answer based on highest scores
    answer_start_index = np.argmax(start_token_scores)
    answer_end_index = np.argmax(end_token_scores)
    """
    31
    34
    """

    #Getting scores for start and end token of the answer
    start_token_score = np.round(start_token_scores[answer_start_index], 2)
    end_token_score = np.round(end_token_scores[answer_end_index], 2)
    """
    1.59
    1.43
    """

    #Combining subwords starting with ## and get full words in output. 
    #It is because tokenizer breaks words which are not in its vocab.
    answer = tokens[answer_start_index] 
    for i in range(answer_start_index + 1, answer_end_index + 1):
        if tokens[i][0:2] == '##':  
            answer += tokens[i][2:] 
        else:
            answer += ' ' + tokens[i]  
    # If the answer didn't find in the passage
    if ( answer_start_index == 0) or (start_token_score < 0 ) or  (answer == '[SEP]') or ( answer_end_index <  answer_start_index):
        answer = "Sorry!, I could not find an answer in the passage."
    
    return (answer_start_index, answer_end_index, start_token_score, end_token_score,  answer)

    #Testing function
    bert_question_answer("What is the name of YouTube Channel", "Watch complete playlist of Ishika Nisha. Don't forget to like, share and subscribe my channel IN Tech Team ")

"""(31, 34, 1.59, 1.43, 'in tech team')

"""

!pip install torch

# Let me define another passage
passage= """Rabindranath Tagore FRAS (Bengali: রবীন্দ্রনাথ ঠাকুর, /rəˈbɪndrənɑːt tæˈɡɔːr/ (listen); 7 May 1861 – 7 August 1941) was a Bengali polymath who worked as a poet, writer, playwright, composer, philosopher, social reformer and painter. He reshaped Bengali literature and music as well as Indian art with Contextual Modernism in the late 19th and early 20th centuries. Author of the "profoundly sensitive, fresh and beautiful" poetry of Gitanjali, he became in 1913 the first non-European and the first lyricist to win the Nobel Prize in Literature. Tagore's poetic songs were viewed as spiritual and mercurial; however, his "elegant prose and magical poetry" remain largely unknown outside Bengal. He was a fellow of the Royal Asiatic Society. Referred to as "the Bard of Bengal", Tagore was known by sobriquets: Gurudev, Kobiguru, Biswakobi.[a]

A Bengali Brahmin from Calcutta with ancestral gentry roots in Burdwan district[9] and Jessore, Tagore wrote poetry as an eight-year-old. At the age of sixteen, he released his first substantial poems under the pseudonym Bhānusiṃha ("Sun Lion"), which were seized upon by literary authorities as long-lost classics. By 1877 he graduated to his first short stories and dramas, published under his real name. As a humanist, universalist, internationalist, and ardent anti-nationalist, he denounced the British Raj and advocated independence from Britain. As an exponent of the Bengal Renaissance, he advanced a vast canon that comprised paintings, sketches and doodles, hundreds of texts, and some two thousand songs; his legacy also endures in his founding of Visva-Bharati University."""

print (f'Length of the passage: {len(passage.split())} words')

question ="Who is Rabindranath Tagore"
print ('\nQuestion 1:\n', question)
_, _ , _ , _, ans  = bert_question_answer( question, passage)
print('\nAnswer from BERT: ', ans ,  '\n')



question ="When was Rabindranath Tagore born"
print ('\nQuestion 7:\n', question)
_, _ , _ , _, ans  = bert_question_answer( question, passage)
print('\nAnswer from BERT: ', ans ,  '\n')

# Let me define one passage
passage = """Hello, I am Ishika. My friend name is Sakshi. He is the son of Pradip. I spend most of the time with Sakshi. 
He always call me by my nick name. Sakshi call me programmer. Except Sakshi, my other friend call me by my original name. 
Amrita is also my friend. """

print (f'Length of the passage: {len(passage.split())} words')

question1 ="What is my name" 
print ('\nQuestion 1:\n', question1)
_, _ , _ , _, ans  = bert_question_answer( question1, passage)
print('\nAnswer from BERT: ', ans ,  '\n')


question2 ="Who is the father of Sakshi"
print ('\nQuestion 2:\n', question2)
_, _ , _ , _, ans  = bert_question_answer( question2, passage)
print('\nAnswer from BERT: ', ans ,  '\n')

question3 ="With whom Ishika spend most of the time" 
print ('\nQuestion 3:\n', question3)
_, _ , _ , _, ans  = bert_question_answer( question3, passage)
print('\nAnswer from BERT: ', ans ,  '\n')

#@title Question-Answering Application { vertical-output: true }
#@markdown ---
question= "name of the sons of Rabindranath Tagore" #@param {type:"string"}
3
passage = """Rabindranath Tagore FRAS (Bengali: রবীন্দ্রনাথ ঠাকুর, /rəˈbɪndrənɑːt tæˈɡɔːr/ (listen); 7 May 1861 – 7 August 1941) was a Bengali polymath who worked as a poet, writer, playwright, composer, philosopher, social reformer and painter. He reshaped Bengali literature and music as well as Indian art with Contextual Modernism in the late 19th and early 20th centuries. Author of the "profoundly sensitive, fresh and beautiful" poetry of Gitanjali, he became in 1913 the first non-European and the first lyricist to win the Nobel Prize in Literature. Tagore's poetic songs were viewed as spiritual and mercurial; however, his "elegant prose and magical poetry" remain largely unknown outside Bengal. He was a fellow of the Royal Asiatic Society. Referred to as "the Bard of Bengal", Tagore was known by sobriquets: Gurudev, Kobiguru, Biswakobi.[a]

A Bengali Brahmin from Calcutta with ancestral gentry roots in Burdwan district[9] and Jessore, Tagore wrote poetry as an eight-year-old. At the age of sixteen, he released his first substantial poems under the pseudonym Bhānusiṃha ("Sun Lion"), which were seized upon by literary authorities as long-lost classics. By 1877 he graduated to his first short stories and dramas, published under his real name. As a humanist, universalist, internationalist, and ardent anti-nationalist, he denounced the British Raj and advocated independence from Britain. As an exponent of the Bengal Renaissance, he advanced a vast canon that comprised paintings, sketches and doodles, hundreds of texts, and some two thousand songs; his legacy also endures in his founding of Visva-Bharati University."""

#@markdown ---
_, _ , _ , _, ans  = bert_question_answer( question, passage)

#@markdown Answer:
print(ans)

#@title Question-Answering Application { vertical-output: true }
#@markdown ---
question= "who is Albert Einstein" #@param {type:"string"}
3
passage = """Albert Einstein was a German-born theoretical physicist, widely acknowledged to be one of the greatest and most influential physicists of all time. Einstein is best known for developing the theory of relativity, but he also made important contributions to the development of the theory of quantum mechanics. Wikipedia"""
#@markdown ---
_, _ , _ , _, ans  = bert_question_answer( question, passage)

#@markdown Answer:
print(ans)