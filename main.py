import docx2txt
import spacy
from spacy.matcher import Matcher
import re
import pyap

import sys

# load pre-trained model
nlp = spacy.load("en_core_web_sm")


def find_name(text):
    # extract name using NLP
    # https://stackoverflow.com/questions/63682422/how-to-extract-names-from-the-resume-in-python
    nlp_text = nlp(text)

    # First name and Last name are always Proper Nouns
    pattern = [{"POS": "PROPN"}, {"POS": "PROPN"}]

    matcher.add("NAME", [pattern])

    matches = matcher(nlp_text)

    for match_id, start, end in matches:
        span = nlp_text[start:end]
        print(type(span))
        # one of the resumes has father name ..to skip it
        if "Father" in span.text:
            continue
        return span


def find_email(text):
    match = re.search(r"[\w.+-]+@[\w-]+\.[\w.-]+", text)
    return match.group(0)


def address(text):
    # TODO address search not working.Fix it
    # print(text.splitlines())
    lines = text.splitlines()
    for line in lines:
        if re.search("address", line, re.IGNORECASE):
            return line.replace("Address", "")
    return "No Address Provided"
    # m = re.search("Address(.+?)", text)
    # if m:
    # found = m.group(1)
    # return found


def phone_number(text):
    # indian phone number format regular expression
    match = re.search(
        r"((\+*)((0[ -]*)*|((91 )*))((\d{12})+|(\d{10})+))|\d{5}([- ]*)\d{6}", text
    )
    if match:
        return match.group(0)
    return "No Phone number provided"


# initialize matcher with a vocab
matcher = Matcher(nlp.vocab)


def read_and_process_resume(file_path):
    my_text = docx2txt.process(file_path)
    print(f"name: {find_name(my_text)}")
    print(f"email: {find_email(my_text)}")
    print(f"phone: {phone_number(my_text)}")
    print(f"address: {address(my_text)}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("No input file passed")
    else:
        read_and_process_resume(sys.argv[1])
