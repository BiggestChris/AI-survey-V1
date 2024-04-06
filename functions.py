from openai import OpenAI, Client
from dotenv import load_dotenv
from flask import request
import pygsheets
import os

load_dotenv()  # Load environment variables from .env file
client = OpenAI()  # Initialize the OpenAI client with the API key

def get_survey_response():
    output = request.form.get('response')
    return output

def craft_question(questions, responses):
    rules = '''We are creating a dynamic and responsive survey to determine how people find and engage with educational online content. We have a 
    starter survey question, and some example follow-up questions, but we really want to hone in on useful and insightful information a user might give.
    As a result, we want to utilise ChatGPT to have more advanced skip logic by reading a users input to then craft a useful follow-up question.
    This is where you'll come in. Importantly, please produce your response exactly as it should appear in the survey to the user,
    because the API is being called to print your response in directly. So as an example please don't preface with "Great! Here's a tailored follow-up question based on their response to the initial question: Follow-up question:"
    '''

    
    message = [
        "Here's the first fixed question that's being asked: ",
        questions[0],
        "Their response to this question is: ",
        responses[0]
    ]

    try:
        if responses[1]:
            message.extend([
                "And then you asked the question: ",
                questions[1],
                "To which they've responded: ",
                responses[1],
                "So now, please craft a FINAL follow-up question"
            ])
    except IndexError:
        message.append("So now, please craft a follow-up question")

    input = ' '.join(message)

    completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            # TODO: Link to an SQL database, to pull relevant content and store learnings on how to best apply AI wrapper
            messages = [
                {"role": "system", 
                "content": rules},
                {"role": "user",
                "content": input }
            ]
        )
    
    print(completion.choices[0].message.content)

    return completion.choices[0].message.content

def export():
    print(os.getenv("GDRIVE_API_CREDENTIALS"))

    gc = pygsheets.authorize(service_account_env_var = 'GDRIVE_API_CREDENTIALS')

    # Open the google spreadsheet (this has the key from the Greg Burns Fitness Sheet)
    sh = gc.open_by_key('1nSrmGO8ZSwJhtitmjnrwXeLhfTq8AVKtcRFKUObUDhY')

    # Select the Daily Tracker worksheet
    wks = sh.worksheet_by_title('Test')

    # Look at first column
    wks.get_col(1)

    # Update values
    wks.update_value(f"A1", "test")