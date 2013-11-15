# Import some necessary libraries.
import socket 
import pywapi
import sys
import string
import aiml
from PyGtalkRobot import GtalkRobot
from random import randint
from random import choice

#stuff from ai library
k = aiml.Kernel()
k.learn("std-startup.xml")
k.respond("load aiml b")


def ping(): 
  ircsock.send("PONG :pingis\n")  

def sendmsg(chan , msg):
  print("I say " + msg)
  ircsock.send("PRIVMSG "+ chan +" :"+ msg +"\n") 

def joinchan(chan):
  ircsock.send("JOIN "+ chan +"\n")

def provide_yesno(recipient):
  yesno_array = [
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
        ]
  answer_key = randint(1,(len(yesno_array) - 1))
  sendmsg(recipient, yesno_array[answer_key] + "\n")

def provide_hollister_insight(recipient):
  hollister_array = [
            "Please reboot your machine",
            "Add more RAM",
            "do you mind if I check your uptimers?",
            "did you reboot a second time?",
            "let me ask my partner",
            "your hard drive needs to be defragmented",
            "your environmental variables may need adjustment",
            "server cluster will be rebooted at 3pm, it will probably work then",
        ]
  answer_key = randint(1,(len(hollister_array) - 1))
  sendmsg(recipient, hollister_array[answer_key] + "\n")

def report_lex_weather(recipient):
  weather_result = pywapi.get_weather_from_yahoo('40513',units = 'imperial')
  sendmsg(recipient, "It is " + string.lower(weather_result['condition']['text']) + " and " + weather_result['condition']['temp'] + "F now in Lexington.\n")

def online_help(recipient):
  sendmsg(recipient, "\"eighthelp:\" for this help message.\n")
  sendmsg(recipient, "\"eight: <question>\" for a yes/no response.\n")
  sendmsg(recipient, "\"weather:\" for a quick Lexington weather summary.\n")
  sendmsg(recipient, "\"hollister: <problem>\" for a hollister solution to your problem.\n")

def chatty_mc_chatterson(recipient, msg):
  response = k.respond(raw_message)
  sendmsg(recipient, response) 

###################################################################################
                  
if len(sys.argv) != 4:
  print "Usage: eight_ball <server[:port]> <channel> <nickname>"
  sys.exit(1)
s = sys.argv[1].split(":", 1)
server = s[0]
if len(s) == 2:
  try:
    port = int(s[1])
  except ValueError:
    print "Error: Erroneous port."
    sys.exit(1)
else:
  port = 6667

channel = sys.argv[2]
botnick = sys.argv[3]

ircsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ircsock.connect((server, port))
ircsock.send("USER "+ botnick +" "+ botnick +" "+ botnick +" :weather / magic eight ball bot\n")
ircsock.send("NICK "+ botnick +"\n")

joinchan(channel)


while 1:
  ircmsg = ircsock.recv(2048) # receive data from the server
  ircmsg = ircmsg.strip('\n\r') # removing any unnecessary linebreaks.
  sender_nick = ircmsg.split(" ")
  sender_nick = sender_nick[0]
  sender_nick = sender_nick.split("!")
  sender_nick = sender_nick[0]
  sender_nick = sender_nick.strip(":")
  raw_message = ircmsg.split(":")
  if (len(raw_message) == 3):
    raw_message = raw_message[2]
    print (sender_nick + ": " + raw_message)

  
  if ircmsg.find("PRIVMSG "+ botnick) != -1:
    sendto = sender_nick
  else:
    sendto = channel

  if ircmsg.find(":hollister:") != -1:
    provide_hollister_insight(sendto)

  elif ircmsg.find(":eight:") != -1:
    provide_yesno(sendto)

  elif ircmsg.find(":eighthelp:") != -1:
    online_help(sendto)

  elif ircmsg.find(":weather:") != -1:
    report_lex_weather(sendto)

  elif (sendto == sender_nick):
    chatty_mc_chatterson(sendto, raw_message)

  if ircmsg.find("PING :") != -1:
    ping()
