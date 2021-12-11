import docx2txt
import spacy
from spacy.matcher import Matcher
import re
import pyap

import sys

# load pre-trained model
nlp = spacy.load('en_core_web_sm')

def find_name(text):
    # https://stackoverflow.com/questions/63682422/how-to-extract-names-from-the-resume-in-python
    nlp_text = nlp(text)
    
    # First name and Last name are always Proper Nouns
    pattern = [{'POS': 'PROPN'}, {'POS': 'PROPN'}]
    
    matcher.add('NAME', [pattern])
    
    matches = matcher(nlp_text)
    
    for match_id, start, end in matches :
        span = nlp_text[start:end]
        print(type(span))
        if 'Father' in span.text:
            continue
        return span

def find_email(text):
     match = re.search(r'[\w.+-]+@[\w-]+\.[\w.-]+', text)
     return  match.group(0)

def address(text):
    m = re.search('Address(.+?)', text)
    if m:
        found = m.group(1)
        print(found)

def phone_number(text):
    match = re.search(r'((\+*)((0[ -]*)*|((91 )*))((\d{12})+|(\d{10})+))|\d{5}([- ]*)\d{6}', text)
    return  match.group(0)


# initialize matcher with a vocab
matcher = Matcher(nlp.vocab)

def read_and_process_resume(file_path):
    my_text = docx2txt.process(file_path)
    print(f'name: {find_name(my_text)}')
    print(f'email: {find_email(my_text)}')
    print(f'phone: {phone_number(my_text)}')
    print(f'address: {address(my_text)}')
    

if __name__ == "__main__":
    if len(sys.argv) < 1:
        print('No input file passed')
    read_and_process_resume(sys.argv[1])


