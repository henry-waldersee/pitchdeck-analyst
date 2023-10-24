
#Installing the libraries we need (PyPDF2 and Langchain):

!pip install openai langchain
!pip install PyPDF2
import PyPDF2
import os
from langchain import OpenAI #or any model!
from langchain import PromptTemplate

#Enter your OpenAI API (!!! Add your own API Key !!!):

openai_api_key = 'your_openAI_API_key'
###you can find this on: https://platform.openai.com/account/api-keys
###Make sure that you have an OpenAI account in order to have access to your own API key

import os
os.environ["OPENAI_API_KEY"] = openai_api_key


#Define (extract_pdf_text and clean_pdf_text)

def extract_pdf_text(pdf: str):
    
    #PyPDF2 can extract text from PDFs and in this case add it to a list
    #We need to open the pdf file in binary, not as a text hence open(pdf, 'rb')
    #https://github.com/federicoazzu/pdf_to_text/blob/master/main.py
    
    with open(pdf, 'rb') as pdf: # Open the PDF file of your choice
        reader = PyPDF2.PdfReader(pdf, strict=False)
        pdf_text = []

        for page in reader.pages:
          content = page.extract_text()
          pdf_text.append(content)

        return pdf_text

def clean_pdf_text(pdf):
    
    #This function simply uses the extract_pdf_text and cleans up the text.
    #You can clean this text in any way you want.
    pdf = str(pdf) #making sure the input is a string
    extracted_text = extract_pdf_text(pdf)
    clean_pdf_text = ",".join(str(element) for element in extracted_text)
    clean_pdf_text = clean_pdf_text.replace('\n', '')
    return clean_pdf_text


#Define variables for prompt

llm = OpenAI() #you can obviously set this to any llm you want, howeve make sure you import the right model from Langchain above
pdf_text = clean_pdf_text('sample.pdf')
investor_focus = 'biotech'


#Creating a prompt template with Langchain


template = """\
I will give you a text exported from a pdf. It might not be clean data.
It is the text extracted from a pitch deck.
You will briefly tell me what the start-up does and
if it is a suitable investment for me, a VC who only invests in {focus}
the text from the pitch deck is {pitchtext}
"""

prompt = PromptTemplate.from_template(template)

#Setting up the prompt and running it through OpenAI with Langchain


prompt = prompt.format(focus= investor_focus,pitchtext = pdf_text)

print(llm(prompt))
