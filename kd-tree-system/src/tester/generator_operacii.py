from kd_strom_struktura.kd_strom import KDStrom
from tester.uroven_1 import Uroven1
from tester.uroven_4 import Uroven4
from tester.testovacie_data import TestovacieData
import random, string, time
from collections.abc import Iterable


class GeneratorOperacii:
    """
    Trieda GeneratorOperacii generuje náhodné operácie pre testovanie implementovanej štruktúry KD stromu.
    Atribúty:
    __pocet_operacii (int): Počet operácií, ktoré sa majú vykonať.
    __dimenzia (int): Dimenzia KD stromu.
    __strom (KDStrom): Inštancia KD stromu.
    __vlozene_kluce (list): Zoznam vložených kľúčov.
    __vlozene_data (list): Zoznam vložených dát.
    __seed (int): Seed pre generátor náhodných hodnôt.
    __cas_vkladania (float): Celkový čas vkladania v milisekundách.
    __cas_hladania (float): Celkový čas hľadania v milisekundách.
    __cas_vymazavania (float): Celkový čas vymazávania v milisekundách.
    __poradie_operacie (int): Poradie aktuálnej operácie.
    """

    def __init__(self, pocet_operacii, dimenzia, seed = random.randint(0, 10000)):
        """
        Inicializuje generátor operácii, v prípade zadania konkrétneho seed-u ho nastaví.
        """
        self.__pocet_operacii = pocet_operacii
        self.__dimenzia = dimenzia
        self.__strom = KDStrom(dimenzia)
        self.__vlozene_kluce = []
        self.__vlozene_data = []
        self.__seed = seed
        self.__cas_vkladania = 0
        self.__cas_hladania = 0
        self.__cas_vymazavania = 0
        self.__poradie_operacie = 0
        if seed is not None:
            random.seed(seed)  # Nahodne nastaveny seed pokial nie je zadany manualne

    def __vygeneruj_string(self): # o velkosti 10 znakov
        """
        Vygeneruje náhodný reťazec o veľkosti 10 znakov.
        """
        pismena = string.ascii_letters
        return ''.join(random.choice(pismena) for i in range(10))
    
    def __vygeneruj_data(self):
        """
        Vygeneruje náhodné dáta a kľúče podľa dimenzie.
        """
        if self.__dimenzia == 4:
            data = self.__vygeneruj_string()
            atribut_a = random.uniform(0, 1.0)
            atribut_b = self.__vygeneruj_string()
            atribut_c = random.randint(0, 15)
            atribut_d = random.uniform(0, 1.0)
            prvy_kluc = Uroven1(atribut_a, atribut_b)
            stvrty_kluc = Uroven4(atribut_b, atribut_c)
            vygenerovany_kluc = (prvy_kluc, atribut_c, atribut_d, stvrty_kluc)
            return data, vygenerovany_kluc
        
        elif self.__dimenzia == 2:
            while True:
                primarny_kluc = self.__vygeneruj_string()
                sekundarny_kluc_x = random.randint(1, 50)
                sekundarny_kluc_y = random.randint(1, 50)
                data = TestovacieData(primarny_kluc, sekundarny_kluc_x, sekundarny_kluc_y)
                vygenerovany_kluc = data.get_suradnice()
                if data not in self.__vlozene_data:
                    break
            return data, vygenerovany_kluc
    
    def generuj_nahodne_operacie(self):
        """
        Generuje náhodné operácie (vkladanie, hľadanie, vymazávanie) pre KD strom, najprv sa vloží 20000 prvkov a potom sa generujú náhodné operácie.
        """
        self.__cas_vkladania = 0
        self.__cas_hladania = 0
        self.__cas_vymazavania = 0

        for i in range(20000):
            self.generuj_vkladanie()
        
        for i in range(self.__pocet_operacii):
            self.__poradie_operacie = i
            nahodna_operacia = random.randint(0, 2)

            if nahodna_operacia == 0:
                self.generuj_vkladanie()
            elif nahodna_operacia == 1:
                self.generuj_hladanie()
            else:
                self.generuj_vymazanie()

            kontrolovane_vrcholy = []
            self.__strom.level_order(kontrolovane_vrcholy.append)
            if self.__strom.get_pocet_vrcholov() != len(kontrolovane_vrcholy):
                raise Exception(f'Pocet vrcholov sa nezhoduje, error seed: {self.__seed}' )

        self.vypis_casy()

    def generuj_vkladanie(self):
        """
        Generuje operáciu vkladania pre KD strom.
        """
        nahodna_sanca = random.randint(0, 99) #vygeneruje sa nahodne cislo od 0 do 99

        if nahodna_sanca < 50 and self.__vlozene_kluce: # sanca 50% ze sa na vkladanie pouzije duplicitny kluc ak uz je nieco vlozene v strome
            vygenerovany_kluc = self.__vlozene_kluce[random.randint(0, len(self.__vlozene_kluce) - 1)]
            if self.__dimenzia == 4:
                data = self.__vygeneruj_string()
                print(f'Vkladam vrchol s datami: {data} a duplicitnymi klucmi: {vygenerovany_kluc[0].toString()} , {vygenerovany_kluc[1]}, {vygenerovany_kluc[2]}, {vygenerovany_kluc[3].toString()}')
            
            elif self.__dimenzia == 2:
                vygenerovane_data_kluce = self.__vygeneruj_data()
                data = vygenerovane_data_kluce[0]
                data.set_x(vygenerovany_kluc[0])
                data.set_y(vygenerovany_kluc[1])
                print(f'Vkladam vrchol s datami: {data.get_primarny_kluc()} a duplicitnymi klucmi: {str(data.get_suradnice())}')
        else:

            vygenerovane_data_kluce = self.__vygeneruj_data()
            data = vygenerovane_data_kluce[0]
            vygenerovany_kluc = vygenerovane_data_kluce[1]
            if self.__dimenzia == 4: 
                print(f'Vkladam vrchol s datami: {data} a klucmi: {vygenerovany_kluc[0].toString()} , {vygenerovany_kluc[1]}, {vygenerovany_kluc[2]}, {vygenerovany_kluc[3].toString()}')
            elif self.__dimenzia == 2:
                print(f'Vkladam vrchol s datami: {data.get_primarny_kluc()} a klucmi: {str(data.get_suradnice())}')
                    

        zaciatocny_cas = time.time()
        self.__strom.vloz(data, vygenerovany_kluc)
        koncovy_cas = time.time()
        self.__cas_vkladania += (koncovy_cas - zaciatocny_cas) * 1000
        self.__vlozene_data.append(data)
        self.__vlozene_kluce.append(vygenerovany_kluc)



    def generuj_hladanie(self):
        """
        Generuje operáciu hľadania pre KD strom.
        """
        if self.__strom.get_pocet_vrcholov() > 0:
            nahodna_sanca = random.randint(0, 99)
            

            if nahodna_sanca == 1: #sanca 1% ze sa vygeneruje novy kluc
                vygenerovane_data_kluce = self.__vygeneruj_data()
                hladany_kluc = vygenerovane_data_kluce[1]
                if self.__dimenzia == 4:
                    print(f'Hladam vrchol s novymi vygenerovanymi klucmi: {hladany_kluc[0].toString()} , {hladany_kluc[1]}, {hladany_kluc[2]}, {hladany_kluc[3].toString()}')
                elif self.__dimenzia == 2:
                    print(f'Hladam vrchol s novymi vygenerovanymi klucmi: {str(hladany_kluc)}')

            else:
                hladany_kluc = self.__vlozene_kluce[random.randint(0, len(self.__vlozene_kluce) - 1)]
                if self.__dimenzia == 4:
                    print(f'Hladam vrchol s duplicitnymi klucmi: {hladany_kluc[0].toString()} , {hladany_kluc[1]}, {hladany_kluc[2]}, {hladany_kluc[3].toString()}')
                elif self.__dimenzia == 2:
                    print(f'Hladam vrchol s duplicitnymi klucmi: {str(hladany_kluc)}')

            zaciatocny_cas = time.time()
            najdene_vrcholy = self.__strom.najdi(hladany_kluc)
            koncovy_cas = time.time()
            self.__cas_hladania += (koncovy_cas - zaciatocny_cas) * 1000
            
            if najdene_vrcholy: 
                for najdeny_vrchol in najdene_vrcholy:
                    if self.__dimenzia == 4: 
                        print(f'Najdeny vrchol: {najdeny_vrchol.get_data()}')
                    elif self.__dimenzia == 2:
                        print(f'Najdeny vrchol: {najdeny_vrchol.get_data().get_primarny_kluc()}')
            else:
                print(f'Vrchol sa nepodarilo najst')

            pocet_najdenych_vrcholov = len(najdene_vrcholy)
            pocet_duplicitnych_dat_klucov = 0
            epsilon = 1e-7
            

            
            # prehladanie ulozenych dat a klucov aby sa overilo, ze v strome naslo spravny pocet vrcholov podla duplicitneho kluca
            for i in range(len(self.__vlozene_kluce)):
                kluce_sa_rovnaju = True
                

                for j in range(self.__dimenzia):

                    if type(self.__vlozene_kluce[i][j]) == float and type(hladany_kluc[j]) == float:
                         if abs(self.__vlozene_kluce[i][j] - hladany_kluc[j]) > epsilon: 
                            kluce_sa_rovnaju = False
                            break

                    elif self.__vlozene_kluce[i][j] != hladany_kluc[j]:
                        kluce_sa_rovnaju = False
                        break
            
                if kluce_sa_rovnaju:
                    

                    v_datach_je_float = False
                    data = self.__vlozene_data[i]
                    if isinstance(data, Iterable) and not isinstance(data, (str, bytes)):
                        for j in range(len(data)):
                            if isinstance(data[j], float):
                                v_datach_je_float = True
                                break

                    for vrchol in najdene_vrcholy:
                        data_sa_rovnaju = True

                        if v_datach_je_float:

                            data_sa_rovnaju = True
                            for j in range(len(data)):
                                if isinstance(data[i], float):
                                    if abs(vrchol.get_data()[j] - data[j]) > 1e-7:
                                        data_sa_rovnaju = False
                                        break
                                elif vrchol.get_data()[j] != data[j]:
                                    data_sa_rovnaju = False
                                    break

                            if data_sa_rovnaju:
                                pocet_duplicitnych_dat_klucov += 1
                                break
                                    
                        else:

                            if vrchol.get_data() == data:
                                    pocet_duplicitnych_dat_klucov += 1
                                    break

                

            if pocet_najdenych_vrcholov != pocet_duplicitnych_dat_klucov:
                raise Exception (f'Chyba hladania, pocet duplicitnych prvkov v strome a v ulozenych listoch sa nezhoduje na operacii {self.__poradie_operacie} a seede {self.__seed}')
                
        else:
            print('Strom je prazdny, nie je mozne vykonat hladanie')

        
        
        

    def generuj_vymazanie(self):
        """
        Generuje operáciu vymazávania pre KD strom.
        """
        if self.__strom.get_pocet_vrcholov() > 0:
            nahodna_sanca = random.randint(0, 99)


            if nahodna_sanca == 1:
                vygenerovane_data_kluce = self.__vygeneruj_data()
                vymazavane_data = vygenerovane_data_kluce[0]
                vymazavany_kluc = vygenerovane_data_kluce[1]
                if self.__dimenzia == 4:
                    print(f'Vymazavam vrchol s novymi datami: {vymazavane_data} a vygenerovanymi klucmi: {vymazavany_kluc[0].toString()} , {vymazavany_kluc[1]}, {vymazavany_kluc[2]}, {vymazavany_kluc[3].toString()}')
                elif self.__dimenzia == 2:
                    print(f'Vymazavam vrchol s novymi datami: {vymazavane_data.get_primarny_kluc()} a vygenerovanymi klucmi: {str(vymazavane_data.get_suradnice())}')
                
            else:
                
                nahodny_index = random.randint(0, len(self.__vlozene_data) - 1) # je jedno ci vlozene_data alebo vlozene_kluce, dlzku maju rovnaku
                vymazavane_data = self.__vlozene_data.pop(nahodny_index) #vyberu sa data podla nahodneho indexu
                vymazavany_kluc = self.__vlozene_kluce.pop(nahodny_index) #vyberie sa datam prisluchajuce kluce podla nahodneho indexu
                if self.__dimenzia == 4:
                    print(f'Vymazavam vrchol s datami: {vymazavane_data} a klucmi: {vymazavany_kluc[0].toString()} , {vymazavany_kluc[1]}, {vymazavany_kluc[2]}, {vymazavany_kluc[3].toString()}')
                elif self.__dimenzia == 2:
                    print(f'Vymazavam vrchol s datami: {vymazavane_data.get_primarny_kluc()} a klucmi: {str(vymazavany_kluc)}')
                
                
            
            zaciatocny_cas = time.time()
            self.__strom.vymaz(vymazavane_data, vymazavany_kluc)
            koncovy_cas = time.time()
            self.__cas_vymazavania += (koncovy_cas - zaciatocny_cas) * 1000

        else:
            print('Strom je prazdny, nie je mozne vykonat vymazanie')
            

    def test(self):
        """
        Testuje počet prejdených vrcholov upravenou in_order prehliadkou pre vymazávanie KD stromu.
        """
        print('Testujem max')
        self.__strom._test(self.__strom.get_koren().get_lavy_syn(), True)
        print('Testujem min')
        self.__strom._test(self.__strom.get_koren().get_pravy_syn())
        print('Testujem max spusteny nad korenom')
        self.__strom._test(self.__strom.get_koren(), True)
        print('Testujem min spusteny nad korenom')
        self.__strom._test(self.__strom.get_koren())


    def vypis_casy(self):
        """
        Vypíše celkové časy vykonanie operácií vkladania, hľadania a vymazávania.
        """
        print(f'Celkovy cas vkladania bol: {self.__cas_vkladania} ms')
        print(f'Celkovy cas hladania bol: {self.__cas_hladania} ms')
        print(f'Celkovy cas vymazavania bol: {self.__cas_vymazavania} ms')

    

    



    



        


    

