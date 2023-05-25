import pandas
import numpy as np
import aktivaatiofunktiot.activation_functions as af

class LM_model:
    #Luodaan neuroverkko. Annetaan parametreja ja tallennetaan piilotetut kerrokset listaan yhteensopivina matriiseina matriiseina
    def __init__(self, learning_rate, number_of_middle_layers):
        self.LR = learning_rate
        self.I_dim = int(input("Syötteen dimensio: "))
        self.middle_layers = []
        for i in range(number_of_middle_layers):
            dim = int(input("Seuraavan kerroksen dimensio: "))
            if i == 0:
                self.middle_layers.append(np.random.uniform(-1, 1, (self.I_dim, dim)))
                prev_dim = dim
            else:
                self.middle_layers.append(np.random.uniform(-1, 1, (prev_dim, dim)))
                prev_dim = dim
        self.O_dim = int(input("Tulosteen dimensio: "))
        self.middle_to_output = np.random.uniform(-1, 1, (prev_dim, self.O_dim))
