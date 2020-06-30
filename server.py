import socket
import time

pattern = "00000000"
encodingPatterns = ["000-+0+-", "000+-0-+"]


def decode(val):
    value = val
    # Replace any encoding pattern found in the string by "00000000"
    value = value.replace(encodingPatterns[0], pattern,
                          value.count(encodingPatterns[0]))
    value = value.replace(encodingPatterns[1], pattern,
                          value.count(encodingPatterns[1]))
    # Replace + and - by 1
    value = value.replace("+", "1", value.count("+"))
    value = value.replace("-", "1", value.count("-"))
    return value


serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serv.bind(('0.0.0.0', 8080))
serv.listen(5)
while True:
    conn, addr = serv.accept()

    while True:
        from_client = ''
        data = conn.recv(4096)

        if not data:
            print("Error")
            break
        from_client += data
        # print(from_client)
        if from_client == "Demande d'envoi":
            print(conn.send("Pret a recevoir"))

        data = conn.recv(4096)
        if not data:
            print("Error")
            break
        from_client = "" + data
        print("Data received from client: " + data)

        print("Decoded Data: " + decode(from_client) + "\n")
        #conn.send("I am SERVER\n")
    conn.close()
    print('client disconnected')
