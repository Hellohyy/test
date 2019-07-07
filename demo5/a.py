str = 'hello,world'
A = [1,5.7,9]

def a(A):
    b=[]
    j = 0
    k = 1
    i = 0
    while(i < len(A)):
        b[i] = A[i]
        #(A[i] == 0 & i % 2 == 0) | (A[i] % 2 == 1 & i % 2 == 1)