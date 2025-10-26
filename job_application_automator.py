# Project: Job Application Automator
# File: job_application_automator.py
# Purpose: Generates and emails personalized cover letters to employers using OpenAI GPT-4o mini API.
# Dependencies: openai>=1.2.0, smtplib, kivy>=2.3.0, Python 3.10+
# Author: Emily Au

from openai import OpenAI

import kivy
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button

import smtplib
from email.mime.text import MIMEText

# Your OpenAI API key
client = OpenAI(api_key = "")

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
        self.prompt1 = Label(text = 'Resume Below', font_size = '50', size_hint = (1, 0.5))
        self.add_widget(self.prompt1)

        # text box 1
        self.userInput1 = TextInput(text = 'Type here')
        self.add_widget(self.userInput1)

        # prompt label 2
        self.prompt2 = Label(text = 'Job Description Below', font_size = '50', size_hint = (1, 0.5))
        self.add_widget(self.prompt2)

        # text box 2
        self.userInput2 = TextInput(text = 'Type here')
        self.add_widget(self.userInput2)

        # generate response button
        self.press = Button(text = 'Click Here to Generate Response', size_hint = (1, 0.5))
        self.press.bind(on_press = self.click_me)
        self.add_widget(self.press)

        # temporary response label
        self.response = Label(text = '', text_size = (2000, None), size_hint = (1, 1.5), halign = 'center')
        self.response.bind(width=self.update_response_text_size)
        self.add_widget(self.response)

        # generate email send button
        self.send = Button(text = 'Click Here to Send Email', size_hint = (1, 0.5))
        self.send.bind(on_press = self.email_sent)
        self.add_widget(self.send)

    # dynamic text adjustment
    def update_response_text_size(self, instance, value):
        instance.text_size = (value, None)
        instance.texture_update()
        instance.height = instance.texture_size[1]

    # Response generation
    def click_me(self, instance):
        prompt = "Given the following resume: '" + self.userInput1.text + "' and the following job description: '" + self.userInput2.text + "' please generate a customized cover letter without any formatting, empty lines, or special characters."
        
        self.response.text = 'Generating response ...'
        
        # generate response with OpenAI GPT model of your choice
        completion = client.chat.completions.create(model="gpt-4o-mini", messages=[{"role": "user", "content": prompt}])
        print(completion.choices[0].message.content)

        # response label
        self.response.text = 'The full cover letter has been generated and printed in the terminal. Here is a snippet:\n' + (completion.choices[0].message.content)[:400] + '...'

        # creating email
        global body
        body = completion.choices[0].message.content

    # Sending email to desired recipient
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
            print("Please generate a cover letter")


class JobApplicationAutomatorApp(App):
    def build(self):
        return myApp()

if __name__ == "__main__":
    JobApplicationAutomatorApp().run()