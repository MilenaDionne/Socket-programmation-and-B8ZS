import socket
import time

levels = ["+", "-"]
pattern = "00000000"
encodingPatterns = ["000-+0+-", "000+-0-+"]


def bipolarAMIEncoding(data):
    # Apply bipolar AMI algorithm to the string (each 1 will be replaced by + or - alternatively)
    value = list(data)
    counter = 0
    for i in range(len(value)):
        if value[i] == "1":
            value[i] = levels[counter % 2]
            counter += 1

    return value


def encode(val):
    bitStream = bipolarAMIEncoding(val)
    bitStream = "".join(bitStream)

    while bitStream.find(pattern) >= 0:
        numberOfOneBeforePattern = bitStream.find(pattern)

        i = numberOfOneBeforePattern - 1
        while i >= 0:
            # Replace 00000000 by an encoding pattern
            if bitStream[i] == "+":
               # print(bitStream[i])
                bitStream = bitStream.replace(pattern, encodingPatterns[1], 1)

                i = -1

            elif bitStream[i] == "-":

                bitStream = bitStream.replace(pattern, encodingPatterns[0], 1)

                i = -1

            i -= 1

    return bitStream


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('0.0.0.0', 8080))
# client.send("Client Connecting to Server<br>")
# from_server = client.recv(4096)
# print(from_server)
while True:
    value = input("Please enter a string:\n")
    data = str(value)

    client.send("Demande d'envoi")

    print("Demande d'envoi")

    from_server = client.recv(4096)
    print(from_server)
    if from_server == "Pret a recevoir":
        client.send(encode(data))
    else:
        break
    print("Sent to server: " + data + "\n")
client.close()
