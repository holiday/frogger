from mtTkinter import *
from PlayerClient import *
from Command import *
from Observer import *
from Countdown import *
import json
from froggerRun import *
import random

class App(Observer):
    def __init__(self,parent):
        #The frame instance is stored in a local variable 'f'.
        #After creating the widget, we immediately call the 
        #pack method to make the frame visible.
        
        f = Frame(parent)
        f.pack(padx=100,pady=50)
        self.f=f
        self.parent = parent
        # keep track of my player id
        self.myPid=None
        # keep track of the other players
        self.otherPlayers={}
        # keep track of the ip
        self.ip = "142.150.2.94"
        self.port = 1337
        self.gameCount = 0 
        self.playerName = "Player" + str(random.randint(1,100))
        #we then create an entry widget,pack it and then 
        #create two more button widgets as children to the frame.
        self.name = Label(f, text="Your Name:", font=("Helvetica", 15))
        self.name.pack(side=TOP)

        self.nameE = Entry(f, width=15)
        self.nameE.insert(0, self.playerName)
        self.nameE.pack(side=TOP,padx=5,pady=5)

        self.startBtn = Button(f, text="Join Game", command=self.setupChat)
        self.startBtn.pack(side=TOP,padx=10,pady=10)

        menubar = Menu(root)

        # create more pulldown menus
        editmenu = Menu(menubar, tearoff=0)
        editmenu.add_command(label="Restart", command=self.restartGame)
        editmenu.add_command(label="Settings", command=self.settings)
        editmenu.add_command(label="Quit", command=self.onClose)
        menubar.add_cascade(label="Game", menu=editmenu)

        self.parent.config(menu=menubar)

        self.listall = None

        #make the player client thread
        self.myListener = None
        self.parent.protocol('WM_DELETE_WINDOW', self.onClose)

        #make an instance of the counter but do not start it
        self.counter = Countdown(5)
        self.counter.addObserver(self)

    def settings(self):
        ''' Handle the GUI for the settings page '''
        self.settingsDialog = Tk()
        self.settingsDialog.title('Frogger Settings')

        labelframe = LabelFrame(self.settingsDialog, text="Server Connection Settings")
        labelframe.pack(fill="both", expand="yes")

        f = Frame(self.settingsDialog)
        f.pack()

        # set the ip address
        ipaddress = Label(labelframe, text="Server ip:")
        ipaddress.grid(row=1, column=0, sticky=E)

        self.inp = Entry(labelframe, width=15)
        self.inp.insert(0, self.ip)
        self.inp.grid(row=1, column=1, sticky=E)

        port = Label(labelframe, text="Server port:")
        port.grid(row=2, column=0, sticky=W)

        self.pinp = Entry(labelframe, width=10)
        self.pinp.insert(0, self.port)
        self.pinp.grid(row=2, column=1, sticky=W)

        savebtn = Button(labelframe, text="Save")
        savebtn.grid(row=3, column=1, sticky=W)
        savebtn.bind('<Button-1>',self.saveServer)

        RWidth= 300
        RHeight= 100
        self.settingsDialog.geometry(("%dx%d")%(RWidth,RHeight))
        self.settingsDialog.mainloop()

    def saveServer(self, e):
        '''Save the ip address and port from settings dialog'''
        try:
            self.ip = self.inp.get()
            self.port = self.pinp.get()
            self.settingsDialog.destroy()
        except Exception as e:
            print("Error reading ip")


    def closeDialog(self):
        ''' Close the dialog for the settings '''
        try:
            self.settingsDialog.destroy()
        except Exception as e:
            print("Error closing dialog")

    def onClose(self):
        ''' handle the parent and GUI on close '''
        if self.myListener!=None:
            self.myListener.disconnect()
        self.parent.quit()
        self.parent.destroy()
        sys.exit()

    def callback(self,e):
        ''' after user enters name into the main page '''
        if(self.nameE.get()!=''):
            self.playerName=self.nameE.get()
            self.button1.pack_forget()
            self.button2.pack_forget()
            self.button3.pack_forget()
            self.exit.pack_forget()
            self.setupChat(e)

    def setupChat(self,e=None):
        ''' Setup the chat GUI '''
        self.playerName = self.nameE.get()
        #setup listener
        if self.myListener is None:
            self.myListener = PlayerClient(self.playerName, self.ip, self.port)
            self.myListener.start()
            self.myListener.addObserver(self)
            self.myListener.clearChanged()

        # forget the last frame
        self.f.pack_forget()
        self.fr = Frame(self.parent)

        # init the elements for the GUI
        self.textbox = Text(self.fr, height=20, width=70, wrap=WORD, state=DISABLED)
        self.textbox.grid(row=0, column=0, sticky=W)
        self.scroll = Scrollbar(self.fr)
        self.textbox.config(yscrollcommand=self.scroll.set)

        self.scroll.config(command=self.textbox.yview)
        self.v = StringVar()
        self.inp = Entry(self.fr, width=55, textvariable=self.v)
        self.inp.grid(row=1, column=0, sticky=W)
        self.send = Button(self.fr, text="send")
        self.send.grid(row=1, column=0, sticky=E)
        self.listall = Listbox(self.fr)
        self.listall.grid(row=0, column=1, sticky=N)
        self.time = Label(self.fr, text="", font=("Helvetica", 50))
        self.time.grid(row=0, column=1, sticky=S)

        self.restartbtn = Button(self.fr, text="restart")
        self.restartbtn.grid(row=1, column=1, sticky=S)

        # bind the keys to callback functions
        self.send.bind('<Button-1>', self.sendtext)
        self.inp.bind('<Return>', self.sendtext)
        self.restartbtn.bind('<Button-1>', self.restartGame)
        
        self.fr.pack()
        self.updatelistall(self.playerName)
        
    def sendtext(self,e):
        ''' handle sending text to all the players  '''
        self.textbox.yview(END) 
        if(self.inp.get()!=''):
            self.textbox.config(state=NORMAL)
            self.textbox.insert(END, self.playerName+'> '+self.inp.get().strip(' ')+ '\n')


            #send the message to all players
            if self.myListener is not None:
                self.myListener.send(MsgCommand.encode('MSG', self.playerName, self.inp.get().strip(' ')))
                
            self.textbox.config(state=DISABLED)
            self.v.set('')
            self.fr.update_idletasks()
    
    def updatelistall(self,name):
        ''' update the player list in chat '''
        try:
            self.listall.insert(END,name)
            self.fr.update_idletasks()
        except Exception as e:
            print("Error updating listall: ", e)

    def restartGame(self, e):
        ''' take user back to old view '''
        self.fr.destroy()
        self.f.pack()

    def update(self, listener):
        ''' update function that is used to notify every one '''
        try:
            if listener.data is not None:
                commands = listener.data.decode().splitlines()
                for cmd in commands:
                    cmd = Command.decode(cmd)
                    if cmd["CMD"].strip() == "MSG":
                        # Message command coming in, insert into textarea
                        self.textbox.config(state=NORMAL)
                        self.textbox.insert(END, cmd["pname"] + "> " + cmd["msg"] + '\n')
                        self.textbox.config(state=DISABLED)
                        self.textbox.yview(END)
                        self.fr.update_idletasks()
                    elif cmd["CMD"].strip() == "ACK":
                    # ACK command coming in, send Join command out
                        self.myPid=cmd['pid']
                        self.myListener.send(JoinCommand.encode('JOIN',self.myPid,self.playerName))
                        
                    elif cmd["CMD"].strip() == "EXIST":
                    # Exist command coming in, making sure that others exist in chat area
                        print(str(self.playerName) + " GOT EXIST >> ")
                        k = list(self.otherPlayers.keys())
                        if(cmd['pid'] not in k):
                            self.otherPlayers[cmd['pid']]=cmd['pname']
                            self.updatelistall(cmd['pname'])
                            # play the game if 3 players are present
                        if len(self.otherPlayers.keys())==2 and self.counter.started == False:
                            self.counter.start()
                            
                    elif cmd["CMD"].strip() == "JOIN":
                    # Join command coming in
                        print(str(self.playerName) + " GOT JOIN >> ")
                        self.otherPlayers[cmd['pid']]=cmd['pname']
                        self.updatelistall(cmd['pname'])
                        self.myListener.send(JoinCommand.encode('EXIST',self.myPid,self.playerName))
                        
                        if len(self.otherPlayers.keys())==2 and self.counter.started == False:
                            self.counter.start()

                    elif cmd["CMD"].strip() == "DC":
                    # Disconnect Command coming in
                        print("Got a disconnect")
                        k = list(self.otherPlayers.keys())
                        if(str(cmd['pid']) in k):
                            del self.otherPlayers[str(cmd['pid'])]

                        self.listall.delete(1, END)
                        for k,v in self.otherPlayers.items():
                            self.updatelistall(v)

                    elif cmd["CMD"].strip() == "COUNT":
                    # Count command, meaning we should count down and run the game
                        self.time.config(text=cmd["count"])
                        self.gameCount = 0
                        if(cmd['count'] == 0):
                            self.myGame=FroggerRun(self.myPid,list(self.otherPlayers.keys()),self.myListener)
                            self.myGame.start()

                    elif cmd["CMD"].strip() == "END":
                        # END command that tells us that game is over
                        if self.gameCount == 0:

                            self.myGame._can_quit=True
                            self.textbox.config(state=NORMAL)
                            # check to see if theres no winner
                            if cmd["winnerPid"] == None:
                                self.textbox.insert(END, "EVERYBODY LOST :( !" + '\n')
                            elif self.myPid == str(cmd["winnerPid"]):
                            # check if i'm the winner
                                self.textbox.insert(END, self.playerName +  " WON!" + '\n')
                            else:
                            # someone else is the winner
                                self.textbox.insert(END, str(self.otherPlayers[str(cmd["winnerPid"])]) +  " WON!" + '\n')

                            ##self.textbox.insert(END, str(cmd["winnerPid"]) +  " WON!" + '\n')
                            self.textbox.config(state=DISABLED)
                            self.textbox.yview(END)
                            self.fr.update_idletasks()
                            self.gameCount += 1

        except Exception as e:
            print("An error occurred while parsing Command: ", e)
        

root = Tk()
root.title('Frogger Rooms')
app = App(root)
RWidth= 650
RHeight= 350
root.geometry(("%dx%d")%(RWidth,RHeight))
root.mainloop()
