import versio2.draft2

x = int(input("mitä ajetaan?"))
if x == 1:
    #tämä on paskaa
    import versio1.draft1
if x == 2:
    LR = float(input("Anna learning rate: "))
    ML = int(input("Montako keskikerrosta: "))
    malli = versio2.draft2.LM_model(LR,ML)
    print(malli.input([1,1,1]))
    print(malli.loss_function([1,1,1],[2,2]))