import os
from dotenv import load_dotenv
import streamlit as st
from langchain.prompts import PromptTemplate
from langchain_huggingface import HuggingFaceEndpoint
from huggingface_hub.utils import HfHubHTTPError

# Load .env file for HuggingFace Token
load_dotenv()


os.environ['HF_TOKEN']=st.secrets["HF_TOKEN"]


## Function To get response from Model

def getLLamaresponse(input_text,no_words,blog_style):

    ### Model
    repo_id = "mistralai/Mistral-7B-Instruct-v0.1"

    llm = HuggingFaceEndpoint(
        repo_id=repo_id, 
        huggingfacehub_api_token=os.environ["HF_TOKEN"],
        temperature=0.01,
        max_new_tokens=500
    )
    
    ## Prompt Template

    template="""
        Write a blog on the topic {input_text} for {blog_style} audience
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
                            ('Beginner','Intermediate','Advanced'),index=0)
    
submit=st.button("Generate")

## Final response
if submit:
    if not input_text.strip():
        st.error("Please enter a blog topic.")
    else:
        with st.spinner("Generating blog..."):
            try:
                output = getLLamaresponse(input_text, no_words, blog_style)
                st.write(output)
            except HfHubHTTPError as e:
                if "Payment Required" in str(e):
                    st.error("Sorry, exceeded the monthly included credits for Inference Providers.")
                else:
                    st.error(f"An error occurred: {e}")
            except Exception as e:
                st.error(f"Unexpected error: {type(e).__name__} - {e}")