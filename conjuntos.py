#Conjuntos
# A = (1, 2 , 3, 4) ; B = (2, 3, 5, 6); C = (3, 4, 6 , 7)
# A U B
# A U C
# B U C
# A ¬ B 
# A ¬ C
# B ¬ C
A={1,2,3,4}
B={2,3,5,6}
C={3,4,6,7}

print(A==B) #comparacion
print(A|B) #union
print(A|C) 

print(A&B) #interseccion
print(A^B)