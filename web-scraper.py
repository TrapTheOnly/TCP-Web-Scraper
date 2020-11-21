import sys
from bs4 import BeautifulSoup
import socket
import requests
import argparse

HOST = "127.0.0.1"
PORT = 65432


class Server:
    def __init__(self):
        self.start()

    def start(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((HOST, PORT))
        sock.listen(1)
        print("[SERVER] has started")
        while True:
            sc, sockname = sock.accept()
            url = (sc.recv(128)).decode('utf-8')
            try:
                content = requests.get("https://" + url).content
                soup = BeautifulSoup(content, "html.parser")
            except:
                try:
                    content = requests.get("http://" + url).content
                    soup = BeautifulSoup(content, "html.parser")
                except:
                    content = requests.get(url).content
                    soup = BeautifulSoup(content, "html.parser")
            soup.prettify()
            pList = soup.find_all("p")
            leafCounter = 0
            for pElement in pList:
                children = pElement.findChildren()
                miniCounter = 0
                for child in children:
                    if child.name == "p":
                        miniCounter += 1
                if miniCounter == 0:
                    leafCounter += 1
            imageCounter = len(soup.find_all("img"))
            finalResult = str(imageCounter) + " " + str(leafCounter)
            sc.send(finalResult.encode('utf-8'))


class Client:
    def __init__(self, url):
        self.url = url
        self.start()

    def start(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((HOST, PORT))
        sock.send(self.url.encode('utf-8'))
        data = sock.recv(128)
        print(data.decode('utf-8'))


def main():
    parser = argparse.ArgumentParser(description='Send URL to the server')
    parser.add_argument('server', nargs='?', help='Start as server')
    parser.add_argument('client', nargs='?', help='Start as client')
    if 'client' in sys.argv:
        parser.add_argument('-p', type=str, help='URL of website')
    args = parser.parse_args()
    if 'server' in sys.argv and 'client' in sys.argv:
        parser.error("Use only one of [server, client]")
    elif 'server' in sys.argv:
        serverObj = Server()
    elif 'client' in sys.argv:
        clientObj = Client(args.p)
    else:
        parser.error("Enter one argument of [server, client]")


if __name__ == "__main__":
    main()
