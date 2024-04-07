from openai import OpenAI, Client
from dotenv import load_dotenv
from flask import request
import pygsheets

load_dotenv()  # Load environment variables from .env file
client = OpenAI()  # Initialize the OpenAI client with the API key

def get_survey_response():
    output = request.form.get('response')
    return output

def craft_question(questions, responses, max_question):
    rules = '''We are creating a dynamic and responsive survey to determine how people find and engage with educational online content. We have a 
    starter survey question, and some example follow-up questions, but we really want to hone in on useful and insightful information a user might give.
    As a result, we want to utilise ChatGPT to have more advanced skip logic by reading a users input to then craft a useful follow-up question.
    This is where you'll come in. Importantly, please produce your response exactly as it should appear in the survey to the user,
    because the API is being called to print your response in directly. So as an example please DON'T preface with "Great! Here's a tailored follow-up question based on their response to the initial question: Follow-up question:"
    '''

    
    message = [
        "Here's the first fixed question that's being asked: ",
        questions[0],
        "Their response to this question is: ",
        responses[0]
    ]

    for i in range(len(responses)):
        try:
            message.extend([
                "And then you asked the question: ",
                questions[i],
                "To which they've responded: ",
                responses[i],
            ])
            if i == max_question - 1:
                message.append("So now, please craft a FINAL follow-up question.")
            else:
                message.append("So now, please craft a follow-up question.")
        except IndexError:
            break

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

def export(questions, responses):
    gc = pygsheets.authorize(service_account_env_var = 'GDRIVE_API_CREDENTIALS')

    # Open the google spreadsheet
    sh = gc.open_by_key('1nSrmGO8ZSwJhtitmjnrwXeLhfTq8AVKtcRFKUObUDhY')

    # Select the Daily Tracker worksheet
    wks = sh.worksheet_by_title('Results - Multiple questions')

    # Look at first column to find first empty row
    # Find the next empty row in the first column
    next_row = 1
    while wks.get_value((next_row, 1)):
        next_row += 1
    
    column_index = 0

    list_c = list(zip(questions, responses))

    # Update values
    for i in list_c:
        try:
            wks.update_value(f"{chr(65 + column_index)}{next_row}", i[0])  # Convert column index to letter
            wks.update_value(f"{chr(65 + column_index + 1)}{next_row}", i[1])  # Convert column index to letter
            column_index += 2  # Question in odd columns, response in even columns
        except IndexError:
            continue


def init_questions(max_question):
    questions = [None for _ in range(max_question)]

    questions[0] = "How often do you read/watch educational things online like articles, videos, or social media posts?"
    questions[1] = "What makes you want to click on something you see online?"
    questions[2] = "If something you're reading or watching online lets you interact with it (like taking quizzes, voting in polls, or moving things around), are you more likely to keep reading or watching?"

    return questions