import pandas
import numpy as np
import aktivaatiofunktiot.activation_functions as af

class LM_model:
    #Luodaan neuroverkko. Annetaan parametreja ja tallennetaan piilotetut kerrokset listaan yhteensopivina matriisei
    def __init__(self, learning_rate, number_of_middle_layer_weight_matrices):
        self.LR = learning_rate
        self.I_dim = int(input("Syötteen dimensio: "))
        self.middle_layer_weight_matrices = []
        self.middle_layer_biases = []
        for i in range(number_of_middle_layer_weight_matrices):
            dim = int(input("Seuraavan kerroksen dimensio: "))
            if i == 0:
                self.middle_layer_weight_matrices.append(np.random.uniform(-1, 1, (dim, self.I_dim)))
                prev_dim = dim
            else:
                self.middle_layer_weight_matrices.append(np.random.uniform(-1, 1, (dim, prev_dim)))
                prev_dim = dim
            self.middle_layer_biases.append(np.random.uniform(-1,1, (dim,1)))
        self.O_dim = int(input("Tulosteen dimensio: "))
        self.middle_to_output_weight_matrix = np.random.uniform(-1, 1, (self.O_dim,prev_dim))
        self.middle_to_output_bias = np.random.uniform(-1, 1, (self.O_dim,1))