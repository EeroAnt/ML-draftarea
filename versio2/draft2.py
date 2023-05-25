import pandas
import numpy as np
import aktivaatiofunktiot.activation_functions as af

class LM_model:
    #Luodaan neuroverkko. Annetaan parametreja ja tallennetaan piilotetut kerrokset listaan yhteensopivina matriisei
    def __init__(self, learning_rate, number_of_weight_matrices):
        self.LR = learning_rate
        self.I_dim = int(input("Syötteen dimensio: "))
        self.weight_matrices = []
        self.biases = []
        for i in range(number_of_weight_matrices):
            dim = int(input("Seuraavan kerroksen dimensio: "))
            if i == 0:
                self.weight_matrices.append(np.random.uniform(-1, 1, (dim, self.I_dim)))
                prev_dim = dim
            else:
                self.weight_matrices.append(np.random.uniform(-1, 1, (dim, prev_dim)))
                prev_dim = dim
            self.biases.append(np.random.uniform(-1,1, (dim,1)))
        self.O_dim = int(input("Tulosteen dimensio: "))
        self.weight_matrices.append(np.random.uniform(-1, 1, (self.O_dim,prev_dim)))
        self.biases.append(np.random.uniform(-1, 1, (self.O_dim,1)))
        self.activation_function_selection()
    

    def activation_function_selection(self):
        print("Vaihtoehdot")
        print("1: Logistinen")
        print("2: ReLU")
        print("3: LReLU")
        print("4: ELU")
        print("5: arctan(x) + x")
        self.selection = int(input("Mikä funktio saisi olla? "))
    
    def activation_function(self,x):
        if self.selection == 1:     
            return af.logistic(x)
        elif self.selection == 2:
            return af.relu(x)
        elif self.selection == 3:
            return af.leaky_relu(x)
        elif self.selection == 4:
            return af.elu(x)
        elif self.selection == 5:
            return af.arctanplusone(x)
    
    def activation_function_deriv(self,x):
        if self.selection == 1:
            return af.logistic_deriv(x)
        elif self.selection == 2:
            return af.relu_deriv(x)
        elif self.selection == 3:
            return af.leaky_relu_deriv(x)
        elif self.selection == 4:
            return af.elu_deriv(x)
        elif self.selection == 5:
            return af.arctanplusone_deriv(x)

    #data ulos taulukosta
    def get_data(self, name_of_file):
        datatype = input("Is the data training or validation data? [Y/n]: ")
        self.data =pandas.read_excel(name_of_file, engine="odf")
        if datatype == "Y":
            self.output_comparison = self.data.output
            self.data = self.data.drop(['output'],axis=1)
        self.data = np.asarray(self.data)
        self.data_count = len(self.data)
    #syöte läpi verkosta
    def input(self, input):
        for layer in range(len(self.weight_matrices)):
            if layer == 0:
                preActivation = np.matmul(self.weight_matrices[layer],input)+self.biases[layer]
                postActivation = []
                for i in preActivation:
                    postActivation.append(self.activation_function(np.sum(i)))
            else:
                preActivation = np.matmul(self.weight_matrices[layer],postActivation)+self.biases[layer]
                postActivation = []
                for i in preActivation:
                    postActivation.append(self.activation_function(np.sum(i)))
        return postActivation
    #least-squares-loss-funktio:
    def loss_function(self, input, expected_output):
        output = self.input(input)
        loss = []
        for i in range(len(output)):
            loss.append(output[i]-expected_output[i])
        return 0.5*np.linalg.norm(loss)**2