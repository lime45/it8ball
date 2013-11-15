import aiml

k = aiml.Kernel()
k.learn("std-startup.xml")
k.respond("load aiml b")

while True: print k.respond(raw_input("> "))
