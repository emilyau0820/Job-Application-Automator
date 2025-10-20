# Project: Job Application Automator
# File: job_application_automator.py
# Purpose: Generates and emails personalized cover letters to employers using OpenAI GPT-4o mini API.
# Dependencies: openai>=0.27, smtplib, kivy, Python 3.10+
# Author: Emily Au

import openai

import kivy
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button

import smtplib
from email.mime.text import MIMEText

# Your OpenAI API key
openai.api_key = ""

# SMPT connection
smtp_server = "smtp.gmail.com"
port = 587

# Your desired email address and app password
username = "youremail@gmail.com"
password = "16 character app password"
sender_email = username

# Employer's email address and email details
receiver_email = "employeremail@gmail.com"
subject = "Application for [Job Title] - [Your Name]"
body = ''

class myApp(GridLayout):
    # initiation
    def __init__(self,**kwargs):
        super(myApp, self).__init__()
        self.cols = 1

        # prompt label 1
        self.prompt1 = Label(text = 'Please paste your resume in the textbox below', font_size = '50', size_hint = (1, 0.5))
        self.add_widget(self.prompt1)

        # text box 1
        self.userInput1 = TextInput(text = 'Type here')
        self.add_widget(self.userInput1)

        # prompt label 2
        self.prompt2 = Label(text = 'Please paste the job description in the textbox below', font_size = '50', size_hint = (1, 0.5))
        self.add_widget(self.prompt2)

        # text box 2
        self.userInput2 = TextInput(text = 'Type here')
        self.add_widget(self.userInput2)

        # generate response button
        self.press = Button(text = 'Click Here to Generate Response', size_hint = (1, 0.5))
        self.press.bind(on_press = self.click_me)
        self.add_widget(self.press)

        # temporary response label
        self.response = Label(text = '', text_size = (2000, None), size_hint = (1, 2))
        self.add_widget(self.response)

        # generate email send button
        self.send = Button(text = 'Click Here to Send Email', size_hint = (1, 0.5))
        self.send.bind(on_press = self.email_sent)
        self.add_widget(self.send)

    # if generate response button clicked
    def click_me(self, instance):
        prompt = "Given the following resume: '" + self.userInput1.text + "' and the following job description: '" + self.userInput2.text + "' please generate a customized cover letter."
        
        self.response.text = 'Generating response ...'
        
        # generate response with OpenAI GPT model of your choice
        completion = openai.ChatCompletion.create(model="gpt-4o-mini", messages=[{"role": "user", "content": prompt}])
        print(completion.choices[0].message.content)

        # response label
        self.response.text = 'Your response has been generated and printed in the terminal. Please press the buttom if you would like to receive this response via email'

        # create email
        global body
        body = completion.choices[0].message.content

    # if send email button clicked
    def email_sent (self, instance):
        print("button clicked: " + body)

        if body!='':
            message = MIMEText(body, "plain")
            message["Subject"] = subject
            message["From"] = sender_email
            message["To"] = receiver_email

            try:
                with smtplib.SMTP(smtp_server, port) as server:
                    server.starttls()
                    server.login(username, password)
                    server.sendmail(sender_email, receiver_email, message.as_string())
                print("Email sent successfully!")
            except Exception as e:
                print(f"Error: {e}")
        else:
            print("please generate a prompt before pressing")


class JobApplicationAutomatorApp(App):
    def build(self):
        return myApp()

if __name__ == "__main__":
    JobApplicationAutomatorApp().run()