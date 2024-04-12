def mode(arr):
    return max(set(arr), key=arr.count)

def simulation(M, Y, g=12):
    Y_prime = []

    MAC = []
    seen = []
    for m in M:
        if m not in seen:
            seen.append(m)
            MAC.append([m])
    for j in range(len(M)):
        for i in range(len(seen)):
            if MAC[i][0] == M[j]:
                MAC[i].append(j)
    for i in range(len(seen)):
        C = []
        for j in range(1, len(MAC[i]), g):
            C.append(MAC[i][j:j+g])
        for c in C:
            g_list = []
            for j in c:
                g_list.append(Y[j])
            mode_val = mode(g_list)
            for j in c:
                Y_prime.append(mode_val)

    LABEL = []
    seen = []
    exceptionlist = []
    dominantMACS = []
    for y in Y:
        if y not in seen:
            seen.append(y)
            LABEL.append([y])
    for j in range(len(Y)):
        for i in range(len(seen)):
            if LABEL[i][0] == Y[i]:
                LABEL[i].append(M[j])
    for i in range(len(seen)):
        if mode(LABEL[i]) not in dominantMACS:
            dominantMACS.append(mode(LABEL[i]))
        else:
            exceptionlist.append(mode(LABEL[i]))

    FinalResults = []
    for j in range(len(Y)):
        if M[j] in exceptionlist:
            FinalResults.append(Y[j])
        else:
            FinalResults.append(Y_prime[j])

    return FinalResults
