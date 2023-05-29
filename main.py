import versio2.draft2

x = 2#int(input("mitä ajetaan?"))
if x == 1:
    #tämä on paskaa
    import versio1.draft1
if x == 2:
    LR = 0.7#float(input("Anna learning rate: "))
    ML = 3#int(input("Montako keskikerrosta: "))
    malli = versio2.draft2.LM_model(LR,ML)
    for i in range(1000):
        malli.training()
        if i%100 == 0:
            print(malli.validation())