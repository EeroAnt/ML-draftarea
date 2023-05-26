import versio2.draft2

x = 2#int(input("mitä ajetaan?"))
if x == 1:
    #tämä on paskaa
    import versio1.draft1
if x == 2:
    LR = 0.3#float(input("Anna learning rate: "))
    ML = 3#int(input("Montako keskikerrosta: "))
    malli = versio2.draft2.LM_model(LR,ML)
    print(malli.input([1,1,1]))
    print(malli.loss_function([1,1,1],[2,2]))
    for i in range(10):
        malli.training()
        print(malli.loss_function([1,1,1],[2,2]))