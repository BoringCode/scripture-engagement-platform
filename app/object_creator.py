class ObjectCreator:
	def __init__(self, sqlite_row):
		self.values_dict = self.make_dict_from_values(sqlite_row)
		self.__dict__.update(self.values_dict)

	def make_dict_from_values(self, sqlite_row):
		keys = sqlite_row.keys()
		values_d = {}
		for key in keys:
			values_d[key] = sqlite_row[key]
		return values_d
