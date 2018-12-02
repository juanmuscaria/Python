#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Criador por: juanmuscaria
# Um package tracker para ver e manipular as informações
# sendo passada entre seu client (jogo talvez) e o servidor
# Para instalar as bibliotecas use:
# sudo python -m pip install socket (no Windows acho que é só python -m pip install <lib> em modo administrador)
# sudo python -m pip install thread
# sudo python -m pip install colorama
# acho que o sys e o cmd já vem por padrão,mas se não tiver é só usa o comando acima só que com o o nome das libs
# Eu usei o python 2.7, não faço a menor ideia se vai funcionar no python 3.
# ----------------------------------------------------------------------------------------------------------------------
import sys
import cmd
import thread
import socket
import os
from colorama import Fore, Back, Style, init
# ----------------------------------------------------------------------------------------------------------------------


def servertoclient(thread):  # Define o thread que manda as coisas do server para o client.
    while True:
        msgserver = ioServer.recv(99999)
        if ShowLog:
            if msgserver.encode("hex") in ignore:
                pass
            else:
                pass
                print Fore.LIGHTBLACK_EX, thread, host, msgserver, ' Codificada: ', msgserver.encode("hex")

        con.send(msgserver)
        if msgserver.encode("hex") in ignore:
            pass
        else:
            log.write('Server:' + msgserver.encode("hex") + '\n')
        if not msgserver:
            # print thread, 'Terminado'
            break


def clienttoserver(thread):  # Define o thread que manda as coisas do cliente para o server.
    while True:
        msgclient = con.recv(99999)
        if ShowLog:
            if msgclient.encode("hex") in ignore:
                pass
            else:
                print Fore.LIGHTBLACK_EX, thread, cliente, msgclient, ' Codificada: ', msgclient.encode("hex")

        ioServer.send(msgclient)
        if msgclient.encode("hex") in ignore:
            pass
        else:
            log.write('Client:' + msgclient.encode("hex") + '\n')
        if not msgclient:
            # print thread, 'Terminado'
            break


class CmdHandler(cmd.Cmd):  # O manipulador de comandos
    intro = 'PackageSniffer by juanmuscaria. Digite "?" para a lista de comandos\n'
    prompt = Fore.LIGHTGREEN_EX + '[PackageSniffer 1.0]'

    def do_SendToServer(self, arg):
        self.doc_header = Fore.CYAN + 'Esse comando leva um pacote em HEXADECIMAL. Ex (pacote de keep alive ):'
        print Fore.BLUE + 'Tentando mandar o seguinte pacote pro servidor:'
        print Fore.RED + arg.decode("hex")
        try:
            ioServer.send(arg.decode("hex"))
        except:
            print Fore.RED + 'Ocorreu um erro ao mandar o pacote! Conexão não estabelecida ou erro interno.'

    def do_SendToClient(self, arg):
        self.doc_header = Fore.CYAN + 'Esse comando leva um pacote em HEXADECIMAL. Ex (pacote de keep alive ):'
        print Fore.BLUE + 'Tentando mandar o seguinte pacote pro cliente:'
        print Fore.RED + arg.decode("hex")
        try:
            con.send(arg.decode("hex"))
        except:
            print Fore.RED + 'Ocorreu um erro ao mandar o pacote! Conexão não estabelecida ou erro interno.'

    def do_decode(self, arg):
        print Fore.BLUE + 'Pacote decodificado:'
        print Fore.RED + arg.decode("hex")

    def do_ShowLog(self, arg):
        global ShowLog
        if ShowLog:
            print Fore.BLUE + 'Parando de mostrar os pacotes!'
            ShowLog = False
        else:
            print Fore.BLUE + 'Mostrando os pacotes!'
            ShowLog = True

    def do_exit(self, arg):
        print Fore.BLUE + 'Bye!'
        thread.interrupt_main()


def cmdloop(thread):
    CmdHandler().cmdloop()


# ----------------------------------------------------------------------------------------------------------------------
#  Boa sorte tentando entender isso tudo.
init()
thread.start_new_thread(cmdloop, ("Thread-3", ))  # loop de comando
server = '192.168.15.225'  # Ip do server que você irá se conectar.
porta = 8080   # Porta do server que você ira se conectar.
host = (server, porta)
ShowLog = False
ioServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ioMc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ioMc.bind(('localhost', 12345))  # Para se conectar nesse server use localhost:12345 ou 127.0.0.1:12345
log = open("log.txt", "ab")  # Um arquivo que vai ficar todos os pacotes recebidos/enviados.
log.write('Iniciando\n')
ignore = ['020301', '020300']


ioMc.listen(1)  # Espera uma conexão no localhost:12345
con, cliente = ioMc.accept()  # Aceita a conexão.

ioServer.connect(host)  # Conecta no servidor alvo.
thread.start_new_thread(servertoclient, ("Thread-1", ))  # Inicia os threads dos sniffersd
thread.start_new_thread(clienttoserver, ("Thread-2", ))
# ----------------------------------------------------------------------------------------------------------------------
# Entra em um loop infinito, se algum erro acontecer ele irá corrigir.
while True:
    if thread._count() < 3:
        ioMc.listen(1)
        con, cliente = ioMc.accept()
        ioServer.close()
        ioServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ioServer.connect(host)
        thread.start_new_thread(servertoclient, ("Thread-1",))
        thread.start_new_thread(clienttoserver, ("Thread-2",))
        # thread.start_new_thread(cmdloop, ("Thread-3",))
