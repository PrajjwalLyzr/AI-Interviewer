from lyzr import QABot
from pathlib import Path
import os
from dotenv import load_dotenv


load_dotenv()


os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')

def ai_interviewer(path, file):
    if file == '.pdf':
        interviewer_pdf = QABot.pdf_qa(
            input_files=[Path(path)]
        )

        return interviewer_pdf
    
    if file == '.docx':
        interviewer_doc = QABot.docx_qa(

            input_files=[Path(path)]
        )

        return interviewer_doc
