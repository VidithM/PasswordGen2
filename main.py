import os, pickle
from manager import Manager


mgr = None

try:
	storage = open('contents.bin', 'rb')
	mgr = pickle.load(storage)
	storage.close()
except:
	print("Looks like you don't have a profile set up. Let's do that now")
	print('Enter a master password: ')
	newpass = input()
	if(newpass == 'forgot'):
		print('Cannot use \'forgot\'')
		quit()
	print('Enter new hint')
	newhint = input()

	mgr = Manager()
	mgr.setConfig(newpass, newhint)
	storage = open('contents.bin', 'wb')
	storage.write(pickle.dumps(mgr))
	storage.close()
	print('Restart to use')
	quit()

master = input('Enter master password or type \'forgot\'\n')
if(master == 'forgot'):
	print('Hint', mgr.getHint())

elif(mgr.authenticate(master)):
	mgr.navigateDirectories(master)
	storage = open('contents.bin', 'wb')
	storage.write(pickle.dumps(mgr))
	storage.close()

else:
	print('Incorrect master password')

