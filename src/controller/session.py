from model.db_connection import *

class Session:
    
    def __init__(self):
        self.login = False;
        self.username= "";
        self.permission = []
        
    def signIn(self, username, password):
        return
    
    def signOut(self):
        return
    
    # Get Variable 
    def getLogin(self):
        return self.login
    
    def getUsername(self):
        return self.username
    
    def getPermission(self):
        return self.permission