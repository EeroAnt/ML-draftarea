def elementwise_error_approximation(x):
	return x[0] * x[1]**(-0.5)


if __name__ == '__main__':
	print(elementwise_error_approximation([944.4529418945312, 3]))
