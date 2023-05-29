import pandas
import numpy as np
import aktivaatiofunktiot.activation_functions as af

class LM_model:
    #Luodaan neuroverkko. Annetaan parametreja ja tallennetaan piilotetut kerrokset listaan yhteensopivina matriisei
    def __init__(self, learning_rate, number_of_weight_matrices):
        self.LR = learning_rate
        self.I_dim = 3#int(input("Syötteen dimensio: "))
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
            self.biases.append(np.random.uniform(-1,1, (dim,)))
        self.O_dim = 1#int(input("Tulosteen dimensio: "))
        self.weight_matrices.append(np.random.uniform(-1, 1, (self.O_dim,prev_dim)))
        self.biases.append(np.random.uniform(-1, 1, (self.O_dim,)))
        self.activation_function_selection()
    

    def activation_function_selection(self):
        print("Vaihtoehdot")
        # print("1: Logistinen")
        # print("2: ReLU")
        # print("3: LReLU")
        # print("4: ELU")
        # print("5: arctan(x) + x")
        # print("6: Identiteetti")
        self.selection = 5#int(input("Mikä funktio saisi olla? "))
    
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
            return af.arctan(x)
        elif self.selection == 6:
            return af.id(x)
    
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
            return af.arctan_deriv(x)
        elif self.selection == 6:
            return af.id_deriv(x)

    #data ulos taulukosta
    def get_data(self, name_of_file):
        self.data =pandas.read_excel(name_of_file, engine="odf")
        self.output_comparison = self.data.output
        self.data = self.data.drop(['output'],axis=1)
        self.data = np.asarray(self.data)
        self.data_count = len(self.data)
    
    #syöte läpi verkosta
    def input(self, input):
        self.postActivations_temp = []
        for layer in range(len(self.weight_matrices)):
            if layer == 0:
                preActivation = np.matmul(self.weight_matrices[layer],input)+self.biases[layer]
                postActivation = []
                for i in preActivation:
                    postActivation.append(self.activation_function(np.sum(i)))
                self.postActivations_temp.append(np.array(postActivation))
            elif layer <len(self.weight_matrices)-1:
                preActivation = np.matmul(self.weight_matrices[layer],postActivation)+self.biases[layer]
                postActivation = []
                for i in preActivation:
                    postActivation.append(self.activation_function(np.sum(i)))
                self.postActivations_temp.append(np.array(postActivation))
            else:
                preActivation = np.matmul(self.weight_matrices[layer],postActivation)+self.biases[layer]
                postActivation = []
                for i in preActivation:
                    postActivation.append(self.activation_function(np.sum(i))) #mahdollisesti eri funktio loppuun
                self.postActivations_temp.append(np.array(postActivation))
        self.postActivations_temp.reverse()
        return postActivation
    
    #least-squares-loss-funktio:
    def loss_function(self, input, expected_output):
        output = self.input(input)
        loss = []
        for i in range(len(output)):
            loss.append(output[i]-expected_output) #täällä kans 1D
        return 0.5*np.linalg.norm(loss)**2
    
    def activation_func_derivs(self):
        activations_function_derivatives = []
        for vector in self.postActivations_temp:
            derivative = np.zeros((len(vector),len(vector)))
            for i in range(len(vector)):
                derivative[i][i]=self.activation_function_deriv(vector[i])
            activations_function_derivatives.append(derivative)
        return activations_function_derivatives

    def loss_function_deriv(self,expected_output):
        loss_function_deriv = []
        for i in range(len(self.postActivations_temp[0])):
            loss_function_deriv.append(self.postActivations_temp[0][i]-expected_output) #täällä huomio, että nyt output on 1D
        return loss_function_deriv

    def derivation(self,sampledata,expected_output):
        self.matrix_derivatives = []
        self.bias_derivatives = []
        act_fnc_ds = self.activation_func_derivs()
        n = len(self.weight_matrices)
        for i in range(n):
            if i == 0:
                self.bias_derivatives.append(np.matmul(self.loss_function_deriv(expected_output),act_fnc_ds[i]))
                self.matrix_derivatives.append(np.matmul(self.postActivations_temp[i],self.bias_derivatives[i]))
            elif i < n-1:
                self.bias_derivatives.append(np.matmul(self.bias_derivatives[i-1],np.matmul(self.weight_matrices[n-i],act_fnc_ds[i])))
                self.matrix_derivatives.append(np.matmul(self.postActivations_temp[i],self.bias_derivatives[i]))
            else:
                self.bias_derivatives.append(np.matmul(self.bias_derivatives[i-1],np.matmul(self.weight_matrices[n-i],act_fnc_ds[i])))
                last_matrix = self.bias_derivatives[i].reshape((len(self.bias_derivatives[i]),1))@sampledata.reshape((1,len(sampledata)))
                self.matrix_derivatives.append(last_matrix)
        self.matrix_derivatives.reverse()
        self.bias_derivatives.reverse()

    def training(self,dataset):
        self.get_data(dataset)
        matrix_corrections = []
        bias_corrections = []
        counter = 0
        n = len(self.weight_matrices)
        for i in range(n):
            matrix_corrections.append(np.zeros((len(self.weight_matrices[i]),len(self.weight_matrices[i][0]))))
            bias_corrections.append(np.zeros(len(self.biases[i])))
        for sample in range(len(self.data)):
            counter += 1
            self.input(self.data[sample])
            self.derivation(self.data[sample],self.output_comparison[sample])
            for j in range(n):
                matrix_corrections[j] = np.add(matrix_corrections[j], self.matrix_derivatives[j])
                bias_corrections[j] = np.add(bias_corrections[j], self.bias_derivatives[j])
        for i in range(n):
            self.weight_matrices[i] = np.add(self.weight_matrices[i], -1*(self.LR/counter) * matrix_corrections[i])
            self.biases[i] = np.add(self.biases[i], (-1*self.LR/counter) * bias_corrections[i])

    def validation(self,dataset):
        self.get_data(dataset)
        amount = len(self.data)
        hits = 0
        for i in range(amount):
            output = self.input(self.data[i])
            if abs(output[0]-self.output_comparison[i])< 1:
                    hits += 1
        print(f"{hits} out of {amount} classified correctly")