from kd_strom_struktura.vrchol import Vrchol
from collections.abc import Iterable


class KDStrom:
    """
    Trieda KDStrom implementuje k-d strom, ktorý je dátovou štruktúrou na ukladanie bodov v k-rozmernom priestore.
    Atribúty:
    __koren (Vrchol): Koreň stromu.
    __pocet_vrcholov (int): Počet vrcholov v strome.
    __dimenzia (int): Počet dimenzií stromu.
    """

    def __init__(self, dimenzia):
        """
        Inicializuje k-d strom s danou dimenziou.
        """
        self.__koren = None
        self.__pocet_vrcholov = 0
        self.__dimenzia = dimenzia

    def get_pocet_vrcholov(self):
        return self.__pocet_vrcholov
    
    def get_koren(self):
        return self.__koren

    

    def vloz(self, data, kluce):
        """
        Vloží nový vrchol do stromu s danými dátami a kľúčmi.
        """
        
        if self.__koren is None:
            self.__koren = Vrchol(data, kluce)
            self.__pocet_vrcholov += 1
        else:
            novyVrchol = Vrchol(data, kluce)
            aktualny_vrchol = self.__koren
            aktualna_uroven = 0
            

            while True:
                index_kluca = aktualna_uroven % self.__dimenzia
                porovnavany_kluc = kluce[index_kluca]
                kluc_aktualneho_vrcholu = aktualny_vrchol.get_kluce()[index_kluca]
                lavy = False

                if isinstance(porovnavany_kluc, float) and isinstance(kluc_aktualneho_vrcholu, float):
                    if porovnavany_kluc < kluc_aktualneho_vrcholu or abs(porovnavany_kluc - kluc_aktualneho_vrcholu) < 1e-7:
                        nasledujuci_vrchol = aktualny_vrchol.get_lavy_syn()
                        lavy = True
                    else:
                        nasledujuci_vrchol = aktualny_vrchol.get_pravy_syn()

                else:
                    if porovnavany_kluc <= kluc_aktualneho_vrcholu: #pokial su porovnavane kluce rovnake, prvok sa vlozi do laveho podstromu
                        nasledujuci_vrchol = aktualny_vrchol.get_lavy_syn()
                        lavy = True
                    else:
                        nasledujuci_vrchol = aktualny_vrchol.get_pravy_syn()
                        
                if nasledujuci_vrchol is None and lavy:
                    novyVrchol.set_uroven(aktualna_uroven + 1)
                    novyVrchol.set_otec(aktualny_vrchol)
                    aktualny_vrchol.set_lavy_syn(novyVrchol)
                    self.__pocet_vrcholov += 1
                    break
                elif nasledujuci_vrchol is None and not lavy:
                    novyVrchol.set_uroven(aktualna_uroven + 1)
                    novyVrchol.set_otec(aktualny_vrchol)
                    aktualny_vrchol.set_pravy_syn(novyVrchol)
                    self.__pocet_vrcholov += 1
                    break

                aktualny_vrchol = nasledujuci_vrchol
                aktualna_uroven += 1
    
    def najdi(self, kluce):
        """
        Nájde vrcholy v strome s danými kľúčmi.
        """
        vratene_vrcholy = []
        aktualna_uroven = 0
        
        if self.__pocet_vrcholov == 0:
            return vratene_vrcholy

        else:
            aktualny_vrchol = self.__koren
            
            epsilon = 1e-7
            while True:
                kluce_sa_rovnaju = True

                for i in range(self.__dimenzia):

                    if type(kluce[i]) == float and type(aktualny_vrchol.get_kluce()[i]) == float:
                         #ak je absolutna hodnota rozdielu dvoch klucov vacsia ako epsilon - nerovnaju sa 
                         if abs(kluce[i] - aktualny_vrchol.get_kluce()[i]) > epsilon: 
                            kluce_sa_rovnaju = False
                            break

                    elif kluce[i] != aktualny_vrchol.get_kluce()[i]:
                        kluce_sa_rovnaju = False
                        break
            
                if kluce_sa_rovnaju: # vrati sa najdeny vrchol
                    vratene_vrcholy.append(aktualny_vrchol)

                    
                if aktualny_vrchol.vrchol_je_list(): 
                    return vratene_vrcholy
                    
                else:
                    index_kluca = aktualna_uroven % self.__dimenzia
                    porovnavany_kluc = kluce[index_kluca]

                    if isinstance(porovnavany_kluc, float) and isinstance(aktualny_vrchol.get_kluce()[index_kluca], float):
                        if porovnavany_kluc < aktualny_vrchol.get_kluce()[index_kluca] or abs(porovnavany_kluc - aktualny_vrchol.get_kluce()[index_kluca]) < epsilon:
                            aktualny_vrchol = aktualny_vrchol.get_lavy_syn()
                            if aktualny_vrchol is None:
                                return vratene_vrcholy

                        else:
                            aktualny_vrchol = aktualny_vrchol.get_pravy_syn()
                            if aktualny_vrchol is None:
                                return vratene_vrcholy
                    
                    else:

                        if porovnavany_kluc <= aktualny_vrchol.get_kluce()[index_kluca]:
                            aktualny_vrchol = aktualny_vrchol.get_lavy_syn()
                            if aktualny_vrchol is None:
                                return vratene_vrcholy

                        else:
                            aktualny_vrchol = aktualny_vrchol.get_pravy_syn()
                            if aktualny_vrchol is None:
                                return vratene_vrcholy

                    aktualna_uroven += 1

    

    def vymaz(self, data, kluce):
        """
        Vymaže vrchol s danými dátami a kľúčmi zo stromu.
        """
        vymazavane_vrcholy = self.najdi(kluce)
        vymazavany_vrchol = None
        vysledok_mazania = True
        vymazavane_duplicitne_vrcholy = []
        naspat_vkladane_vrcholy = []
        vymazavanie_duplicit = False
        v_datach_je_float = False
        #prehľadáva či je v dátach dátový typ float
        if isinstance(data, Iterable) and not isinstance(data, (str, bytes)):
            for i in range(len(data)):
                if isinstance(data[i], float):
                    v_datach_je_float = True
                    break
        #pokiaľ sa v dátach nachádza float, porovnávajú sa podľa absolútnej hodnoty ich rozdielu s epsilonom
        if v_datach_je_float:
            if len(vymazavane_vrcholy) == 1:
                data_sa_rovnaju = True
                for i in range(len(data)):
                    if isinstance(data[i], float):
                        if abs(vymazavane_vrcholy[0].get_data()[i] - data[i]) > 1e-7:
                            data_sa_rovnaju = False
                            break
                    elif vymazavane_vrcholy[0].get_data()[i] != data[i]:
                        data_sa_rovnaju = False
                        break

                if data_sa_rovnaju:
                    vymazavany_vrchol = vymazavane_vrcholy[0]

            if len(vymazavane_vrcholy) > 1:
                for vrchol in vymazavane_vrcholy:
                    data_sa_rovnaju = True
                    for i in range(len(data)):
                        if isinstance(data[i], float):
                            if abs(vrchol.get_data()[i] - data[i]) > 1e-7:
                                data_sa_rovnaju = False
                                break
                        elif vrchol.get_data()[i] != data[i]:
                            data_sa_rovnaju = False
                            break
                    if data_sa_rovnaju:
                        vymazavany_vrchol = vrchol
                        break
        #v opačnom prípade sa porovnávajú priamo dáta
        else:

            if len(vymazavane_vrcholy) == 1 and vymazavane_vrcholy[0].get_data() == data:
                vymazavany_vrchol = vymazavane_vrcholy[0]
            
            elif len(vymazavane_vrcholy) > 1:
                for vrchol in vymazavane_vrcholy:
                    if vrchol.get_data() == data:
                        vymazavany_vrchol = vrchol
                        break

        

        while True:
            if not vymazavane_vrcholy or vymazavany_vrchol is None:
                vysledok_mazania = False
                break
    
            elif len(vymazavane_duplicitne_vrcholy) > 0:
                vymazavany_vrchol = vymazavane_duplicitne_vrcholy.pop()
                if vymazavany_vrchol not in naspat_vkladane_vrcholy:
                    naspat_vkladane_vrcholy.append(vymazavany_vrchol)
            #pokial nie je listom, nahrad ho najvacsim v lavom/ najmensim v pravom podstrome na zaklade kluca Ki
            while vymazavany_vrchol.vrchol_je_list() == False: 
                
                index_kluca = vymazavany_vrchol.get_uroven() % self.__dimenzia
                lavy_syn = vymazavany_vrchol.get_lavy_syn()
                pravy_syn = vymazavany_vrchol.get_pravy_syn()
                if lavy_syn is not None: #ak ma laveho syna, vyberie max z lava
                    nahradny_vrchol = self.__najdi_max_v_podstrome(lavy_syn, index_kluca)
                    vymazavany_vrchol.vymen_pozicie_vrcholov(nahradny_vrchol)

                elif pravy_syn is not None: #ak ma len praveho syna, vyberie min z prava
                    vymazavane_duplicitne_vrcholy += self.__najdi_min_v_podstrome(pravy_syn, index_kluca)
                    
                    
                    if len(vymazavane_duplicitne_vrcholy) > 1:
                        vymazavanie_duplicit = True
                    nahradny_vrchol = vymazavane_duplicitne_vrcholy.pop()
                    vymazavany_vrchol.vymen_pozicie_vrcholov(nahradny_vrchol)

                if vymazavany_vrchol is self.__koren:
                    self.__koren = nahradny_vrchol

            if self.__pocet_vrcholov == 1:
                self.__koren = None
            else:
                otec = vymazavany_vrchol.get_otec()
                if otec is not None:
                    otec.vymaz_syna(vymazavany_vrchol)
                    vymazavany_vrchol.set_otec(None)

            #ak sa nachadza v duplicitach, bude urcite este raz vymazany, pocet sa znizi az po vymazani poslednej duplicity daneho vrchola
            if vymazavany_vrchol not in vymazavane_duplicitne_vrcholy: 
                self.__pocet_vrcholov -= 1

            if vymazavanie_duplicit == True and len(vymazavane_duplicitne_vrcholy) == 0:
                for vrchol in naspat_vkladane_vrcholy:
                    vkladany = Vrchol(vrchol.get_data(), vrchol.get_kluce())
                    self.vloz(vkladany.get_data(), vkladany.get_kluce())
                break
            elif vymazavanie_duplicit == False:
                break

        return vysledok_mazania
    
    def uprav(self, data, kluce, nove_data, nove_kluce):
        """
        Upraví vrchol s danými dátami a kľúčmi na základe zadaných nových dát a kľúčov.
        """
        vysledok_upravy = False
        uprava_klucovych_atributov = False
        uprava_neklucovych_atributov = False
        
        for i in range (self.__dimenzia):
            if isinstance(kluce[i], float) and isinstance(nove_kluce[i], float):
                if abs(kluce[i] - nove_kluce[i]) > 1e-7:
                    uprava_klucovych_atributov = True
                    break
            else:
                if kluce[i] != nove_kluce[i]:
                    uprava_klucovych_atributov = True
                    break

        if data != nove_data:
            uprava_neklucovych_atributov = True

        
        if uprava_klucovych_atributov:
            vysledok_vymazania = self.vymaz(data, kluce)
            if vysledok_vymazania:
                self.vloz(nove_data, nove_kluce)
                vysledok_upravy = True

        elif uprava_neklucovych_atributov:
            najdene_vrcholy = self.najdi(kluce)
            if najdene_vrcholy:
                for vrchol in najdene_vrcholy:
                    if vrchol.get_data() == data:
                        vrchol.set_data(nove_data)
                        vysledok_upravy = True
                        break

        return vysledok_upravy


            



    def __najdi_max_v_podstrome(self, vrchol, index_kluca):
        """
        Nájde vrchol s maximálnou hodnotou kľúča v ľavom podstrome.
        """
        aktualny_vrchol = vrchol
        if aktualny_vrchol is None:
            return None
        else:
            vybrane_vrcholy = []
            self.__in_order_pre_vymazavanie(vybrane_vrcholy.append, aktualny_vrchol, True)
            max_vrchol = vybrane_vrcholy[0]

            for vrchol in vybrane_vrcholy:
                if vrchol.get_kluce()[index_kluca] > max_vrchol.get_kluce()[index_kluca]:
                    max_vrchol = vrchol

            return max_vrchol
        
    def __najdi_min_v_podstrome(self, vrchol, index_kluca):
        """
        Nájde vrcholy s minimálnou hodnotou kľúča v pravom podstrome.
        """
        aktualny_vrchol = vrchol
        if aktualny_vrchol is None:
            return None
        else:
            vybrane_vrcholy = []
            self.__in_order_pre_vymazavanie(vybrane_vrcholy.append, aktualny_vrchol)
            min_vrchol = vybrane_vrcholy[0]

            for vrchol in vybrane_vrcholy:
                if vrchol.get_kluce()[index_kluca] < min_vrchol.get_kluce()[index_kluca]:
                    min_vrchol = vrchol

            vsetky_min_vrcholy = []
            minimalna_hodnota = min_vrchol.get_kluce()[index_kluca]

            for vrchol in vybrane_vrcholy:
                if type(minimalna_hodnota) == float and type(vrchol.get_kluce()[index_kluca]) == float:
                    if abs(vrchol.get_kluce()[index_kluca] - minimalna_hodnota) < 1e-7:
                        vsetky_min_vrcholy.append(vrchol)
                
                else:
                    if vrchol.get_kluce()[index_kluca] == minimalna_hodnota:
                        vsetky_min_vrcholy.append(vrchol)

            return vsetky_min_vrcholy
        

        
    
    def level_order(self, operacia, zaciatocny_vrchol = None):
        """
        Prejde strom pomocou level-order prehliadky a vykoná zadanú operáciu na každom vrchole.
        """
        if self.__koren is not None:
            vrcholy_predoslej_urovne = [self.__koren]
            if zaciatocny_vrchol is not None:
                vrcholy_predoslej_urovne = [zaciatocny_vrchol]
        
            while vrcholy_predoslej_urovne:
                vrcholy_aktualnej_urovne = []
                for vrchol in vrcholy_predoslej_urovne:
                    operacia(vrchol)
                    if vrchol.get_lavy_syn() is not None:
                        vrcholy_aktualnej_urovne.append(vrchol.get_lavy_syn())
                    if vrchol.get_pravy_syn() is not None:
                        vrcholy_aktualnej_urovne.append(vrchol.get_pravy_syn())
                
                vrcholy_predoslej_urovne = vrcholy_aktualnej_urovne

        else:
            print('Strom je prazdny')


    def in_order(self, operacia, zaciatocny_vrchol = None):
        """
        Vykoná in-order prehliadku stromu a vykoná zadanú operáciu na každom vrchole.
        """
        if self.__koren is not None:
            aktualny_vrchol = self.__koren
            
            if zaciatocny_vrchol is not None:
                aktualny_vrchol = zaciatocny_vrchol
        
            vrcholy = []
                
            while aktualny_vrchol is not None or vrcholy:
                while aktualny_vrchol is not None:
                    vrcholy.append(aktualny_vrchol)
                    aktualny_vrchol = aktualny_vrchol.get_lavy_syn()

                aktualny_vrchol = vrcholy.pop()
                operacia(aktualny_vrchol)
                
                aktualny_vrchol = aktualny_vrchol.get_pravy_syn()

        else:
            print('Strom je prazdny')

    def __in_order_pre_vymazavanie(self, operacia, zaciatocny_vrchol, hladaj_max = False):
            """
            Prejde strom v upravenom in-order poradí pre účely vymazávania a vykoná operáciu na každom vrchole.
            """

            aktualny_vrchol = zaciatocny_vrchol
            #zaciatocny_vrchol je synom vrcholu, ktory sa vymazava, cize sa min/max hlada podla urovne otca
            hladana_uroven = zaciatocny_vrchol.get_uroven() - 1 
            vrcholy = []

            while aktualny_vrchol is not None or vrcholy: 
                while aktualny_vrchol is not None:
                    vrcholy.append(aktualny_vrchol)
            #pokial sa hlada max, prejde sa pravy podstrom, ak sme na spravnej urovni a pravy podstrom uz nie je, v lavom podstrome budu uz iba <= prvky
                    if (aktualny_vrchol.get_uroven() % self.__dimenzia ) == hladana_uroven:
                        if hladaj_max: 
                            if aktualny_vrchol.get_pravy_syn() is not None:
                                aktualny_vrchol = aktualny_vrchol.get_pravy_syn()
                            else:
                                break
                        else:
                            aktualny_vrchol = aktualny_vrchol.get_lavy_syn()
                    else:
                        if hladaj_max:
                            aktualny_vrchol = aktualny_vrchol.get_lavy_syn()
                        else:
                            aktualny_vrchol = aktualny_vrchol.get_pravy_syn()

                if vrcholy:
                    aktualny_vrchol = vrcholy.pop()
                    operacia(aktualny_vrchol)
                    
    #ak spätne prehladavam strom, nenachadzam sa na hladanej urovni, prejdem aj druhy podstrom, ak sa nachadzam na spravnej urovni, prejdem naspat
                    if (aktualny_vrchol.get_uroven() % self.__dimenzia) != hladana_uroven:
                        if hladaj_max:
                            aktualny_vrchol = aktualny_vrchol.get_pravy_syn()
                        else:
                            aktualny_vrchol = aktualny_vrchol.get_lavy_syn()
                    else:
                        aktualny_vrchol = None
                else:
                    aktualny_vrchol = None


    def _test(self, zaciatocny_vrchol, hladaj_max = False):
        """
        Testovacia metóda pre overenie nájdeného počtu prvkov na prechod stromu a počítanie prejdených vrcholov.
        """
        if zaciatocny_vrchol is self.__koren:
            hladana_uroven = 0
        else:
            # zaciatocny_vrchol je synom vrcholu, ktory sa vymazava, cize sa min/max hlada podla urovne o 1 'nizsie'
            hladana_uroven = zaciatocny_vrchol.get_uroven() - 1
            
        aktualny_vrchol = zaciatocny_vrchol
          
        vrcholy = []
        pocet_prejdenych_vrcholov = 0

        while aktualny_vrchol is not None or vrcholy:
            while aktualny_vrchol is not None:
                vrcholy.append(aktualny_vrchol)
                if (aktualny_vrchol.get_uroven() % self.__dimenzia ) == hladana_uroven:
                    if hladaj_max:
                        if aktualny_vrchol.get_pravy_syn() is not None:
                            aktualny_vrchol = aktualny_vrchol.get_pravy_syn()
                        else:
                            break
                    else:
                        aktualny_vrchol = aktualny_vrchol.get_lavy_syn()
                else:
                    if hladaj_max:
                        aktualny_vrchol = aktualny_vrchol.get_lavy_syn()
                    else:
                        aktualny_vrchol = aktualny_vrchol.get_pravy_syn()

            if vrcholy:
                aktualny_vrchol = vrcholy.pop()
                pocet_prejdenych_vrcholov += 1

                if (aktualny_vrchol.get_uroven() % self.__dimenzia) != hladana_uroven:
                    if hladaj_max:
                        aktualny_vrchol = aktualny_vrchol.get_pravy_syn()
                    else:
                        aktualny_vrchol = aktualny_vrchol.get_lavy_syn()
                else:
                    aktualny_vrchol = None
            else:
                aktualny_vrchol = None

        print('Pocet prejdenych vrcholov: ', pocet_prejdenych_vrcholov)
            

    




    
                



                
                    

            


    





                    



            





            


