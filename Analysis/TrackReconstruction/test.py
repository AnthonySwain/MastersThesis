import os 
    
# path 
path = "/home/anthony/MastersThesis/Data/DumpFolder"
    
# Create the directory 
# 'GeeksForGeeks' in 
# '/home / User / Documents' 
try: 
    os.mkdir(path) 
except OSError as error: 
    print(error)  
    
try: 
    os.mkdir(path + "2")
except OSError as error: 
    print(error)  