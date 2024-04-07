# AI survey V1
 
Credit: The code for this was modelled on my own submission for the Mercedes F1 Inversity challenge as a base and my CS50 project

Overview:
This App allows the user to create an AI-driven survey, of 1-10 questions, with a survey objective of their choice and asking them to craft the initial question to kick things off. Note that there has been some error testing but not as robust as would be needed for Production given what can be asked, albeit ChatGPT already has a number of controls in place regarding inputs (e.g. managing use of inappropriate language).

The app.py file contains the main Flask application, with most functions marked separately in functions.py.

The templates folder holds the HTML templates, with responses.html containing JavaScript to dynamically construct the page (note VS Code sees a syntax error where Python Flask/Jinja/JavaScript interacts, albeit the code seems to run fine and suspect this is just due to VS Code struggling to parse with current extensions).

Currently the App doesn't have a way to manually reset a survey, it needs to be restarted, HOWEVER creating a new survey seems to effectively reset and create new data, albeit I've not tested it with all edge cases.


IMPORTANT:
The Google-sheet that it prints data to can be found here:
https://docs.google.com/spreadsheets/d/1nSrmGO8ZSwJhtitmjnrwXeLhfTq8AVKtcRFKUObUDhY/edit?usp=sharing

It is viewable by anyone, but a Google API key will be needed to run the Flask, and the Google API will need to submit an edit request to the G-sheet for the user.
