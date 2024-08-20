from twisted.cred.checkers import AllowAnonymousAccess, InMemoryUsernamePasswordDatabaseDontUse
from twisted.cred.portal import Portal
from twisted.protocols.ftp import FTPFactory, FTPRealm
from twisted.internet import reactor    
from twisted.python import log
import tkinter as tk
from threading import Thread
from tkinter import scrolledtext
import sys
from tkinter import filedialog
import shutil
import os

x_janela = 445
y_janela = 500
corJanela = "lightgrey"
corHover = "grey"

window = tk.Tk()
window.geometry(f"{x_janela}x{y_janela}")
window.title("fileKong")

botaoClicadoAgora = None


canva = tk.Canvas(
    window,
    width=x_janela,
    height=y_janela,
    bg = corJanela
)
canva.place(x = 0, y = 0)

taOuvindo = False

caminhoArquivos = "./public"

janela = "ftp"



def ftp():
    global inputPorta
    global factory
    global textoLog
    mudaCorDesseBotao(butaos, botaoHost)
    checker = InMemoryUsernamePasswordDatabaseDontUse()
    checker.addUser(username="public", password="12345")


    textoLog = scrolledtext.ScrolledText(
        window, 
        wrap = tk.WORD,
        height = 15,
        width=47,
        state=tk.DISABLED,
        bg = "white"
    )
    textoLog.place(x = 30, y = 200)

    logRedirector = textRedirector(textoLog)
    observadorTerminal = log.FileLogObserver(sys.stdout).emit
    log.addObserver(observadorTerminal)
    log.addObserver(lambda event: logRedirector.write(event['message'][0] + '\n'))

    realm = FTPRealm(caminhoArquivos)
    portal = Portal(realm, [AllowAnonymousAccess(), checker])

    factory = FTPFactory(portal)
    factory.timeOut = 600
    factory.allowAnonymous = True


    window.resizable = (False, False)

    textoPorta = canva.create_text(
        30, 40,
        text="Porta",
        fill="black",
        font=("comic-sans", 10)
    )

    inputPorta = tk.Entry(
        window,
        bg = "white",
        width=8,
    )
    inputPorta.place(x = 10, y = 50)

    botaoServer.place(x=85, y=45)

    botaoMatar.place(x=200, y=45)


    labelProcuradorArquivo.place(x = -10, y=80 )

    botaoArquivo.place(x=315, y=45)


def procuraArquivo():
    nomeArquivo = filedialog.askopenfilename(
                                            initialdir = "/",
                                            title = "Escolha um arquivo",
                                            filetypes = (("all files", "*.*"),)
                                            )
    
    labelProcuradorArquivo.configure(text = "Arquivo enviado: "+ nomeArquivo)
    clonaArquivo(nomeArquivo, caminhoArquivos)


def clicaBotaoHost():
    mudaCorDesseBotao(butaos, botaoHost)
    print("botao host apertado")

def daHover(e):
    if e.widget != botaoClicadoAgora:
        e.widget.config(bg=corHover)

def tiraHover(e):
    if e.widget != botaoClicadoAgora:
        e.widget.config(bg=corJanela)

def clonaArquivo(nomeArquivo, diretorioDestino):
    if not os.path.exists(diretorioDestino):
        raise FileNotFoundError("nao encontrado") 

    shutil.copy2(nomeArquivo,diretorioDestino)

def mudaCorDesseBotao(butaos, butaoClicado):
    global botaoClicadoAgora
    for btn in butaos:
        btn.config(bg = corJanela)
    
    butaoClicado.config(bg=corHover)
    botaoClicadoAgora = butaoClicado

def clicaBotaoClient():
    mudaCorDesseBotao(butaos, botaoClient)
    print("botao client apertado")

class textRedirector:
    def __init__(self, text_widget):
        self.text_widget = text_widget

    def write(self, message):
        self.text_widget.config(state=tk.NORMAL)
        self.text_widget.insert(tk.END, message)
        self.text_widget.config(state=tk.DISABLED)
        self.text_widget.yview(tk.END)

    def flush():
        pass

def startaReactor():
    global taOuvindo
    if taOuvindo == False:
        reactor.run(installSignalHandlers=0)
        taOuvindo = True

def clicaBotaoServer():
    porta = int(inputPorta.get())
    reactor.listenTCP(porta, factory)
    threadHost = Thread(target=startaReactor)
    threadHost.start()

def FechaServer():
    global taOuvindo 
    if taOuvindo == True:
        reactor.stop()
        taOuvindo = False

def adicionaLog(mensagem):
    textoLog.config(state=tk.NORMAL)
    textoLog.insert(tk.END, mensagem + "\n")
    textoLog.config(state=tk.DISABLED)
    textoLog.yview(tk.END)

botaoArquivo = tk.Button(
    window,
    bg = corJanela,
    text= "Arquivo",
    command=procuraArquivo,
    width="10"
)

botaoHost = tk.Button(
    bg = corJanela,
    text= "FTP Host",
    command=ftp,
    width="8",
    height="1"  
)
botaoHost.place(x=0, y=0)

botaoClient = tk.Button(
    bg = corJanela,
    text= "FTP Client",
    command=clicaBotaoClient,
    width="8",
    height="1"
)
botaoClient.place(x=88, y=0)

botao3 = tk.Button(
    bg = corJanela,
    text= "FTP Client",
    command=clicaBotaoClient,
    width="8",
    height="1"
)
botao3.place(x=176, y=0)

botao4 = tk.Button(
    bg = corJanela,
    text= "FTP Client",
    command=clicaBotaoClient,
    width="8",
    height="1"
)
botao4.place(x=264, y=0)

botaoSair = tk.Button(
    bg = corJanela,
    text= "Sair",
    command=exit,
    width="8",
    height="1"
)
botaoSair.place(x=352, y=0)

botaoServer = tk.Button(
    window,
    bg = corJanela,
    text= "Ouvir",
    command=clicaBotaoServer,
    width="10"
)

botaoMatar = tk.Button(
    window,
    bg = corJanela,
    text= "Matar",
    command=FechaServer,
    width="10"
)

butaos = [botaoHost, botaoClient, botao3, botao4, botaoSair, botaoServer, botaoMatar, botaoArquivo]

labelProcuradorArquivo = tk.Label(
    window,
    width= 100,
    height= 4,
    fg = "grey"
)

ftp()

window.resizable = (False, False)

threadJanlea = Thread(target=window.mainloop())

#reactor.run()
threadJanlea.start()
