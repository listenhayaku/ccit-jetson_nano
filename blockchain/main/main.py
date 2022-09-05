from node import Node
from blockchain import Blockchain
from block import Block
import time
import threading
import appendix
import os



'''
import os
print("os.environ[\"CUDA_VISIBLE_DEVICES\"] = ",os.environ["CUDA_VISIBLE_DEVICES"])
os.environ["CUDA_VISIBLE_DEVICES"] = "0"
'''


#global variable
STOP = int()    # 0 run, 1 stop
node = Node()
blockchain = Blockchain()
#golbal variable

class go_fuck_yourself():
    def __init__(self,data = (0,0,0,0,0,0,0,0,0)):
        self.data = data
        #print("init data = ",self.data)
        arr = list()
        arr.append(self.data)

    def getobj(self):
        return self
    
    def to_string(self):
        return str(self.data)
    def to_obj(self,string):
        #print("para in:",string)

        return string
    
    def go_fuck(self,string):
        #print("[go_fuck_yourself.go_fuck]======================")
        #print("[go_fuck_yourself.go_fuck]string:",string)
        if("fuck:" in string):
            #print("fuck: is in string")
            string = string.split("fuck:")
            #print(string)
            #print(string[1])    #[(9, 8, 7, 6, 5, 4, 3, 2, 1)(1, 2, 3, 4, 5, 6, 7, 8, 1)]
            string = string[1].replace("[","").replace("]","")
            #print(string)   #(9, 8, 7, 6, 5, 4, 3, 2, 1)(1, 2, 3, 4, 5, 6, 7, 8, 1)
            string = string.replace("(","")
            #print(string)
            string = string.split(")")
            string = string[0:-1]
            #print(string)   #['9, 8, 7, 6, 5, 4, 3, 2, 1', '1, 2, 3, 4, 5, 6, 7, 8, 1', '']
            data = list()
            for _ in string:
                temp = _.split(",")
                row = list()
                for x in temp:
                    row.append(int(x))
                #print(temp)
                data.append(row)
            #print("[go_fuck]",data)
            return data
        else:
            pass
            #print("fuck: is not in string")
        #print("[go_fuck_yourself.go_fuck]======================")



def init():
    #init
    print("[main.init]__name__ = ",__name__)


    t = threading.Thread(target = retriever,args = (node,))
    t.start()

    t = threading.Thread(target = miner,args = (blockchain,))
    #if node.server_port == 5000:t.start()
    t.start()


    if node.server_port == 5000:
        port = 5001
        node.client_init(port)
        port = 5002
        node.client_init(port)
    elif node.server_port == 5001:
        port = 5000
        node.client_init(port)
        port = 5002
        node.client_init(port)
    elif node.server_port == 5002:
        port = 5000
        node.client_init(port)
        port = 5001
        node.client_init(port)
    else:
        print("[main.init]unknown error!")

    print("\n======init done======\n")
    

def miner(blockchain):
    while STOP == 0:
        while len(blockchain.blockqueue) >= 1:
            block = blockchain.mine()
            if block == False:  #代表有人先挖到 有更新
                break
            block.print_block("[main.miner]I mined a block")
            node.broadcast("update//"+block.conv_block_to_str()+"//appendix//miner:node"+str(node.server_port)+"ip"+str(node.server_ip)+" ("+str(round(time.time(),2))+") "+"\\fuck:["+go_fuck_yourself((9,8,7,6,5,4,3,2,1)).to_string()+go_fuck_yourself((1,2,3,4,5,6,7,8,1)).to_string()+"]")
    pass


def retriever(node):
    global STOP
    while STOP == 0:
        data = node.server_retriever()  #if node stop, data == None
        # data = {{"msg":{"tag":tag,"content":content,"appendix":appendix}} ,"source":來源的socket物件}
        if(data == None): 
            # node stop
            break

        if(type(data) == dict):
            print("[retriever]",data)
            if data["msg"]["tag"] == "block":
                #print("[retriever]:data is block type")
                #data["msg"]["content"].print_block("call by block")
                blockchain.append_blockqueue(data["msg"]["content"])
            
            elif data["msg"]["tag"] == "cmd":
                #print("[retriever]:data is string type")
                #print("[retriever]",data["msg"]["content"],sep=":")
                if(data["msg"]["content"] == "new block"):
                    new_block(True)

                elif(data["msg"]["content"] == "request_ledger"):
                    print("[main.retriever]i received the request for ledger")

            
            elif data["msg"]["tag"] == "update":
                #print("[retriever]:data is for updating blockchain",blockchain)
                #data["msg"]["content"].print_block("call by update")
                blockchain.update_blockchain(data["msg"]["content"])

            #print("[main.retriever]appendix:",data["msg"]["appendix"])
            print("[main.retriever]miner is ",appendix.miner(data["msg"]["appendix"]),",go_fuck is:",go_fuck_yourself().go_fuck(data["msg"]["appendix"]))
        
        else:
            print("[retriever]:data is not type dict")

        pass


def new_block(auto = False):
    if auto == False:
        info = input("new block:")
        block = Block(info,node.server_ip+":"+str(node.server_port))
        for i in range(2):
            node.broadcast("block//"+block.conv_block_to_str()+"//appendix//test")
            blockchain.append_blockqueue(block)
    else:
        print("[main.new_block]:auto new_block start")
        time.sleep(1)
        count = 0
        while True:
            info = "test {count} port {port}".format(count = count,port = node.server_port)
            print("[main.new_block]info = ",info)
            block = Block(info,node.server_ip+":"+str(node.server_port))
            node.broadcast("block//"+block.conv_block_to_str()+"//appendix//test")
            blockchain.append_blockqueue(block)
            if count <= 5: count += 1
            else: break
            

if __name__ == "__main__":
    init()
    
    #flag
    STOP = 0

    #run
    blockchain.run(node.server_port)


    while STOP == 0:
        

        msg = input()   #阻塞
        node.broadcast(msg)
        
        if msg == 'exit':
            break
        elif msg == "show blockchain":
            #blockchain.print_blockchain()
            blockchain.write_log(port = node.server_port)
        elif msg == "show blockqueue":
            print(blockchain.blockqueue)
        elif msg == "show block":
            if len(blockchain.blockqueue) >= 1:
                blockchain.blockqueue[int(input("input index:"))].print_block()
            else: print("[main]there is not anything in blockqueue!")
        elif msg == "new block":
            block = new_block(True)
        elif msg == "show serverlist":
            print("[main]show serverlist:",node.server_list_client)
        elif msg == "show clientlist":
            print("[main]show clientlist:",node.client_list_server)
        elif msg == "request":
            time.sleep(1)
            blockchain.request_ledger(node)
        else:
            pass

    blockchain.write_log(port = node.server_port)   #auto show blockchain
    
    STOP = 1
    blockchain.blockchain_stop()

    time.sleep(1)
    node.stop()

    print("===end===")
    print("[main.end]blockchain.blockqueue = ",blockchain.blockqueue)
    print("[main.end]len of blockchain.blockqueue = ",len(blockchain.blockqueue))
    print("===end===")
    
'''
fuck you by chen,pin-jui
'''