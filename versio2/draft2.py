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

    def get_data(self, name_of_file):
        datatype = input("Is the data training or validation data? [Y/n]: ")
        self.data =pandas.read_excel(name_of_file, engine="odf")
        if datatype == "Y":
            self.output_comparison = self.data.output
            self.data = self.data.drop(['output'],axis=1)
        self.data = np.asarray(self.data)
        self.data_count = len(self.data)
    
    def forward_propagation(self, input):
        for layer in range(len(self.middle_layer_weight_matrices)):
            if layer == 0:
                preActivation = np.matmul(self.middle_layer_weight_matrices[layer],input)+self.middle_layer_biases[layer]
                postActivation = []
                for i in preActivation:
                    postActivation.append(af.elu(np.sum(i)))
            else:
                preActivation = np.matmul(self.middle_layer_weight_matrices[layer],postActivation)+self.middle_layer_biases[layer]
                postActivation = []
                for i in preActivation:
                    postActivation.append(af.elu(np.sum(i)))
        preActivation = np.matmul(self.middle_to_output_weight_matrix, postActivation)+self.middle_to_output_bias
        postActivation = []
        for i in preActivation:
            postActivation.append(af.elu(np.sum(i)))
        return postActivation