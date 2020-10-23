from termcolor import cprint
from cryptography.fernet import Fernet

'''
Each directory can be thought of as a node in a tree
'''

class Directory:
    def __init__(self, name, parent):
        self.name = name
        self.parent = parent
        self.children = []
        self.psswrds = []
    
    def addPassword(self, title, password, key):
        f = Fernet(key)
        self.psswrds.append(title)
        self.psswrds.append(f.encrypt(password.encode()))

    def getPath(self):
        curr = self
        res = ''
        while(not curr.parent == None):
            res = '->' + curr.name + res
            curr = curr.parent
        res = curr.name + res
        return res

    def showContents(self, key):
        f = Fernet(key)
        cprint('Current path: ' + self.getPath(), 'yellow')
        if(len(self.psswrds) == 0 and len(self.children) == 0):
            cprint('No contents', 'green')
            return
        cprint('Passwords:', 'green')
        for idx in range(len(self.psswrds)):
            if(idx % 2 == 0):
                cprint(self.psswrds[idx], 'cyan')
            else:
                print(f.decrypt(self.psswrds[idx]).decode())
        
        cprint('Subfolders:', 'green')
        for child in self.children:
            print(child.name)
    
    def changePassword(self, key, newkey):
        f = Fernet(key)
        newf = Fernet(newkey)
        for idx in range(1, len(self.psswrds), 2):
            psswrd = f.decrypt(self.psswrds[idx]).decode()
            self.psswrds[idx] = newf.encrypt(psswrd.encode())
    
        for child in self.children:
            child.changePassword(key, newkey)

    def getParent(self):
        return self.parent

    def getChild(self, name):
        for idx in self.children:
            if(idx.getName() == name):
                return idx
        return None

    def rmDir(self, name):
        self.children.remove(self.getChild(name))

    def makeDir(self, name):
        for child in self.children:
            if(child.name == name):
                return False
        add = Directory(name, self)
        self.children.append(add)
        return True

    def getName(self):
        return self.name

if __name__ == '__main__':
    test = Directory('root', None)
    print(test.getChild('test'))
