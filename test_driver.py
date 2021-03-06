import socket # socket
import random # random number
import time   # sleep

# constants 
IP_TX = "10.10.10.3"
PORT_TX = 5000
IP_RX = "10.10.10.2"
PORT_RX = 6002
BUFFER_SIZE = 3 * 1024
STRINGS = "=@#$^&*-_"

def string_compare(strtx, strrx):
    if len(strtx) != len(strrx):
        print("len(strtx): %d len(strrx): %d\n", len(strtx), len(strrx))
        return [False, 0]
    
    for i in range(len(strtx)):
        if ord(strtx[i]) != ord(strrx[i]):
            print("ord(strtx[i]): %d ord(strrx[i]): %d\n",
                  ord(strtx[i]), ord(strrx[i]))
            return [False, i]

    return [True, 0]

if __name__ == "__main__":
    print("UDP target tx IP:", IP_TX)
    print("UDP target tx port:", PORT_TX)
    print("UDP target rx IP:", IP_RX)
    print("UDP target rx port:", PORT_RX)
    sock_tx = socket.socket(socket.AF_INET, # Internet
                            socket.SOCK_DGRAM) # UDP

    sock_rx = socket.socket(socket.AF_INET, # Internet
                            socket.SOCK_DGRAM) # UDP
    sock_rx.bind((IP_RX, PORT_RX))

    mesg_size_max = 0
    for j in range(14, 300):
        time.sleep(0.2)
        print(j)
        message_tx = ""
        ran_num = j #random.randrange(10, 30)
        print("random number: " +  str(ran_num))        
        for i in range(ran_num):
            message_tx += STRINGS[:len(STRINGS) - len(str(i))] + str(i) + "/"
        mesg_size_max = max(len(message_tx), mesg_size_max)

        print("transmitting data with size: " + str(len(message_tx)))
        sock_tx.sendto(message_tx, (IP_TX, PORT_TX))
        
        print("waiting for a packet")
        data_rx, addr_rx = sock_rx.recvfrom(BUFFER_SIZE)

        print("received a message\n")
        # print("received message: " + data_rx, addr_rx)
        # message_rx = "|" + message_tx[1:len(message_tx)-1] + "|\n"

        # bcompare, icompare = string_compare(message_rx, data_rx)
        bcompare, icompare = string_compare(message_tx, data_rx)
        if not bcompare:
            break
    # end for
    if not bcompare:    
        print("data_rx: ", data_rx)
        print("the first difference between message_rx and data_rx is at: %d"
              % icompare)
        print("message_tx: \"{}\" ascii {}".format(message_tx[icompare], ord(message_tx[icompare])))
        print("data_rx: \"{}\" ascii {}".format(data_rx[icompare], ord(data_rx[icompare])))
    else:
        print("Congratulations your echo server works\n")
        print("the maximum transmitted data is " + str(mesg_size_max))
        print("random number: " +  str(ran_num))
