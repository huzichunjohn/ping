import zmq
from random import randrange

context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind("tcp://*:5566")

while True:
    zipcode = randrange(10000, 10010)
    temperature = randrange(-80, 135)
    relhumidity = randrange(10, 60)
  
    print "%i %i %i" % (zipcode, temperature, relhumidity)
    socket.send_string("%i %i %i" % (zipcode, temperature, relhumidity))
