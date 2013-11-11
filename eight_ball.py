# Import some necessary libraries.
import socket 
import pywapi
import string
from random import randint
from random import choice

# Some basic variables used to configure the bot        
server = "colorscience.lpdev.prtdev.lexmark.com" # Server
channel = "#innovationcouch" # Channel
botnick = "IT8Ball" # Your bots nick

def ping(): 
  ircsock.send("PONG :pingis\n")  

def sendmsg(chan , msg): 
  ircsock.send("PRIVMSG "+ chan +" :"+ msg +"\n") 

def joinchan(chan):
  ircsock.send("JOIN "+ chan +"\n")

def provide_insight():
  answer_array = [
            "It is certain",
            "It is decidedly so",
            "Without a doubt",
            "Yes definitely",
            "You may rely on it",
            "As I see it yes",
            "Most likely",
            "Outlook good",
            "Yes",
            "Signs point to yes",
            "Reply hazy try again",
            "Ask again later",
            "Better not tell you now",
            "Cannot predict now",
            "Concentrate and ask again",
            "Don't count on it",
            "My reply is no",
            "My sources say no",
            "Outlook not so good",
            "Very doubtful",
            "Please reboot your machine",
            "Add more RAM",
        ]
  answer_key = randint(0,21)
  sendmsg(channel, answer_array[answer_key] + "\n")

def report_lex_weather():
  weather_result = pywapi.get_weather_from_yahoo('40513',units = 'imperial')
  sendmsg(channel, "It is " + string.lower(weather_result['condition']['text']) + " and " + weather_result['condition']['temp'] + "F now in Lexington.\n")

                  
ircsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ircsock.connect((server, 6667))
ircsock.send("USER "+ botnick +" "+ botnick +" "+ botnick +" :weather / magic eight ball bot\n")
ircsock.send("NICK "+ botnick +"\n")

joinchan(channel)

while 1:
  ircmsg = ircsock.recv(2048) # receive data from the server
  ircmsg = ircmsg.strip('\n\r') # removing any unnecessary linebreaks.
  print(ircmsg) # Here we print what's coming from the server
  sender_nick = ircmsg.split(" ")
  sender_nick = sender_nick[0]
  sender_nick = sender_nick.split("!")
  sender_nick = sender_nick[0]
  sender_nick = sender_nick.strip(":")
 
  if ircmsg.find(":eight:") != -1:
    provide_insight()

  if ircmsg.find(":weather:") != -1:
    report_lex_weather()

  if ircmsg.find("PING :") != -1:
    ping()
