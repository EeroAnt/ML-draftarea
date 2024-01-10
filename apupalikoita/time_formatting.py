def time_formatter(seconds):
	string_to_return = ""
	hours = int(seconds//3600)
	if hours > 0:
		string_to_return += f"{hours} h "
	minutes = int((seconds - hours*3600)//60)
	if hours > 0 or minutes > 0:
		string_to_return += f"{minutes} min "
	seconds = seconds - hours*3600 - minutes*60
	string_to_return += f"{'{:.2f}'.format(seconds)} s" 
	return string_to_return


if __name__ == "__main__":
	print(time_formatter(360413.1234341243124))