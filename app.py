import os
from dotenv import load_dotenv
import streamlit as st
from langchain.prompts import PromptTemplate
from langchain_huggingface import HuggingFaceEndpoint

# Load .env file for HuggingFace Token
load_dotenv()
os.environ['HF_TOKEN']=os.getenv("HF_TOKEN")

## Function To get response from Model

def getLLamaresponse(input_text,no_words,blog_style):

    ### Model
    repo_id = "mistralai/Mistral-7B-Instruct-v0.3"

    llm = HuggingFaceEndpoint(
        repo_id=repo_id, 
        huggingfacehub_api_token=os.environ["HF_TOKEN"],
        temperature=0.01,
        max_new_tokens=256
    )
    
    ## Prompt Template

    template="""
        Write a blog for {blog_style} job profile for a topic {input_text}
        within {no_words} words.
            """
    
    prompt=PromptTemplate(input_variables=["blog_style","input_text",'no_words'],
                          template=template)
    
    ## Generate the ressponse from the Model

    formatted_prompt = prompt.format(
        blog_style=blog_style,
        input_text=input_text,
        no_words=no_words
    )

    response = llm.invoke(formatted_prompt)

    

    # print(response)
    return response






st.set_page_config(page_title="Generate Blogs",
                    page_icon='🤖',
                    layout='centered',
                    initial_sidebar_state='collapsed')

st.header("Generate Blogs 🤖")

input_text=st.text_input("Enter the Blog Topic")

## creating to more columns for additonal 2 fields

col1,col2=st.columns([5,5])

with col1:
    no_words=st.text_input('No of Words')
with col2:
    blog_style=st.selectbox('Writing the blog for',
                            ('Researchers','Data Scientist','Common People'),index=0)
    
submit=st.button("Generate")

## Final response
if submit:
    if not input_text.strip():
        st.error("Please enter a blog topic.")
    else:
        with st.spinner("Generating blog..."):
            output = getLLamaresponse(input_text, no_words, blog_style)
            st.write(output)