import hashlib
from directory import Directory

class Manager():
    def __init__(self):
        self.root = Directory('root', None)
    
    def navigateDirectories(self, psswrd):
        curr = self.root
        key = (hashlib.sha256(psswrd.encode()).hexdigest()[0:43] + '=').encode()
        verbose = True
        while(True):
            if(verbose):
                curr.showContents(key)
                verbose = False
            print('\nTo edit this folder, type (1). To go to a subfolder, type its name. To change your password, type (2). To go up a level, type \'..\'. To quit, type (3)')
            op = input()
            if(op == '1'):
                print('Choose an option:\n(1) Delete this folder\n(2) Add a folder\n(3) Add a password')
                op = int(input())
                if(op == 1):
                    if(curr == self.root):
                        print('You cannot delete the root')
                    else:
                        name = curr.getName()
                        curr = curr.getParent()
                        curr.rmDir(name)
                        verbose = True
                if(op == 2):
                    name = input('Enter directory name: ')
                    if(not curr.makeDir(name)):
                        print('Folder name already exists!')
                    else:
                        verbose = True 
                if(op == 3):
                    title = input('Enter a title for the password: ')
                    psswrd = input('Enter your password: ')
                    curr.addPassword(title, psswrd, key)
                    verbose = True
                
            elif(op == '2'):
                newpass = ''
                while(True):
                    newpass = input('Enter a new password: ')
                    if(newpass == 'forgot'):
                        print('Cannot use '/forgot/'. Try again!')
                    else:
                        break
                newhint = input('Enter a new hint: ')
                head = curr
                while(not head.parent == None):
                    head = head.parent
            
                newkey = (hashlib.sha256(newpass.encode()).hexdigest()[0:43] + '=').encode()
                head.changePassword(key, newkey)
                self.hint = newhint
                self.hash = hashlib.sha256((newpass + self.salt).encode()).hexdigest()
                key = newkey
                print('Password change successful')
            elif(op == '3'):
                break
            elif(op == '..'):
                if(curr == self.root):
                    print('You are at the root')
                else:
                    curr = curr.getParent()
                    verbose = True
            else:
                goto = curr.getChild(op)
                if(goto == None):
                    print('That folder does not exist!')
                else:
                    verbose = True
                    curr = goto

    def resetPassword(self, newpass):
        pass

    def setConfig(self, salt, hash, hint):
        self.hash = hash 
        self.salt = salt
        self.hint = hint 

    def authenticate(self, psswrd):
        return (hashlib.sha256((psswrd + self.salt).encode()).hexdigest() == self.hash)

    def getHint(self):
        return self.hint
    
         