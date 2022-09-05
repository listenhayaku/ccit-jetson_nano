from inspect import Attribute
from operator import attrgetter
from block import Block
import time
import threading
import random
import os

class Blockchain():
    def __init__(self):
        self.chain = []
        self.difficulty = 5
        self.blockqueue = []    # 待挖區塊
        random.seed()

        #flag
        self.STOP = int()
        self.PAUSE = int()
        self.UPDATE = int(0)    #是否有更新
        self.UPDATING = False   #是否正在更新

        #node
        self.port = int()

    def run(self,port):
        pass
        self.port = port
        genesis_block = Block("this is genesis block")
        genesis_block.timestamp = float(0)
        self.chain.append(genesis_block)

    def append_blockqueue(self,block):
        self.blockqueue.append(block)
        print("[append_blockqueue]new update,len of blockqueue is ",len(self.blockqueue))

    def remove_blockqueue(self,block):
        self.blockqueue.remove(block)
        print("[remove_blockqueue]new update,len of blockqueue is ",len(self.blockqueue))


    def print_blockqueue(self):
        print("\n[print_blockqueue]==================\n")
        for _ in self.blockqueue:
            _.print_block()
        print("\n[print_blockqueue]==================\n")
        

    def update_blockchain(self,block):#input:block
        while self.UPDATING == True: pass #有別的執行續正在更新
        self.UPDATING = True
        verify = self.verify(block)
        if(verify == True):
            self.UPDATE = 1
            for _ in self.blockqueue:
                if _.is_same_as(block):
                    self.remove_blockqueue(_)
            block.id = len(self.chain)
            self.chain.append(block)

            print("[blockchain.update_blockchain]verify successful!")
            print("[blockchain.update_blockchain]==================the appended block is")
            block.print_block()
            self.write_log_block(block,"appended")
            print("[blockchain.update_blockchain]the appended block is==================")
        else:
            print("[blockchain.update_blockchain]verify failed! ",verify)
            print("[blockchain.update_blockchain]==================the dropped block is")
            block.print_block()
            self.write_log_block(block,"dropped",debug = verify)
            print("[blockchain.update_blockchain]the dropped block is==================")
        self.UPDATING = False

    def request_ledger(self,node = None):   #和別的節點要求帳本
        if(node ==  None): print("[blockchain.request_ledger]error:plz input node!")
        else:
            node.broadcast("request_ledger")
            pass

    def verify(self,block): #input:block, output:True(bool),(str)
        #fake hash (假hash)
            #check prev_hash (檢查prev_hash欄位是否不符規則)
        if(block.prev_hash != self.chain[-1].get_blockhash()):
            return "fake prev_hash"
        
            #check current hash (檢查區塊的hash是否符合規則)
        if(block.get_blockhash()[0:self.difficulty] != '0' * self.difficulty):
            return "current hash is fake"
        #same content
        attribute = ["timestamp","nonce","prev_hash","information.data","source"]
        for _ in self.chain:
            result = _.cmp(block)   #result == ["timestamp","nonce"]
            count = 0
            for x in attribute:
                if x in result:
                    count += 1
            if count >= len(attribute):
                return "same content"

        print("[blockchain.verify]successful!")
        return True

    def print_blockchain(self):
        print("[print_blockchain]",self)
        for _ in self.chain:
            _.print_block()
            time.sleep(0.5)

    def blockchain_stop(self):
        self.STOP = 1
        print("[blockchain.blockchain_stop]stop,len of blockqueue is ",len(self.blockqueue))

    def mine(self):
        if(len(self.blockqueue) >= 1):
            block_hash = self.blockqueue[0].get_blockhash()
            self.UPDATE = 0

            self.blockqueue[0].nonce = random.getrandbits(32)
            #print("[blockchain.mine]original nonce = ",self.blockqueue[0].nonce)
            self.blockqueue[0].prev_hash = str(self.chain[-1].get_blockhash())
            while block_hash[0:self.difficulty] != '0' * self.difficulty:
                try:
                    self.blockqueue[0].nonce += 1
                    block_hash = self.blockqueue[0].get_blockhash()
                except IndexError:
                    print("[blockchain.mine]IndexError!")
                if self.UPDATE == 1:
                    print("[blockchain.mine]interrupt")
                    time.sleep(1)
                    return False
                if self.STOP == 1:
                    break

            block = self.blockqueue.pop(0)
            self.update_blockchain(block)
            return block


    def write_log(self,port = 0,debug = "writelog"):
        result = os.getcwd().split("\\")
        #print("blockchain.result = ",result)
        if result[-1] == "blockchain":
            path = "./log/"
        elif result[-1] == "main":
            path = "../log/"  
        else:
            print("[write_log]current path error!")    
        #print("[blockchain.write_log]result = ",result)
        #print("[blockchain.write_log]","{path}blockchain.log".format(path = path))
        if port == 5000:
            f = open("{path}5000/blockchain.log".format(path = path),'w')
        elif port == 5001:
            f = open("{path}5001/blockchain.log".format(path = path),'w')
        elif port == 5002:
            f = open("{path}5002/blockchain.log".format(path = path),'w')
                
        msg = str()
        for _ in self.chain:
            msg += _.print_block("write_log port:"+str(port))
        
        f.write(msg)
        f.close()

    def write_log_block(self,block,type = "droppped",debug = ""):
        result = os.getcwd().split("\\")
        if result[-1] == "blockchain":
            path = "./log/"
        elif result[-1] == "main":
            path = "../log/"  
        else:
            print("[write_log]current path error!")    
        #print("[blockchain.write_log]result = ",result)
        #print("[blockchain.write_log]","{path}blockchain.log".format(path = path))

        if self.port == 5000:
            f = open("{path}5000/verify_{type}.log".format(path = path,type = type),'a')
        elif self.port == 5001:
            f = open("{path}5001/verify_{type}.log".format(path = path,type = type),'a')
        elif self.port == 5002:
            f = open("{path}5002/verify_{type}.log".format(path = path,type = type),'a')
                
        msg = str()
        msg = block.print_block(show = False,debug = debug)
        
        f.write(msg)
        f.close()


if __name__ == "__main__":
    block1 = Block("this is block1")
    block1.id = 1
    block2 = Block("this is block2")
    block2.id = 2
    
    block1.print_block()
    blockchain = Blockchain()
    blockchain.run()
    blockchain.update_blockchain(block1)
    blockchain.update_blockchain(block2)
    print("\n\n\n")
    blockchain.print_blockchain()