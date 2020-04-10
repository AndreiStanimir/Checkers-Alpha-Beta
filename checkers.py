from logging import setLogRecordFactory
import time
import random
from copy import copy
from copy import deepcopy

class Joc:
    """
    Clasa care defineste jocul. Se va schimba de la un joc la altul.
    """
    NR_COLOANE = 8
    NR_LINII = 8

    SIMBOLURI_JUC = ['a', 'n']  # ['G', 'R'] sau ['X', '0']
    JMIN = None  # 'R'
    JMAX = None  # 'G'
    GOL = '.'

    get_opponent={'A':['n','N'],
                  'a':['n','N'],
                  'N':['a','A'],
                  'n':['a','A']}

    def __init__(self, tabla=None):
        self.matr = tabla or [['.','a','.','a','.','a','.','a'],
                              ['a','.','a','.','a','.','a','.'],
                              ['.','a','.','a','.','a','.','a'],
                              ['.','.','.','.','.','.','.','.'],
                              ['.','.','.','.','.','.','.','.'],
                              ['n','.','n','.','n','.','n','.'],
                              ['.','n','.','n','.','n','.','n'],
                              ['n','.','n','.','n','.','n','.']]
        self.nr_piese_albe = 12
        self.nr_piese_negre = 12

    def final(self,jucator):
        # sau 'False' daca nu s-a terminat jocul
        #has_moves_a = False
        #has_moves_n = False
        #has_moves=False
        for i in range(Joc.NR_COLOANE):
            for j in range(Joc.NR_COLOANE):
                #if self.matr[i][j].isalpha():
                if self.matr[i][j].lower() ==jucator:
                    lista_mutari = self.mutari_piesa(i, j)
                    if len(lista_mutari) > 0:
                        return False
                        # if self.matr[i][j] in ['a', 'A']:
                        #     has_moves_a = True
                        # else:
                        #     has_moves_n = True
        #if not has_moves:
        return jucator

    def mutari_piesa(self, l, c, must_move = False):
        lista_mutari = []


        if self.matr[l][c].isupper():
            must_move = self.white_check_capture(l,c, must_move, lista_mutari)
            must_move = self.black_check_capture(l,c, must_move, lista_mutari)
            if must_move:
                return must_move,lista_mutari
            indicies = [(1, 1), (1, -1),(-1, 1), (-1, -1)]
            for x, y in indicies:
                if 0 <= l + x < Joc.NR_LINII and 0 <= c + y < Joc.NR_COLOANE:
                    if self.matr[l + x][c + y] == '.':
                        lista_mutari.append((l + x, c + y))

        if self.matr[l][c] == 'a':
            must_move = self.white_check_capture(l,c, must_move, lista_mutari)
            if must_move:
                return must_move,lista_mutari
            indicies = [(1, 1), (1, -1)]
            for x, y in indicies:
                if 0 <= l + x < Joc.NR_LINII and 0 <= c + y < Joc.NR_COLOANE:
                    if self.matr[l + x][c + y] == '.':
                        lista_mutari.append((l + x, c+ y))
        elif self.matr[l][c] == 'n':
            must_move = self.black_check_capture(l,c, must_move, lista_mutari)
            if must_move:
                return must_move,lista_mutari
            indicies = [(-1, 1), (-1, -1)]
            for x, y in indicies:
                if 0 <= l + x < Joc.NR_LINII and 0 <= c + y < Joc.NR_COLOANE:
                    if self.matr[l + x][c + y] == '.':
                        lista_mutari.append((l + x, c+y))
        return must_move,lista_mutari

    def black_check_capture(self, l,c, must_move, lista_mutari):
        indicies = [(-2, 2), (-2, -2)]
        for x, y in indicies:
            if 0 <= l + x < Joc.NR_LINII and 0 <= c + y < Joc.NR_COLOANE:
                if self.matr[l + x][c + y] == '.' and self.matr[l + x//2][c + y // 2] in self.get_opponent[self.matr[l][c]]:
                    must_move = True
                    lista_mutari.append((l + x, c+y))
        return must_move

    def white_check_capture(self, l,c, must_move, lista_mutari):
        # verific daca poate captura
        indicies = [(2, 2), (2, -2)]
        for x, y in indicies:
            if 0 <= l + x < Joc.NR_LINII and 0 <= c + y < Joc.NR_COLOANE:
                if self.matr[l + x][c + y] == '.' and self.matr[l + x//2][c + y // 2] in self.get_opponent[self.matr[l][c]]:
                    must_move = True
                    lista_mutari.append((l + x, c+y))
        return must_move

    def mutari(self, jucator):
        # returneaza o lista cu elemente de forma (l_s,c_s, lista )
        # unde l_s si c_s sunt coordonatele piesei care poate fi mutata
        # iar lista de pozitii contine perechi de coordonate unde se po
        l_mutari = []
        player_must_capture=False

        for l in range(Joc.NR_COLOANE):
            for c in range(Joc.NR_COLOANE):
                if self.matr[l][c].lower() == jucator:
                    must_move, mutari_gasite=self.mutari_piesa(l, c)
                    if must_move and not player_must_capture:
                        l_mutari.clear() # daca jucatorul poate captura, sterg mutarile gasite inainte, care nu erau modalitati de a captura
                        player_must_capture=True
                    if len(mutari_gasite)>0 and(must_move==player_must_capture):
                        l_mutari.append((l, c, mutari_gasite))
                        #for m in mutari_gasite:
                        # l c,
        # TO DO..........
        return l_mutari

    def nr_intervale_deschise(self, jucator):
        # un interval de 4 pozitii adiacente (pe linie, coloana, diag \ sau diag /)
        # este deschis pt "jucator" daca nu contine "juc_opus"

        juc_opus = Joc.JMIN if jucator == Joc.JMAX else Joc.JMAX
        rez = 0

        # linii
        # TO DO.....

        # coloane
        # TO DO.....

        # diagonale \
        # TO DO.....

        # diagonale /
        # TO DO.....

        return rez


    def fct_euristica(self):
        # TO DO: alte variante de euristici? .....

        # intervale_deschisa(juc) = cate intervale de 4 pozitii
        # (pe linii, coloane, diagonale) nu contin juc_opus
        self.diferenta_piese = 0
        valori_piese = {'a': -3,
                        'A': -5,
                        'n': 3,
                        'N': 5,
                        '.': 0
                        }
        for i in range(Joc.NR_COLOANE):
            for p in self.matr[i]:
                self.diferenta_piese+=valori_piese[p]
        return self.diferenta_piese

    def estimeaza_scor(self, adancime,jucator_curent):
        t_final = self.final(jucator_curent)
        if t_final == Joc.JMAX:
            return (999 + adancime)
        elif t_final == Joc.JMIN:
            return (-999 - adancime)
        elif t_final == 'remiza':
            return 0
        else:
            return self.fct_euristica()

    def __str__(self):
        sir = '  '

        for nr_col in range(ord('a'), ord('h') + 1):
            sir += chr(nr_col) + ''
        sir += '\n'

        for i in range(self.NR_COLOANE):
            sir += str(i) + '|'
            sir = sir + ''.join(self.matr[i]) + '\n'
        return sir


class Stare:
    """
    Clasa folosita de algoritmii minimax si alpha-beta
    Are ca proprietate tabla de joc
    Functioneaza cu conditia ca in cadrul clasei Joc sa fie definiti JMIN si JMAX (cei doi jucatori posibili)
    De asemenea cere ca in clasa Joc sa fie definita si o metoda numita mutari() care ofera lista cu
    configuratiile posibile in urma mutarii unui jucator
    """

    ADANCIME_MAX = None

    def __init__(self, tabla_joc: Joc, j_curent, adancime, parinte=None, scor=None):
        self.tabla_joc = tabla_joc
        self.j_curent = j_curent

        # adancimea in arborele de stari
        self.adancime = adancime

        # scorul starii (daca e finala) sau al celei mai bune stari-fiice (pentru jucatorul curent)
        self.scor = scor

        # lista de mutari posibile din starea curenta
        self.mutari_posibile = []

        # cea mai buna mutare din lista de mutari posibile pentru jucatorul curent
        self.stare_aleasa = None

    def jucator_opus(self):
        if self.j_curent == Joc.JMIN:
            return Joc.JMAX
        else:
            return Joc.JMIN

    def get_starile_urmatoare(self):
        # returneaza toate starile posibile
        l_stari_mutari=[]
        l_mutari = self.tabla_joc.mutari(self.j_curent)
        juc_opus = self.jucator_opus()
        tabla_noua=None
        for l,c,mutari in l_mutari:
            for m in mutari:
                tabla_noua=deepcopy(self.tabla_joc)
                l_stari_mutari.append(Stare(tabla_noua, juc_opus, self.adancime - 1, parinte=self))
                l_stari_mutari[-1].muta(l,c,m[0],m[1])

        return l_stari_mutari
    def muta(self,l,c,l_dest,c_dest):
        self.tabla_joc.matr[l_dest][c_dest] = self.tabla_joc.matr[l][c]
        self.promoveaza(l_dest,c_dest)
        self.tabla_joc.matr[l][c]='.'
        if abs(l_dest-l)==2: # captura
            self.tabla_joc.matr[l + (l_dest-l)//2][c+(c_dest-c)//2]='.'

    def __str__(self):
        sir = str(self.tabla_joc) + "(Juc curent: " + self.j_curent + ")\n"
        return sir
    def promoveaza(self,l,c):
        if self.tabla_joc.matr[l][c]=='a' and l==self.tabla_joc.NR_LINII-1:
            self.tabla_joc.matr[l][c]='A'
        elif self.tabla_joc.matr[l][c]=='n' and l==0:
            self.tabla_joc.matr[l][c]='N'

""" Algoritmul MinMax """


def min_max(stare):
    if stare.adancime == 0 or stare.tabla_joc.final():
        stare.scor = stare.tabla_joc.estimeaza_scor(stare.adancime)
        return stare

    # calculez toate mutarile posibile din starea curenta
    stare.mutari_posibile = stare.mutari()

    # aplic algoritmul minimax pe toate mutarile posibile (calculand astfel subarborii lor)
    mutari_scor = [min_max(mutare) for mutare in stare.mutari_posibile]

    if stare.j_curent == Joc.JMAX:
        # daca jucatorul e JMAX aleg starea-fiica cu scorul maxim
        stare.stare_aleasa = max(mutari_scor, key=lambda x: x.scor)
    else:
        # daca jucatorul e JMIN aleg starea-fiica cu scorul minim
        stare.stare_aleasa = min(mutari_scor, key=lambda x: x.scor)

    stare.scor = stare.stare_aleasa.scor
    return stare


def alpha_beta(alpha, beta, stare):
    if stare.adancime == 0 or stare.tabla_joc.final(stare.j_curent):
        stare.scor = stare.tabla_joc.estimeaza_scor(stare.adancime,stare.j_curent)
        return stare

    if alpha >= beta:
        return stare  # este intr-un interval invalid deci nu o mai procesez

    stare.mutari_posibile = stare.get_starile_urmatoare()
    if stare.j_curent == Joc.JMAX:
        scor_curent = float('-inf')

        for mutare in stare.mutari_posibile:
            # calculeaza scorul
            stare_noua = alpha_beta(alpha, beta, mutare)

            if (scor_curent < stare_noua.scor):
                stare.stare_aleasa = stare_noua
                scor_curent = stare_noua.scor
            if (alpha < stare_noua.scor):
                alpha = stare_noua.scor
                if alpha >= beta:
                    break

    elif stare.j_curent == Joc.JMIN:
        scor_curent = float('inf')

        for mutare in stare.mutari_posibile:
            stare_noua = alpha_beta(alpha, beta, mutare)

            if (scor_curent > stare_noua.scor):
                stare.stare_aleasa = stare_noua
                scor_curent = stare_noua.scor

            if (beta > stare_noua.scor):
                beta = stare_noua.scor
                if alpha >= beta:
                    break
    if stare.stare_aleasa is None:
        stare.scor=0
        return stare
    stare.scor = stare.stare_aleasa.scor

    return stare


def afis_daca_final(stare_curenta):
    # ?? TO DO:
    # de adagat parametru "pozitie", ca sa nu verifice mereu toata tabla,
    # ci doar linia, coloana, 2 diagonale pt elementul nou, de pe "pozitie"

    final = stare_curenta.tabla_joc.final(stare_curenta.j_curent)
    if (final):
        if (final == "remiza"):
            print("Remiza!")
        else:
            print("A castigat " + stare_curenta.jucator_opus())

        return True

    return False


def main():
    # initializare algoritm

    # initializare ADANCIME_MAX
    raspuns_valid = False
    joc_automat=True
    while not raspuns_valid:
        n = input("Adancime maxima a arborelui: ")

        if n.isdigit():
            Stare.ADANCIME_MAX = int(n)
            raspuns_valid = True
        else:
            print("Trebuie sa introduceti un numar natural nenul.")

    #jucatorul alege o mutare random de fiecare data
    joc_automat=input("Jucatorul joaca automat?(y/n)")
    if joc_automat=='y':
        joc_automat=True
    else:
        joc_automat=False

    tabla_curenta = Joc()
    print("Tabla initiala")
    print(str(tabla_curenta))

    # creare stare initiala
    stare_curenta = Stare(tabla_curenta, Joc.SIMBOLURI_JUC[0], Stare.ADANCIME_MAX)

    linie = -1
    coloana = -1

    while True:
        if (stare_curenta.j_curent == Joc.JMIN):
            # muta jucatorul
            raspuns_valid = False
            mutari_juc = stare_curenta.tabla_joc.mutari(stare_curenta.j_curent)
            if len(mutari_juc)==0 or mutari_juc is None:
                print("A castigat n!")
                break
            if joc_automat:
                l,c,dest=random.choice(mutari_juc)
                stare_curenta.muta(l,c,dest[0][0],dest[0][1])
                time.sleep(0)
                raspuns_valid=True
            print(mutari_juc)
            while not raspuns_valid:
                try:
                    linie = int(input("linie= "))
                    coloana = input("coloana = ")
                    coloana = ord(coloana) - ord('a')
                    # casuta goala de pe acea "coloana"
                    if 0 <= linie < Joc.NR_LINII and ( 0<=coloana<Joc.NR_COLOANE):
                        #coloana=ord(coloana)-ord('a')
                        for l,c,mutari_posibile in mutari_juc:
                            if l==linie and c==coloana:
                                if len(mutari_posibile)==1:
                                    stare_curenta.muta(l,c,mutari_posibile[0][0],mutari_posibile[0][1])
                                    break
                                print(mutari_posibile)
                                linie = input("linie = ")
                                coloana = int(input("coloana = "))
                                for m in mutari_posibile:
                                    if (linie,coloana) ==m:
                                        stare_curenta.muta(l,c,m[0],m[1])
                                        break
                        raspuns_valid=True
                    else:
                        print("Coloana invalida (trebuie sa fie un numar intre 0 si {}).".format(Joc.NR_COLOANE - 1))
                    # if ........
                    # ..........

                    # if ......
                    #    print("Toata coloana este ocupata.")

                except ValueError:
                    print("Coloana trebuie sa fie un numar intreg.")

            # dupa iesirea din while sigur am valida coloana
            # deci pot plasa simbolul pe "tabla de joc"
            #pozitie = linie * Joc.NR_COLOANE + coloana
            #stare_curenta.tabla_joc.matr[pozitie] = Joc.JMIN

            # afisarea starii jocului in urma mutarii utilizatorului
            print("\nTabla dupa mutarea jucatorului")
            print(str(stare_curenta))

            # testez daca jocul a ajuns intr-o stare finala
            # si afisez un mesaj corespunzator in caz ca da
            if (afis_daca_final(stare_curenta)):
                break

            # S-a realizat o mutare. Schimb jucatorul cu cel opus
            stare_curenta.j_curent = stare_curenta.jucator_opus()

        # --------------------------------
        else:  # jucatorul e JMAX (calculatorul)
            # Mutare calculator

            # preiau timpul in milisecunde de dinainte de mutare        
            t_inainte = int(round(time.time() * 1000))
            stare_actualizata = alpha_beta(-5000, 5000, stare_curenta)
            stare_curenta.tabla_joc = stare_actualizata.stare_aleasa.tabla_joc
            print("Tabla dupa mutarea calculatorului")
            print(str(stare_curenta))

            # preiau timpul in milisecunde de dupa mutare
            t_dupa = int(round(time.time() * 1000))
            print("Calculatorul a \"gandit\" timp de " + str(t_dupa - t_inainte) + " milisecunde.")

            if (afis_daca_final(stare_curenta)):
                break

            # S-a realizat o mutare. Schimb jucatorul cu cel opus
            stare_curenta.j_curent = stare_curenta.jucator_opus()


if __name__ == "__main__":
    main()
