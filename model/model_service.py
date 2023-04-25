from builder.assembler import Assembler

assembler = None

def Init_ModelService():
    """
    初始化 
    """
    global assembler 
    assembler = Assembler()
    return assembler
    
def Load_Model_File(modelPath:str):
    assembler.load_file(modelPath)

def Init_Model():
    assembler.init_model()
    
def Create_Model():
    assembler.assemble()
     