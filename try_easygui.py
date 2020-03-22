import easygui as g
import sys
while 1:
     g.msgbox("hello")
     msg = "what can i learn from this"
     title = "interact game"
     choices = ["love", "code", "readbook"]
     choice = g.choicebox(msg, title, choices)
     g.msgbox("your choice is:"+str(choice),"result")
     g.boolbox("boolbox","try_boolbox")
     msg = "do you want to play game again?"
     title = "please choose"
     if g.ccbox(msg, title):
             pass
     else:
             sys.exit(0)
