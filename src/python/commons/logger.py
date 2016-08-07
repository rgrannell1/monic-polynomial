
from systemd import journal





def log (str):

	print(str)
	journal.send(str)
