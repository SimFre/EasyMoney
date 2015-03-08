
class Test:
	ost = None

	def __init__(self, message):
		self.ost = message
		print("Construct", self.ost)

	def __enter__(self):
		print("Enter", self.ost)
		return self

	def __exit__(self, type, value, traceback):
		print("Exit", self.ost)


t1 = Test("T1")

with Test("T2") as t2:
	pass

with Test("T3") as t3:
	print("Within", t3.ost)

