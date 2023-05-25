import versio2.draft2

x = int(input("mitä ajetaan?"))
if x == 1:
    import versio1.draft1
if x == 2:
    LR = float(input("Anna learning rate: "))
    ML = int(input("Montako keskikerrosta: "))
    versio2.draft2.LM_model(LR,ML)
