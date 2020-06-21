import pyttsx3
from os import system, _exit
from datetime import datetime
import platform
import socket
import speech_recognition as sr
from random import randint
from wikipedia import summary
import smtplib, ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import webbrowser
import pyautogui as pyag
import pyjokes as pyjk

r = sr.Recognizer()
m = sr.Microphone()
error_messages = ["Something Went Wrong", "Pardon Me", "I Didn't Get It"]

class NoInternet(Exception):
	'''This Exception Is Raised When There
	Is No Internet Connection.'''
	pass

system("cls")
engine = pyttsx3.init()

def Simon_Talk(TEXT_TO_TALK):
	engine.setProperty('rate', 142)
	print("Simon : {}".format(TEXT_TO_TALK))
	engine.say(TEXT_TO_TALK)
	engine.runAndWait()

def Current_Time():
	t = datetime.now().strftime("%I:%M %p")
	Simon_Talk(t)

def Current_Date():
	d = datetime.now().strftime("%d %B %Y")
	Simon_Talk(d)

def Welcome_Message():
	saying = "Welcome Back"
	if datetime.now().hour < 12:
		saying = "Good Morning"
	elif datetime.now().hour >= 12 and datetime.now().hour <= 17:
		saying = "Good Afternoon"
	saying += " {}".format(platform.node().title())
	Simon_Talk(saying)
	Simon_Talk("How Can I Help You ?")

def Internet_Checking():
	count = 0
	while True:
		system("cls")
		try:
			ip_address = socket.gethostbyname(socket.gethostname())
			if ip_address == "127.0.0.1":
				Simon_Talk("Your Not Connected To The Internet")
				raise NoInternet
		except NoInternet:
			if count > 1:
				Simon_Talk("Too Many Tries, Comeback Later")
				_exit(1)
			Simon_Talk("Press Any Key After Connecting To The Internet")
			input()
			count += 1
		else:
			break

def Bye_Message():
	Simon_Talk("Bye Bye {}".format(platform.node().title()))
	if datetime.now().hour > 17:
		Simon_Talk("Good Night, Sweet Dreams")

def User_Input():
	Internet_Checking()
	with m as source:
		r.adjust_for_ambient_noise(source)
		Simon_Talk("I Am Listening.....")
		audio = r.listen(source)
	try:
		uvoice = r.recognize_google(audio, language = "en-in").title()
		print("You : {}".format(uvoice))
	except :
		Simon_Talk(error_messages[randint(0,len(error_messages))])
		return ""
	else:
		uvoice = uvoice.lower()
		if "simon" in uvoice:
			uvoice.replace("simon", "")
			if "hey" in uvoice:
				uvoice.replace("hey", "")
		return uvoice.lower()

time_commands = ["what is the time", "what is the time now", "what time it is", "what time it is now", "what is the time right now"]
date_commands = ["what is the date", "what is today's date", "what is today"]
bye_commands = ["bye", "bai", "bhai", "boy"]

def Wikipedia_Result(matter):
	if "?" in matter:
		matter = matter.replace("?", "")
	if "who is" in matter:
		matter = matter.replace("who is", "")
	elif "what is" in matter:
		matter = matter.replace("what is", "")
	answer = summary(matter, sentences = 1, auto_suggest = True)
	Simon_Talk("According To Wikipedia")
	Simon_Talk(answer)

def Mail_Send():
	try:
		Internet_Checking()
		message = MIMEMultipart()
		Simon_Talk("Fill In The Form Below ")
		user_email = input("Enter Your Email : ")
		user_pass = input("Enter Your Password : ")
		reciever = input("Reciever's Email : ")
		message["From"] = user_email[:]
		message["To"] = reciever[:]
		message["Subject"] = input("Enter Subject : ")
		body = input("Enter The Content To Send : ")

		message.attach(MIMEText(body, 'plain'))
		my_message = message.as_string()
		context = ssl.create_default_context()
		server = smtplib.SMTP("smtp.gmail.com", 587)
		server.ehlo()  
		server.starttls(context=context)
		server.ehlo()
		server.login(user_email, user_pass)
		server.sendmail(user_email, reciever, my_message)
		server.quit()
	except Exception as e:
		print(e)
		Simon_Talk("Something Went Wrong")
	else:
		Simon_Talk("Email Has Been Sent Successfully")
	system("cls")

def Search_The_Web(content):
	Simon_Talk("Checking Duck Duck Go For " + content)
	webbrowser.open("https://duckduckgo.com/?q=" + content)

def Take_Screenshot():
	Simon_Talk("Taking Screenshot")
	img = pyag.screenshot()
	img.save("C:\\Users\\{}\\Pictures\\cap.png".format(platform.node()))
	Simon_Talk("Screenshot Has Been Saved To Your Pictures Folder")

def Tell_Joke():
	Simon_Talk(pyjk.get_joke())

if __name__ == "__main__":
	system("cls")
	Welcome_Message()
	commands = list()
	while True:
		input("Press Any Key To Activate Simon")
		command = User_Input()
		commands.append(command)

		if command == "what is today's date and time":
			Simon_Talk("Today Is ")
			Current_Date()
			Simon_Talk("And The Time Is ")
			Current_Time()
	
		elif command in time_commands:
			Simon_Talk("The Time Is")
			Current_Time()

		elif command in date_commands:
			Simon_Talk("The Date Is")
			Current_Date()

		elif command in bye_commands:
			command = "Bye"
			break

		elif "command history" in command:
			Simon_Talk("Your Commands Are Given Below ")
			for text in commands:
				print(text)

		elif ("who is" in command) or ("what is" in command):
			Wikipedia_Result(command[:])

		elif ("send email" in command) or ("email" in command):
			Mail_Send()

		elif ("logout" in command) or ("log out" in command) or ("logoff" in command) or ("log off" in command):
			Simon_Talk("Logging Out In Few Seconds")
			system("shutdown -l")

		elif "shutdown" in command:
			Simon_Talk("Shutting Down In 10 Seconds")
			system("shutdown -s -t 10")

		elif "restart" in command:
			Simon_Talk("Restarting The System In 10 Seconds")
			system("shutdown -r -t 10")

		elif "abort" in command:
			Simon_Talk("Aborting System Operation")
			system("shutdown -a")

		elif "play" in command:
			command = command.replace("play", "")
			Simon_Talk("Checking Youtube For {}".format(command))
			webbrowser.open("https://www.youtube.com/results?search_query=" + command)

		elif "take screenshot" in command:
			Take_Screenshot()

		elif "happy" == command.split()[0]:
			Simon_Talk("Thank You So Much")
			Simon_Talk("I Wish You The Same")

		elif "joke" in command:
			Tell_Joke()

		elif "open" == command.split()[0]:
			try:
				command = command.replace("open", "")
				Simon_Talk("Trying To Open {}".format(command))
				system("start {}".format(command))
			except:
				Simon_Talk("Software Does No Exist")

		else:
			if command == "":
				pass
			else:
				Search_The_Web(command[:])
	
	Bye_Message()

