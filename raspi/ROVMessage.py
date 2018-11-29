class ROVException(Exception):
	def __init__(self, message):
		# Call the base class constructor with the parameters it needs
		super().__init__("Error: " + message)

class ROVWarning(Exception):
	def __init__(self, message):
		# Call the base class constructor with the parameters it needs
		super().__init__("Warning: " + message)