from services.training import test_with_plots

network_structure = [
	(120, 'relu'),
	(120, 'relu'),
	(120, 'relu'),
	3
]


test_with_plots(num_epochs=3, k=4, network_structure=network_structure)
