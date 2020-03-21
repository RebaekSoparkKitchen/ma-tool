import time
start0 = time.time()
from Module import Module, Conversation
end0 = time.time()


start = time.time()
m = Conversation()
end = time.time()
print('I import the third party module using', str(end0-start0), 'seconds.')
print('I run this program using', str(end-start), 'seconds.')
m.say_hi()

m.order_report()



