import statistics as st

def t_test(ar1, ar2):
    m1 = st.mean(ar1)
    s1 = st.stdev(ar1)
    f1 = s1**2 / len(ar1)

    m2 = st.mean(ar2)
    s2 = st.stdev(ar2)
    f2 = s2**2 / len(ar2)

    return (m1 - m2) / st.sqrt(f1 + f2)
