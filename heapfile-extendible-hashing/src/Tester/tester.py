from Heapfile.heapfile import HeapFile
from System.Zakaznik.zakaznik import Zakaznik
from System.Zakaznik.zaznam_o_navsteve import ZaznamONavsteve
from Hashfile.hashfile import HashFile
from System.Hash_zakaznik.hash_zakaznik_ecv import HashZakaznikECV
from System.Hash_zakaznik.hash_zakaznik_id import HashZakaznikID
from Interface.interface import IData
from datetime import datetime
import random, string
import os


class GeneratorOperacii():
    """
    Trieda GeneratorOperacii slúži na generovanie operácií nad zvolením súborom (Heapfile alebo Hashfile).
    Atribúty:
        __nazov_suboru (str): Názov súboru.
        __velkost_bloku (int): Veľkosť bloku.
        __testovanie_hash_file (bool): True, ak sa má testovať HashFile, inak False.
        __testovanie_na_id (bool): True, ak sa má testovať podľa ID, inak False.
        __seed (int): Seed pre generovanie náhodných čísel.
        __adresy (List[int]): Zoznam adries blokov.
        __vkladane_zaznamy (List[IData]): Zoznam vkladaných záznamov.
        __vygenerovane_ecv (List[str]): Zoznam vygenerovaných ECV.
        __vygenerovane_id (List[int]): Zoznam vygenerovaných ID.
        __poradie_operacie (int): Poradie operácie.
        __volne_id (int): Volné ID.
    """



    def __init__(self, nazov_suboru: str, velkost_bloku: int, testovanie_hash_file: bool = False, testovanie_na_id: bool = False, seed: int = random.randint(0, 10000)):
        """
        Inicializuje objekt GeneratorOperacii.
        """
        self.__nazov_suboru = nazov_suboru
        self.__velkost_bloku = velkost_bloku
        self.__testovanie_hash_file = testovanie_hash_file
        self.__testovanie_na_id = testovanie_na_id
        if testovanie_hash_file:
            if self.__testovanie_na_id:
                self.__hashfile = HashFile(nazov_suboru + '_hash_id', self.__velkost_bloku, HashZakaznikID(-1, -1))
            else:
                self.__hashfile = HashFile(nazov_suboru + '_hash_ecv', self.__velkost_bloku, HashZakaznikECV("1234567890", -1))
            self.__hashfile.nacitaj_riadiaci_subor()
        else:
            self.__heapfile = HeapFile(nazov_suboru, self.__velkost_bloku, Zakaznik("John", "Doe", 1, 'sacsa'))
            self.__heapfile.nacitaj_riadiaci_subor()

        self.__seed = seed
        self.__adresy = []
        self.__vkladane_zaznamy = []
        self.__vygenerovane_ecv = []
        self.__vygenerovane_id = []
        self.__poradie_operacie = 0
        random.seed(self.__seed)
        self.__volne_id = 0

        #Načítanie záznamov zo súboru, ktoré sa v ňom už nachádzajú
        if not self.__testovanie_hash_file:
            if os.path.getsize(nazov_suboru) > 0:
                pocet_blokov = self.__heapfile.get_pocet_blokov()
                for i in range(pocet_blokov):
                    adresa_bloku = i * self.__velkost_bloku
                    blok = self.__heapfile.get_blok(adresa_bloku)
                    zaznamy_bloku = blok.get_zaznamy()
                    for i in range(len(zaznamy_bloku)):
                        klon = zaznamy_bloku[i].klonuj()
                        if zaznamy_bloku[i] != klon:
                            self.__adresy.append(adresa_bloku)
                            self.__vkladane_zaznamy.append(zaznamy_bloku[i])
                            vkladane_id = zaznamy_bloku[i].get_id()
                            self.__vygenerovane_ecv.append(zaznamy_bloku[i].get_ecv())
                            if vkladane_id >= self.__volne_id:
                                self.__volne_id = vkladane_id + 1
        else:
            pocet_blokov = self.__hashfile.get_pocet_blokov()

            if self.__testovanie_na_id:
                if os.path.getsize(nazov_suboru + '_hash_id') > 0:
                    for i in range(pocet_blokov):
                        blok = self.__hashfile.get_blok(i * self.__velkost_bloku)
                        pocet_platnych_zaznamov = blok.get_pocet_platnych_zaznamov()
                        zaznamy_bloku = blok.get_zaznamy()
                        for i in range(pocet_platnych_zaznamov):
                            self.__vkladane_zaznamy.append(zaznamy_bloku[i])
                            self.__vygenerovane_id.append(zaznamy_bloku[i].get_id())
            else:
                if os.path.getsize(nazov_suboru + '_hash_ecv') > 0:
                    for i in range(pocet_blokov):
                        blok = self.__hashfile.get_blok(i * self.__velkost_bloku)
                        pocet_platnych_zaznamov = blok.get_pocet_platnych_zaznamov()
                        zaznamy_bloku = blok.get_zaznamy()
                        for i in range(pocet_platnych_zaznamov):
                            
                            self.__vkladane_zaznamy.append(zaznamy_bloku[i])
                            self.__vygenerovane_ecv.append(zaznamy_bloku[i].get_ecv())
                        
                    

    def generuj_operacie(self, pocet_operacii: int):
        """
        Generuje zadaný počet operácií nad súborom.
        """
        print(f'Seed: {self.__seed}')
        if not self.__testovanie_hash_file:
            if self.__heapfile.get_pocet_blokov() == 0:
                print("Napĺňam súbor záznamami")
                for i in range(1000):
                    self.generuj_vkladanie()

        else:
            if self.__hashfile.get_pocet_blokov() == 0:
                print("Napĺňam súbor záznamami")
                for i in range(1000):
                    self.generuj_vkladanie()

        for i in range(pocet_operacii):
            self.__poradie_operacie += 1
            
            if not self.__testovanie_hash_file:
                nahodna_sanca = random.randint(1, 3)
            else:
                nahodna_sanca = random.randint(1, 2)

            if nahodna_sanca == 1:
                self.generuj_vkladanie()
            elif nahodna_sanca == 2:
                self.generuj_vyhladanie()
                
            else:
                self.generuj_vymazanie()
            
            # V prípade, že sa vykoná vkladanie alebo mazanie, tak sa vykoná kontrola celého súboru
            if nahodna_sanca in [1, 3]: 
                if not self.__testovanie_hash_file:
                    for i in range(len(self.__adresy)):
                        kontrolovany_blok = self.__heapfile.get_blok(self.__adresy[i])
                        najdeny_zakaznik = kontrolovany_blok.vrat_zaznam(self.__vkladane_zaznamy[i])
                        if najdeny_zakaznik != self.__vkladane_zaznamy[i]:
                            raise Exception(f"Nastala chyba pri celkovej kontrole suboru! Operacia: {self.__poradie_operacie}, Seed: {self.__seed}")
                
                else:
                    for i in range(len(self.__vkladane_zaznamy)):
                        if self.__testovanie_na_id:
                            najdeny_zaznam = self.__hashfile.vrat_zaznam(self.__vkladane_zaznamy[i])
                            if najdeny_zaznam != self.__vkladane_zaznamy[i]:
                                raise Exception(f"Nastala chyba pri celkovej kontrole suboru! Operacia: {self.__poradie_operacie}, Seed: {self.__seed}")
                        else:
                            najdeny_zaznam = self.__hashfile.vrat_zaznam(self.__vkladane_zaznamy[i])
                            if najdeny_zaznam != self.__vkladane_zaznamy[i]:
                                raise Exception(f"Nastala chyba pri celkovej kontrole suboru! Operacia: {self.__poradie_operacie}, Seed: {self.__seed}")
        
        if not self.__testovanie_hash_file:
            print(self.__heapfile.sekvencny_vypis()) 

            self.__heapfile.zavri_subor()

            print("Operacie boli vykonane uspesne")
            velkost_suboru = os.path.getsize(self.__nazov_suboru)
            print(f'Velkost suboru: {velkost_suboru}')
            if self.__adresy:
                max_adresa = 0
                for i in range(len(self.__adresy)):
                    if max_adresa < self.__adresy[i]:
                        max_adresa = self.__adresy[i]

                ocakavana_velkost = max_adresa + self.__velkost_bloku

            else:
                ocakavana_velkost = 0
                
            if velkost_suboru != ocakavana_velkost:
                    raise Exception(f"Chyba! Subor nema spravnu velkost! Ocakavana velkost: {ocakavana_velkost} Realna velkost: {velkost_suboru} Seed: {self.__seed}")



        else:
            if self.__testovanie_na_id:
                print('-------------- HEAPFILE ID ----------------')
                velkost_suboru = os.path.getsize(self.__nazov_suboru + '_hash_id')
            else:
                print('-------------- HEAPFILE ECV ----------------')
                velkost_suboru = os.path.getsize(self.__nazov_suboru + '_hash_ecv')
                
            print(self.__hashfile.sekvencny_vypis())

            self.__hashfile.zavri_subor()
            print('Operacie boli vykonane uspesne')
            max_velkost_suboru = len(self.__vkladane_zaznamy) * self.__velkost_bloku

            if velkost_suboru > max_velkost_suboru:
                raise Exception(f"Chyba! Subor ma vacsiu velkost ako je mozne aby mal! Velkost suboru: {velkost_suboru} Odhad max: {max_velkost_suboru}Seed: {self.__seed}")
            

    def generuj_vkladanie(self):
        """
        Generuje vkladanie záznamu do súboru.
        """
        if not self.__testovanie_hash_file:
           
            zakaznik = self.__vygeneruj_zaznam()
            pocet_blokov = self.__heapfile.get_pocet_blokov()
            if pocet_blokov == 0:
                adresa_ulozenia = 0
            else:
                #Určenie, kde by sa mal nový záznam podľa riadiacich informácií Heapfilu uložiť
                adresa_ulozenia = self.__heapfile.get_prvy_ciastocne_prazdny_blok()

                if adresa_ulozenia == -1: 
                    adresa_ulozenia = self.__heapfile.get_prvy_uplne_prazdny_blok()

                    if adresa_ulozenia == -1: 
                        adresa_ulozenia = pocet_blokov * self.__velkost_bloku 

            self.__vkladane_zaznamy.append(zakaznik)
            print(f"P:{self.__poradie_operacie} Vkladam zaznam: -> {zakaznik.get_id()} , {zakaznik.get_meno()} {zakaznik.get_priezvisko()} {zakaznik.get_ecv()}")
            self.__adresy.append(self.__heapfile.vloz_zaznam(zakaznik))

            kontrolovany_blok = self.__heapfile.get_blok(adresa_ulozenia)
            najdeny_zakaznik = kontrolovany_blok.vrat_zaznam(zakaznik)

            if najdeny_zakaznik is None:
                raise Exception(f"Nastala chyba pri vkladani! Operacia: {self.__poradie_operacie}, Seed: {self.__seed}")
        
        else:
            zakaznik = self.__vygeneruj_zaznam()
            if self.__testovanie_na_id:
                print(f"P:{self.__poradie_operacie} Vkladam zaznam: -> {zakaznik.get_id()}")
                self.__hashfile.vloz_zaznam(zakaznik)
                
            else:
                print(f"P:{self.__poradie_operacie} Vkladam zaznam: -> {zakaznik.get_ecv()}")
                self.__hashfile.vloz_zaznam(zakaznik)

            self.__vkladane_zaznamy.append(zakaznik)
            if self.__hashfile.vrat_zaznam(zakaznik) is None:
                    raise Exception(f"Nastala chyba pri vkladani! Operacia: {self.__poradie_operacie}, Seed: {self.__seed}")
        

    def generuj_vymazanie(self):
        """
        Generuje vymazanie záznamu zo súboru.
        """

        nahodna_sanca = random.randint(1,100)

        if nahodna_sanca < 20 and self.__adresy:
            posledna_adresa = self.__adresy[len(self.__adresy) - 1]
            nahodna_adresa = random.randint(posledna_adresa + 1000, posledna_adresa + 2000)
            vymazavany_zakaznik = Zakaznik("John", "Doe", self.__poradie_operacie + 1, 'sdf')
            print(f"P:{self.__poradie_operacie} Vymazavam neexistujuci zaznam: -> {vymazavany_zakaznik.get_id()}")

            if self.__heapfile.vymaz_zaznam(nahodna_adresa, vymazavany_zakaznik):
                raise Exception(f"Nastala chyba pri vymazavani! Operacia: {self.__poradie_operacie}, Seed: {self.__seed}")

        elif self.__adresy:
            nahodny_index = random.randint(0, len(self.__adresy) - 1)
            vymazavana_adresa = self.__adresy.pop(nahodny_index)
            vymazavany_zakaznik = self.__vkladane_zaznamy.pop(nahodny_index)

            print(f"P:{self.__poradie_operacie} Vymazavam zaznam: -> {vymazavany_zakaznik.get_id()}")

            if not self.__heapfile.vymaz_zaznam(vymazavana_adresa, vymazavany_zakaznik):
                raise Exception(f"Nastala chyba pri vymazavani! Operacia: {self.__poradie_operacie}, Seed: {self.__seed}")
            
        else:
            print("Nie je mozne mazanie, kedze nie su ziadne zaznamy v subore")
            
    def generuj_vyhladanie(self):
        """
        Generuje vyhľadanie záznamu zo súboru.
        """
        nahodna_sanca = random.randint(1,100)
        
        if not self.__testovanie_hash_file:
            
            if nahodna_sanca < 20 and self.__adresy:
                posledna_adresa = self.__adresy[len(self.__adresy) - 1]
                nahodna_adresa = random.randint(posledna_adresa + 1000, posledna_adresa + 2000)
                hladany_zakaznik = Zakaznik("John", "Doe", self.__poradie_operacie + 1, 'ffds')

                print(f"P:{self.__poradie_operacie} Hladam neexistujuci zaznam: -> {hladany_zakaznik.get_id()}")
                najdeny_zakaznik = self.__heapfile.vrat_zaznam(nahodna_adresa, hladany_zakaznik)

                if najdeny_zakaznik is not None:
                    raise Exception(f"Nastala chyba pri hladani! Operacia: {self.__poradie_operacie}, Seed: {self.__seed}")
                else:
                    print("zakaznik nebol najdeny")

            elif self.__adresy:
                nahodny_index = random.randint(0, len(self.__adresy) - 1)
                hladana_adresa = self.__adresy[nahodny_index]
                hladany_zakaznik = self.__vkladane_zaznamy[nahodny_index]

                print(f"P:{self.__poradie_operacie} Hladam zaznam: -> {hladany_zakaznik.get_id()}")
                najdeny_zakaznik = self.__heapfile.vrat_zaznam(hladana_adresa, hladany_zakaznik)

                if najdeny_zakaznik is None:
                    raise Exception(f"Nastala chyba pri hladani! Operacia: {self.__poradie_operacie}, Seed: {self.__seed}")
                else:
                    print(f"Vratene udaje: {najdeny_zakaznik.to_string()}")
                
            else:
                print("Nie je mozne hladanie, kedze nie su ziadne zaznamy v subore")

        else:
            
            if nahodna_sanca < 20:
                if self.__testovanie_na_id:
                    while True:
                        nahodne_id = random.randint(0, 1000000)
                        if nahodne_id not in self.__vygenerovane_id:
                            break

                    hladany_zakaznik = hladany_zakaznik = HashZakaznikID(nahodne_id, random.randint(0, 1000))
                    print(f"P:{self.__poradie_operacie} Hladam neexistujuci zaznam: -> {hladany_zakaznik.get_id()}")
                    najdeny_zakaznik = self.__hashfile.vrat_zaznam(hladany_zakaznik)
                else:
                    while True:
                        nahodne_ecv = self.__vygeneruj_string(10)
                        if nahodne_ecv not in self.__vygenerovane_ecv:
                            break

                    hladany_zakaznik = HashZakaznikECV(nahodne_ecv, random.randint(0, 1000))
                    print(f"P:{self.__poradie_operacie} Hladam neexistujuci zaznam: -> {hladany_zakaznik.get_ecv()}")
                    najdeny_zakaznik = self.__hashfile.vrat_zaznam(hladany_zakaznik)

                if najdeny_zakaznik is not None:
                    raise Exception(f"Nastala chyba pri hladani! Operacia: {self.__poradie_operacie}, Seed: {self.__seed}")
                else:
                    print("Zakaznik nebol najdeny")

            elif self.__testovanie_na_id and self.__vygenerovane_id or not self.__testovanie_na_id and self.__vygenerovane_ecv:
                if self.__testovanie_na_id:
                    nahodny_index = random.randint(0, len(self.__vygenerovane_id) - 1)
                    hladany_zakaznik = HashZakaznikID(self.__vygenerovane_id[nahodny_index], random.randint(0, 1000))
                    print(f"P:{self.__poradie_operacie} Hladam zaznam: -> {hladany_zakaznik.get_id()}")
                    najdeny_zakaznik = self.__hashfile.vrat_zaznam(hladany_zakaznik)
                else:
                    nahodny_index = random.randint(0, len(self.__vygenerovane_ecv) - 1)
                    hladany_zakaznik = HashZakaznikECV(self.__vygenerovane_ecv[nahodny_index], random.randint(0, 1000))
                    print(f"P:{self.__poradie_operacie} Hladam zaznam: -> {hladany_zakaznik.get_ecv()}")
                    najdeny_zakaznik = self.__hashfile.vrat_zaznam(hladany_zakaznik)

                if najdeny_zakaznik is None:
                    raise Exception(f"Nastala chyba pri hladani! Operacia: {self.__poradie_operacie}, Seed: {self.__seed}")
                else:
                    print(f"Vratene udaje: {najdeny_zakaznik.to_string()}")


    def __vygeneruj_zaznam(self) -> IData:
        """
        Vygeneruje náhodný záznam.
        """
        if not self.__testovanie_hash_file:
            while True:
                vygenerovane_ecv = self.__vygeneruj_string(10)
                if vygenerovane_ecv not in self.__vygenerovane_ecv:
                    self.__vygenerovane_ecv.append(vygenerovane_ecv)
                    break
            id = self.__volne_id
            zakaznik = Zakaznik(self.__vygeneruj_string(15), self.__vygeneruj_string(20), id, vygenerovane_ecv)
            self.__volne_id += 1
            nahodny_pocet_zaznamov = random.randint(1, 5)
            for i in range(nahodny_pocet_zaznamov):
                zakaznik.pridaj_zaznam_o_navsteve(ZaznamONavsteve(datetime.now(), random.uniform(0, 100)))  

            return zakaznik 
        else:
            if self.__testovanie_na_id:
                while True:
                    id = random.randint(0, 100000)
                    if id not in self.__vygenerovane_id:
                        self.__vygenerovane_id.append(id)
                        return HashZakaznikID(id, random.randint(0, 1000))
            else:
                while True:
                    ecv = self.__vygeneruj_string(10)
                    if ecv[:4] not in self.__vygenerovane_ecv:
                        self.__vygenerovane_ecv.append(ecv[:4])
                        return HashZakaznikECV(ecv, random.randint(0, 1000))

    def __vygeneruj_string(self, max_pocet_znakov: int): 
        """
        Vygeneruje náhodný string so zadaným maximálnym počtom znakov.
        """
        pocet_znakov = random.randint(1, max_pocet_znakov)

        pismena = string.ascii_letters
        return ''.join(random.choice(pismena) for i in range(pocet_znakov))
        

