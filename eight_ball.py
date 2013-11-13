# Import some necessary libraries.
import socket 
import pywapi
import sys
import string
from random import randint
from random import choice

def ping(): 
  ircsock.send("PONG :pingis\n")  

def sendmsg(chan , msg): 
  ircsock.send("PRIVMSG "+ chan +" :"+ msg +"\n") 

def joinchan(chan):
  ircsock.send("JOIN "+ chan +"\n")

def provide_yesno():
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
  sendmsg(channel, yesno_array[answer_key] + "\n")

def provide_hollister_insight():
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
  sendmsg(channel, hollister_array[answer_key] + "\n")

def report_lex_weather():
  weather_result = pywapi.get_weather_from_yahoo('40513',units = 'imperial')
  sendmsg(channel, "It is " + string.lower(weather_result['condition']['text']) + " and " + weather_result['condition']['temp'] + "F now in Lexington.\n")

def online_help():
  sendmsg(channel, "\"eighthelp:\" for this help message.\n")
  sendmsg(channel, "\"eight: <question>\" for a yes/no response.\n")
  sendmsg(channel, "\"weather:\" for a quick Lexington weather summary.\n")
  sendmsg(channel, "\"hollister: <problem>\" for a hollister solution to your problem.\n")
                  
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
  print(ircmsg) # Here we print what's coming from the server
  sender_nick = ircmsg.split(" ")
  sender_nick = sender_nick[0]
  sender_nick = sender_nick.split("!")
  sender_nick = sender_nick[0]
  sender_nick = sender_nick.strip(":")
 
  if ircmsg.find(":hollister:") != -1:
    provide_hollister_insight()

  if ircmsg.find(":eight:") != -1:
    provide_yesno()

  if ircmsg.find(":eighthelp:") != -1:
    online_help()

  if ircmsg.find(":weather:") != -1:
    report_lex_weather()

  if ircmsg.find("PING :") != -1:
    ping()
