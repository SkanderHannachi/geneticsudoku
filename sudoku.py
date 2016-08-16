"""
Algorithme génétique qui résoud une grille de sudoku.
""" 
#-----------------Dépendences
import os
import random as rdm 
import numpy as np
import matplotlib.pyplot as plt 
#-----------------Constantes
NOMBRE_INDIVIDU_NXT = 1000
#-----------------Classes
class Indiv() : 
    def __init__(self,mat,metrique,lib) : 
        self.mat = mat
        self.metrique = metrique
        self.lib = lib
    def __gt__(self,autre) : 
        return self.metrique > autre.metrique
    def __repr__(self) : 
        return "métrique de {}" .format(self.metrique) +str("\n")+" et la solution est : {}" .format(self.mat)
#-----------------Modules
def RNG_diff(x,a,b) : 
    """Permet de générer un nombre aléatoire != x."""
    bl = True 
    while(bl) : 
        y = rdm.randint(a,b)
        if x != y : 
            return y 
        else : 
            bl = True

def imprt_input() : 
    """Charge la matrice a l'input et à renvoie une matrice remplie aléatoirement a la sortie"""
    V = []
    with open('matrice.txt','r') as fichier : 
        for i in range(9) : 
            f = fichier.readline()
            ll = f.split(' ')
            ll = [int(x[0]) if len(x) == 2 else int(x) for x in ll]
            V.append(ll)        
    return(V)

def fill_mat(vierge) : 
    """Remplit la liste avec une solution (ie un individu)"""
    lss=imprt_input()
    for i in range(9) : 
        for j in range(9) : 
            if lss[i][j] == 0 : 
                k = rdm.randint(1,9)
                lss[i][j]= k + 10
            else : 
                lss[i][j] = vierge[i][j]
    return lss            

def population_gen(ls) :
    """génère une liste qui contient toute la population"""
    popu=[]
    for i in range(100) :
        popu.append(fill_mat(ls))
    #print(popu)
    return popu

def couplage(ls_2,ls_1) : 
    """fait le couplage de deux solutions.(ie choisit un point de coupure et fait fusionner deux solutions choisies au hasard)""" 
    ls_porchaine_gen = ls_2
    coupure_indice = rdm.randint(0,80) 
    #print("Le point de coupure est : " + str(coupure_indice))
    col = coupure_indice%9 - 1
    lgn = coupure_indice//9 
    for i in range(0,lgn) : 
        for j in range(0,col) : 
            ls_porchaine_gen[i][j] = ls_1[i][j]
    return ls_porchaine_gen

def mutation(ls) : 
    """fait la mutation d'une solution donnée.(ie choisit un emplacement d'une façon aléatoire et remplace la valeur)"""
    val=True
    while(val) : 
        selec = rdm.randint(0,80)
        col = selec%9 - 1
        lgn = selec//9 - 1
        if ls[lgn][col] > 10 :
            ls[lgn][col] = RNG_diff(ls[lgn][col],11,19)
            val=False
        else : 
            val=True
        return ls

def NextGen_generateur(ls) : 
    """1000 individus avec 70% issus d'une mutation et 30% d'un couplage """ 
    nxt_gen=[]
    for i in range(int(NOMBRE_INDIVIDU_NXT*0.3)) : 
        sol1_index = rdm.randint(0,99)
        sol2_index = rdm.randint(0,99)
        nxt_gen.append(couplage(ls[sol1_index],ls[sol2_index]))
    for i in range(int(NOMBRE_INDIVIDU_NXT*0.7)) :
        sol1_index = rdm.randint(0,99)
        nxt_gen.append(mutation(ls[sol1_index]))
    for i in range(100) : 
        nxt_gen.append(ls[i])
    return nxt_gen
    #print(nxt_gen)
    
def Metrique_ligne(l) : 
    """Permet de calculer la métrique de la partition de la ligne à partir d'une solution selectionnée.""" 
    G = lambda ls,x : len([i for i,val in enumerate(ls) if val==x or val==x+10])  ##Nombre d'occurences dans une seule ligne.
    Sl= 0
    for v in range(1,10) : 
        for i in range(9) : 
            if G(l[i],v) == 0 : 
                cc = 1 
            else : 
                cc = G(l[i],v)
            Sl += (cc - 1)**2
    return Sl            

def Metrique_colone(l) :
    """Permet de calculer la métrique de la partition de la ligne à partir d'une solution selectionnée.Pour faciliter le travail, on inverse tout simplement la matrice et on fait appel au module précedent."""
    l_inv=[]
    for i in range(9) :
        l_inter=[]
        for j in range(9) :
            l_inter.append(l[j][i])
        l_inv.append(l_inter)
    return Metrique_ligne(l_inv)        
    
def Metrique_matrice(ls) : 
    """Permet le calcul de la métrique 3 X 3. """
    l=[]
    M = np.asarray(ls)
    a = 0
    b = 3
    Sp = 0
    for i in range(3) :
        c = 0
        d = 3
        for i in range(3) : 
            l.append(M[a:b,c:d])
            c += 3
            d += 3
        a += 3
        b += 3
    for i in range(9) : 
        m = l[i]
        for i in range(1,9) : 
            x = np.count_nonzero(m == i)
            if x ==0 : 
                x = 1
            Sp += (x-1)**2
    return Sp

def bilan(ls) : 
    """Renvoie les 100 individus à garder pour la prochaine génération"""
    R =[]
    fitness = lambda solution :  Metrique_colone(solution)+Metrique_ligne(solution)+Metrique_matrice(solution)
    for i in range(len(ls)):
        indiv = Indiv(ls[i],fitness(ls[i]),i)
        R.append(indiv)
    R.sort()
    return R[:100]
#---------------------------programme principal    
def main() : 
    inp = imprt_input()        
    L = population_gen(inp) ##ls est une solution unique
    N = NextGen_generateur(L)
    F = bilan(N)
    j = 1
    Y =[]
    while j<50 : 
        nm = []
        print("Generation N° : "+str(j))
        for i in range(100) : 
            nm.append(F[i].mat) 
        N = NextGen_generateur(nm)
        F = bilan(N)
        print("COMPUTING ")
        j += 1
        Y.append(F[0].metrique) 
        if F[0].metrique == 0 : 
            print("SOLUTION TROUVÉE")
            print("~~~~~~~~~~~~~~~~")
            print(F[0])
    plt.plot(range(len(Y)),Y)
    plt.show()

if __name__ == '__main__':
    main()


