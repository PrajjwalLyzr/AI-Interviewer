import streamlit as st
import os
from pathlib import Path
from PIL import Image
from utils import utils
from lyzr_qabot import ai_interviewer

utils.page_config()

data = "data"
os.makedirs(data, exist_ok=True)

image = Image.open("./logo/lyzr-logo.png")
st.image(image, width=150)
st.title('AI Interviewer 👩🏻‍💻💬')
st.markdown('Welcome to the lyzr AI Interviewer app, this app will help you to prepare your upcoming interviews !!!')



def interviwer(path, filetype):
    interview_agent = ai_interviewer(path=path, file=filetype)
    metric = "Extract all the skills from the given file"
    skills = interview_agent.query(metric)

    return skills.response


def gpt_interview_questions(qabot_response):
    question_response = utils.llm_calling(user_prompt=f"Create one interview question on based on this skill set {qabot_response}, [!important] question should not more than 2 line make it very specific",
                                   system_prompt=f"You are an interview expert",llm_model="gpt-4-turbo-preview")

    answer_response = utils.llm_calling(user_prompt=f"Generate answer for this {question_response}, [!Important] answer should not more than 3 lines, make it simple",
                                   system_prompt=f"You are an interview expert",llm_model="gpt-4-turbo-preview")  
    
    return question_response, answer_response



def question_answer_session(typefile):
    path = utils.get_files_in_directory(data)
    filepath = path[0]
    qa_response = interviwer(path=filepath, filetype=typefile)
    question, gpt_answer = gpt_interview_questions(qabot_response=qa_response)
    st.header(question)
    answer = st.text_input('Write your response')
    if answer:
        st.write(answer)
    st.markdown('---')
    st.subheader('Gpt answer')
    st.write(gpt_answer)


def main():
    st.sidebar.image(image, width=150)
    file = st.sidebar.file_uploader("Upload your resume", type=["pdf", "docx"])
    if file is None:
        st.subheader('👈 Upload you resume to get started!!!')
        utils.remove_existing_files(data)
        
    if file is not None:
        utils.save_uploaded_file(file, directory_name=data)
        typefile = Path(file.name).suffix

        if st.sidebar.button('Next'): 
            question_answer_session(typefile=typefile)
            
        st.sidebar.info('Click this 👆 Button to generate Interview Questions')
            

if __name__ == "__main__":
    utils.style_app()
    main()
    utils.template_end()
    