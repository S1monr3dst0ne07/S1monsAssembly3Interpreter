"""
Acc - Accumolator
Reg - Register
mem - Memory

8-Bit Maschin
4-Bit Memory length

set attr - set attr into Reg

add none - Acc = Acc + Reg
sub none - Acc = Acc - Reg
shg none - Acc = Acc shifted greater
shs none - Acc = Acc shifted smaller

lor none - Acc = Acc (logical or) Reg
and none - Acc = Acc (logical and) Reg
xor none - Acc = Acc (logical xor) Reg
not none - Acc = Acc (logical not)

lDA attr - Load mem at attr into Acc
lDR attr - Load mem at attr into Reg
sAD attr - Save Acc into mem at attr
sRD attr - Save Reg into mem at attr

lPA atrr - Load mem pointed to by mem at attr into Acc
lPR atrr - Load mem pointed to by mem at attr into Reg
sAP atrr - Save Acc into mem pointed to by mem at attr
sRP atrr - Save Reg into mem pointed to by mem at attr

out attr - outputs mem at attr
inp attr - inputs  mem at attr

lab attr - define lable
got attr - goto attr
jm0 attr - goto attr if Acc = 0
jmA attr - goto attr if Acc = Reg

jmG attr - goto attr if Acc > Reg (jmG for jump great)
jmL attr - goto atrr if Acc < Reg (jmL for jump less)

jmS attr - goto attr as subroutine (pc gets push to stack)
ret none - return from subroutine (stack gets pop to pc)

pha none - push Acc to stack
pla none - pull from stack to Acc


brk none - stops programm
clr none - clears Reg and Acc
"""

 
class _Error(Exception):
    def __init__(self, error):
        self.error = error
        
    def __str__(self):
        return self.error


 
class cMain:
    def __init__(self):
        self.xFile = ""

        self.xReg = 0
        self.xAcc = 0
        
        self.xMem = [0 for i in range(255)]
        
        self.xStack = []
        
        
        self.xProgrammIndex = 0
        self.xLables = {}
        
        self.xTotalIndex = 0
            
    def ParseLables(self, xCode):
        for xI in range(len(xCode)):
            xLine = xCode[xI]
            
            if xLine.split(" ")[0] == "lab" and len(xLine.split(" ")) > 1:
                self.xLables[str(xLine.split(" ")[1])] = str(xI)
            

                
    def Interpret(self):
        
        xCode = self.xFile.split("\n")
        self.ParseLables(xCode)
        
        while self.xProgrammIndex < len(xCode):
            
            xLine = xCode[self.xProgrammIndex]
            
            xInst = None
            xAttr = None
            
            #get inst and attr
            if len(xLine.split(" ")) > 0:
                xInst = xLine.split(" ")[0]
            
            if len(xLine.split(" ")) > 1:
                xAttr = xLine.split(" ")[1]
            
            #print("Inst: " + str(xInst))
            
            #execute inst
            if xInst == "set":
                self.xReg = int(xAttr)
                
            elif xInst == "add":
                self.xAcc += self.xReg
            
            elif xInst == "sub":
                self.xAcc -= self.xReg
            
            elif xInst == "shg":
                self.xAcc *= 2
                
            elif xInst == "shs":
                self.xAcc //= 2
            
            elif xInst == "lor":
                self.xAcc = self.xAcc | self.xReg

            elif xInst == "and":
                self.xAcc = self.xAcc & self.xReg

            elif xInst == "xor":
                self.xAcc = self.xAcc ^ self.xReg

            elif xInst == "not":
                xInverted = []
                for xI in list(bin(self.xAcc)[2:]):
                    if xI == "0":
                        xInverted.append("1")
                    
                    elif xI == "1":
                        xInverted.append("0")
                                        
                self.xAcc = int("".join(xInverted), 2)

                
            
            elif xInst == "lDA":
                self.xAcc = self.xMem[int(xAttr)]
            
            elif xInst == "lDR":
                self.xReg = self.xMem[int(xAttr)]
            
            elif xInst == "sAD":
                self.xMem[int(xAttr)] = self.xAcc
            
            elif xInst == "sRD":
                self.xMem[int(xAttr)] = self.xReg
            
            elif xInst == "lPA":
                self.xAcc = self.xMem[self.xMem[int(xAttr)]]
            
            elif xInst == "lPR":
                self.xReg = self.xMem[self.xMem[int(xAttr)]]

            elif xInst == "sAP":
                self.xMem[self.xMem[int(xAttr)]] = self.xAcc
            
            elif xInst == "sRP":
                self.xMem[self.xMem[int(xAttr)]] = self.xReg

            
            
            elif xInst == "out":
                xOut = self.xMem[int(xAttr)]
                print(xOut)
            
            elif xInst == "inp":
                xInput = int(input(">>>"))
                self.xMem[int(xAttr)] = xInput
            
            elif xInst == "got":
                self.xProgrammIndex = int(self.xLables[str(xAttr)])
                continue
            
            elif xInst == "jm0":
                if self.xAcc == 0:
                    self.xProgrammIndex = int(self.xLables[str(xAttr)])
                    continue
                
                
            elif xInst == "jmA":
                if self.xAcc == self.xReg:
                    self.xProgrammIndex = int(self.xLables[str(xAttr)])
                    continue
            
            elif xInst == "jmG":
                if self.xAcc > self.xReg:
                    self.xProgrammIndex = int(self.xLables[str(xAttr)])
                    continue
            
            elif xInst == "jmL":
                if self.xAcc < self.xReg:
                    self.xProgrammIndex = int(self.xLables[str(xAttr)])
                    continue
            
            
                    
            elif xInst == "brk":
                break
                
            elif xInst == "clr":
                self.xReg = 0
                self.xAcc = 0
            
            elif xInst == "jmS":
                self.xStack.append((self.xProgrammIndex + 1) * 2)
                self.xProgrammIndex = int(self.xLables[str(xAttr)])
                continue
                
                
            elif xInst == "ret":
                if len(self.xStack) != 0:
                    self.xProgrammIndex = int(self.xStack.pop() / 2)
                    continue
                    
            elif xInst == "pha":
                self.xStack.append(int(self.xAcc))
                
            elif xInst == "pla":
                if len(self.xStack) != 0:
                    self.xAcc = int(self.xStack.pop())
                    

                            
            self.xProgrammIndex += 1
            self.xTotalIndex += 1
        
        print("Programm took " + str(self.xTotalIndex) + " Executes to complete")
        
        if m.MemDump:
            print(self.xMem)
        
if __name__ == '__main__':
    import sys, os
    xArgv = sys.argv
    xDatapath = None
    
    try:
        for xI in range(len(xArgv)):
            if xArgv[xI] == "--file":
                xDatapath = str(xArgv[xI + 1])
        
        
        xFile = open(xDatapath, "r").read()
    
    except Exception:
        print("Error while loading file")
        exit()
        
    try:
        m = cMain()
        m.MemDump = "--dump" in xArgv
        m.xFile = xFile
        
        m.Interpret()
            
                
    except Exception:
        raise _Error("Error")
    
    
    