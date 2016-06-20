import zmq
import sys

context = zmq.Context()
socket = context.socket(zmq.SUB)

print "collecting updates from weather server..."
socket.connect("tcp://localhost:5566")

zip_filter = sys.argv[1] if len(sys.argv) > 1 else "10001"

if isinstance(zip_filter,bytes):
    zip_filter = zip_filter.decode('ascii')

socket.setsockopt_string(zmq.SUBSCRIBE, zip_filter)

total_temp = 0
for update_nbr in range(5):
    print update_nbr
    string = socket.recv_string()
    print string
    zipcode, temperature, relhumidity = string.split()
    total_temp += int(temperature)

print "average temperature for zipcode '%s' was %dF" % (zip_filter, total_temp/update_nbr)
