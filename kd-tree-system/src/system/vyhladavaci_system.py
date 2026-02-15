from kd_strom_struktura.kd_strom import KDStrom
from system.nehnutelnost import Nehnutelnost
from system.parcela import Parcela
from system.pozicia_gps import PoziciaGPS
from system.praca_so_subormi.csv_spravca import CSVSpravca
import random,string, copy, tkinter as tk


class VyhladavaciSystem:
    """
    Trieda VyhladavaciSystem implementuje systém na správu nehnuteľností a parciel pomocou KD stromov.
    Atribúty:
    __instancia (VyhladavaciSystem): Singleton inštancia triedy.
    __nehnutelnosti_strom (KDStrom): KD strom pre nehnuteľnosti.
    __parcely_strom (KDStrom): KD strom pre parcely.
    __kombinovany_strom (KDStrom): KD strom pre nehnuteľnosti aj parcely.
    __nasledujuce_volne_id (int): Nasledujúce voľné ID pre pridávané objekty.
    """
    
    __instancia = None
    
    def __init__(self):
        self.__nehnutelnosti_strom = KDStrom(2)
        self.__parcely_strom = KDStrom(2)
        self.__kombinovany_strom = KDStrom(2)
        self.__nasledujuce_volne_id = 0
        

    def __new__(cls):
        """
        Vytvorí novú inštanciu triedy, ak ešte neexistuje.
        """
        if cls.__instancia is None:
            cls.__instancia = super().__new__(cls)
        return cls.__instancia
    
    #1
    def najdi_nehnutelnosti(self, sirka, pozicia_sirky, dlzka, pozicia_dlzky):
        """
        Nájde nehnuteľnosti na základe zadaných súradníc.
        """
        zadana_suradnica = PoziciaGPS(sirka, pozicia_sirky, dlzka, pozicia_dlzky)
        najdene_nehnutelnosti = self.__nehnutelnosti_strom.najdi(zadana_suradnica.get_suradnice())

        if najdene_nehnutelnosti:
            return copy.deepcopy(najdene_nehnutelnosti)
        else: 
            return None
    
    
    #2
    def najdi_parcely(self, sirka, pozicia_sirky, dlzka, pozicia_dlzky):
        """
        Nájde parcely na základe zadaných súradníc.
        """
        zadana_suradnica = PoziciaGPS(sirka, pozicia_sirky, dlzka, pozicia_dlzky)
        najdene_parcely = self.__parcely_strom.najdi(zadana_suradnica.get_suradnice())

        if najdene_parcely:
            return copy.deepcopy(najdene_parcely)
        else:
            return None
    
    #3
    def najdi_vsetky_objekty(self, sirka, pozicia_sirky, dlzka, pozicia_dlzky, sirka2, pozicia_sirky2, dlzka2, pozicia_dlzky2 ):
        """
        Nájde všetky objekty na základe dvoch zadaných súradníc.
        """
        prva_pozicia = PoziciaGPS(sirka, pozicia_sirky, dlzka, pozicia_dlzky)
        druha_pozicia = PoziciaGPS(sirka2, pozicia_sirky2, dlzka2, pozicia_dlzky2)
        vsetky_objekty = []
        objekty_na_druhej_pozicii = []

        vsetky_objekty = self.__kombinovany_strom.najdi(prva_pozicia.get_suradnice())
        objekty_na_druhej_pozicii = self.__kombinovany_strom.najdi(druha_pozicia.get_suradnice())

        for objekt in objekty_na_druhej_pozicii:
            duplicitny = False

            for vrchol in vsetky_objekty:
                if objekt.get_data() == vrchol.get_data(): 
                    duplicitny = True
            
            if not duplicitny:
                vsetky_objekty.append(objekt)


        if vsetky_objekty:
            return copy.deepcopy(vsetky_objekty)
        

    #4 
    def pridaj_nehnutelnost(self, supisne_cislo, popis, sirka, pozicia_sirky, dlzka, pozicia_dlzky, sirka2, pozicia_sirky2, dlzka2, pozicia_dlzky2):
        """
        Pridá novú nehnuteľnosť do databázy.
        """
        prva_pozicia = PoziciaGPS(sirka, pozicia_sirky, dlzka, pozicia_dlzky)
        druha_pozicia = PoziciaGPS(sirka2, pozicia_sirky2, dlzka2, pozicia_dlzky2)


        nehnutelnost = Nehnutelnost(self.__nasledujuce_volne_id, supisne_cislo, popis, prva_pozicia, druha_pozicia)
        self.__nasledujuce_volne_id += 1
        najdene_parcely = []
        parcely_v_nehnutelnosti = nehnutelnost.get_parcely()

        suradnice1 = prva_pozicia.get_suradnice()
        suradnice2 = druha_pozicia.get_suradnice()

        self.__nehnutelnosti_strom.vloz(nehnutelnost, suradnice1)
        self.__nehnutelnosti_strom.vloz(nehnutelnost, suradnice2)
        self.__kombinovany_strom.vloz(nehnutelnost, suradnice1)
        self.__kombinovany_strom.vloz(nehnutelnost, suradnice2)

        najdene_parcely += self.__parcely_strom.najdi(suradnice1)
        najdene_parcely += self.__parcely_strom.najdi(suradnice2)

        for vrchol in najdene_parcely:
            parcela = vrchol.get_data()

            if parcela not in parcely_v_nehnutelnosti:
                parcela.pridaj_nehnutelnost(nehnutelnost)
                parcely_v_nehnutelnosti.append(parcela)

    def __pridaj_nehnutelnost(self, nehnutelnost): #metoda pre pridanie nehnutelnosti pocas nacitavania zo suboru
        """
        Pridá novú nehnuteľnosť počas načítavania zo súboru.
        """
        if nehnutelnost.get_id() >= self.__nasledujuce_volne_id:
            self.__nasledujuce_volne_id = nehnutelnost.get_id() + 1

        suradnice1 = nehnutelnost.get_pozicia_GPS1().get_suradnice()
        suradnice2 = nehnutelnost.get_pozicia_GPS2().get_suradnice()

        najdene_parcely = []
        parcely_v_nehnutelnosti = nehnutelnost.get_parcely()
        
        self.__nehnutelnosti_strom.vloz(nehnutelnost, suradnice1)
        self.__nehnutelnosti_strom.vloz(nehnutelnost, suradnice2)
        self.__kombinovany_strom.vloz(nehnutelnost, suradnice1)
        self.__kombinovany_strom.vloz(nehnutelnost, suradnice2)

        najdene_parcely += self.__parcely_strom.najdi(suradnice1)
        najdene_parcely += self.__parcely_strom.najdi(suradnice2)

        for vrchol in najdene_parcely:
            parcela = vrchol.get_data()

            if parcela not in parcely_v_nehnutelnosti:
                parcela.pridaj_nehnutelnost(nehnutelnost)
                parcely_v_nehnutelnosti.append(parcela)
   

    #5 
    def pridaj_parcelu(self, cislo_parcely, popis, sirka, pozicia_sirky, dlzka, pozicia_dlzky, sirka2, pozicia_sirky2, dlzka2, pozicia_dlzky2):
        """
        Pridá novú parcelu do databázy.
        """
        prva_pozicia = PoziciaGPS(sirka, pozicia_sirky, dlzka, pozicia_dlzky)
        druha_pozicia = PoziciaGPS(sirka2, pozicia_sirky2, dlzka2, pozicia_dlzky2)

        parcela = Parcela(self.__nasledujuce_volne_id, cislo_parcely, popis, prva_pozicia, druha_pozicia)
        self.__nasledujuce_volne_id += 1
        najdene_nehnutelnosti = []
        nehnutelnosti_v_parcele = parcela.get_nehnutelnosti()

        suradnice1 = prva_pozicia.get_suradnice()
        suradnice2 = druha_pozicia.get_suradnice()

        self.__parcely_strom.vloz(parcela, suradnice1)
        self.__parcely_strom.vloz(parcela, suradnice2)
        self.__kombinovany_strom.vloz(parcela, suradnice1)
        self.__kombinovany_strom.vloz(parcela, suradnice2)

        najdene_nehnutelnosti += self.__nehnutelnosti_strom.najdi(suradnice1)
        najdene_nehnutelnosti += self.__nehnutelnosti_strom.najdi(suradnice2)

        for vrchol in najdene_nehnutelnosti:
            nehnutelnost = vrchol.get_data()

            if nehnutelnost not in nehnutelnosti_v_parcele:
                nehnutelnost.pridaj_parcelu(parcela)
                nehnutelnosti_v_parcele.append(nehnutelnost)

    def __pridaj_parcelu(self, parcela): #metoda pre pridanie parcely pocas nacitavania zo suboru
        """
        Pridá novú parcelu počas načítavania zo súboru.
        """
        if parcela.get_id() >= self.__nasledujuce_volne_id:
            self.__nasledujuce_volne_id = parcela.get_id() + 1

        suradnice1 = parcela.get_pozicia_GPS1().get_suradnice()
        suradnice2 = parcela.get_pozicia_GPS2().get_suradnice()

        najdene_nehnutelnosti = []
        nehnutelnosti_v_parcele = parcela.get_nehnutelnosti()

        self.__parcely_strom.vloz(parcela, suradnice1)
        self.__parcely_strom.vloz(parcela, suradnice2)
        self.__kombinovany_strom.vloz(parcela, suradnice1)
        self.__kombinovany_strom.vloz(parcela, suradnice2)

        najdene_nehnutelnosti += self.__nehnutelnosti_strom.najdi(suradnice1)
        najdene_nehnutelnosti += self.__nehnutelnosti_strom.najdi(suradnice2)

        for vrchol in najdene_nehnutelnosti:
            nehnutelnost = vrchol.get_data()

            if nehnutelnost not in nehnutelnosti_v_parcele:
                nehnutelnost.pridaj_parcelu(parcela)
                nehnutelnosti_v_parcele.append(nehnutelnost)

    #6
    def editacia_nehnutelnosti(self, kopia_vrcholu, cislo, popis, sirka1, pozicia_sirky1, dlzka1, pozicia_dlzky1, sirka2, pozicia_sirky2, dlzka2, pozicia_dlzky2):
        """
        Upraví existujúcu nehnuteľnosť.
        """
        kopia_nehnutelnosti = kopia_vrcholu.get_data()
        if isinstance (kopia_nehnutelnosti, Nehnutelnost):
            nova_nehnutelnost = copy.deepcopy(kopia_nehnutelnosti)
            
            nova_nehnutelnost.zmen_vsetko(cislo, popis, sirka1, pozicia_sirky1, dlzka1, pozicia_dlzky1, sirka2, pozicia_sirky2, dlzka2, pozicia_dlzky2)
            nova_nehnutelnost.vymaz_parcely()

            stare_suradnice1 = kopia_nehnutelnosti.get_pozicia_GPS1().get_suradnice()
            stare_suradnice2 = kopia_nehnutelnosti.get_pozicia_GPS2().get_suradnice()
            nove_suradnice1 = nova_nehnutelnost.get_pozicia_GPS1().get_suradnice()
            nove_suradnice2 = nova_nehnutelnost.get_pozicia_GPS2().get_suradnice()

            if stare_suradnice1 != nove_suradnice1 or stare_suradnice2 != nove_suradnice2 and kopia_nehnutelnosti.get_parcely():
                najdene_nehnutelnosti = self.__nehnutelnosti_strom.najdi(stare_suradnice1)
                for vrchol in najdene_nehnutelnosti:
                    if kopia_nehnutelnosti == vrchol.get_data():
                        kopia_nehnutelnosti = vrchol.get_data()



            vysledky_uprav = []
            vysledky_uprav.append(self.__nehnutelnosti_strom.uprav(kopia_nehnutelnosti, stare_suradnice1, nova_nehnutelnost, nove_suradnice1))
            vysledky_uprav.append(self.__nehnutelnosti_strom.uprav(kopia_nehnutelnosti, stare_suradnice2, nova_nehnutelnost, nove_suradnice2))
            vysledky_uprav.append(self.__kombinovany_strom.uprav(kopia_nehnutelnosti, stare_suradnice1, nova_nehnutelnost, nove_suradnice1))
            vysledky_uprav.append(self.__kombinovany_strom.uprav(kopia_nehnutelnosti, stare_suradnice2, nova_nehnutelnost, nove_suradnice2))

            if False in vysledky_uprav:
                return False
            else:
                if stare_suradnice1 != nove_suradnice1 or stare_suradnice2 != nove_suradnice2:
                    
                   
                    kopia_nehnutelnosti.vymaz_parcely()
                    najdene_parcely = []
                    najdene_parcely += self.__parcely_strom.najdi(stare_suradnice1)
                    najdene_parcely += self.__parcely_strom.najdi(stare_suradnice2)

                    for vrchol in najdene_parcely:
                        parcela = vrchol.get_data()
                        parcela.vyrad_nehnutelnost(kopia_nehnutelnosti)

                    najdene_parcely = []
                    parcely_v_nehnutelnosti = nova_nehnutelnost.get_parcely()

                    najdene_parcely += self.__parcely_strom.najdi(nove_suradnice1)
                    najdene_parcely += self.__parcely_strom.najdi(nove_suradnice2)

                    for vrchol in najdene_parcely:
                        parcela = vrchol.get_data()

                        if parcela not in parcely_v_nehnutelnosti:
                            parcela.pridaj_nehnutelnost(nova_nehnutelnost)
                            parcely_v_nehnutelnosti.append(parcela)

            return True

         
                





    #7
    def editacia_parcely(self, kopia_vrcholu, cislo, popis, sirka1, pozicia_sirky1, dlzka1, pozicia_dlzky1, sirka2, pozicia_sirky2, dlzka2, pozicia_dlzky2):
        """
        Upraví existujúcu parcelu.
        """
        kopia_parcely = kopia_vrcholu.get_data()
        if isinstance(kopia_parcely, Parcela):
            
            nova_parcela = copy.deepcopy(kopia_parcely)
            nova_parcela.zmen_vsetko(cislo, popis, sirka1, pozicia_sirky1, dlzka1, pozicia_dlzky1, sirka2, pozicia_sirky2, dlzka2, pozicia_dlzky2)
            nova_parcela.vymaz_nehnutelnosti()

            stare_suradnice1 = kopia_parcely.get_pozicia_GPS1().get_suradnice()
            stare_suradnice2 = kopia_parcely.get_pozicia_GPS2().get_suradnice()
            nove_suradnice1 = nova_parcela.get_pozicia_GPS1().get_suradnice()
            nove_suradnice2 = nova_parcela.get_pozicia_GPS2().get_suradnice()

            if stare_suradnice1 != nove_suradnice1 or stare_suradnice2 != nove_suradnice2 and kopia_parcely.get_nehnutelnosti():
                najdene_parcely = self.__parcely_strom.najdi(stare_suradnice1)
                for vrchol in najdene_parcely:
                    if kopia_parcely == vrchol.get_data():
                        kopia_parcely = vrchol.get_data()

            vysledky_uprav = []
            vysledky_uprav.append(self.__parcely_strom.uprav(kopia_parcely, stare_suradnice1, nova_parcela, nove_suradnice1))
            vysledky_uprav.append(self.__parcely_strom.uprav(kopia_parcely, stare_suradnice2, nova_parcela, nove_suradnice2))
            vysledky_uprav.append(self.__kombinovany_strom.uprav(kopia_parcely, stare_suradnice1, nova_parcela, nove_suradnice1))
            vysledky_uprav.append(self.__kombinovany_strom.uprav(kopia_parcely, stare_suradnice2, nova_parcela, nove_suradnice2))

            if False in vysledky_uprav:
                return False
            else:
                if stare_suradnice1 != nove_suradnice1 or stare_suradnice2 != nove_suradnice2:

                    for nehnutelnost in kopia_parcely.get_nehnutelnosti():
                        nehnutelnost.vyrad_parcelu(kopia_parcely)

                    kopia_parcely.vymaz_nehnutelnosti()
                    najdene_nehnutelnosti = []
                    nehnutelnosti_v_parcele = nova_parcela.get_nehnutelnosti()

                    najdene_nehnutelnosti += self.__nehnutelnosti_strom.najdi(nove_suradnice1)
                    najdene_nehnutelnosti += self.__nehnutelnosti_strom.najdi(nove_suradnice2)

                    for vrchol in najdene_nehnutelnosti:
                        nehnutelnost = vrchol.get_data()

                        if nehnutelnost not in nehnutelnosti_v_parcele:
                            nehnutelnost.pridaj_parcelu(nova_parcela)
                            nehnutelnosti_v_parcele.append(nehnutelnost)

            return True
                   
                
           
                
                

    #8
    def vyradenie_nehnutelnosti(self, kopia_vrcholu):
        """
        Vyradí nehnuteľnosť z databázy.
        """
        nehnutelnost = kopia_vrcholu.get_data()
        if isinstance(nehnutelnost, Nehnutelnost):


            suradnice1 = nehnutelnost.get_pozicia_GPS1().get_suradnice()
            suradnice2 = nehnutelnost.get_pozicia_GPS2().get_suradnice()

            if nehnutelnost.get_parcely():
                najdene_nehnutelnosti = self.__nehnutelnosti_strom.najdi(suradnice1)
            else:
                najdene_nehnutelnosti = []

            vysledky = []

            vysledky.append(self.__nehnutelnosti_strom.vymaz(nehnutelnost, suradnice1))
            vysledky.append(self.__nehnutelnosti_strom.vymaz(nehnutelnost, suradnice2))
            vysledky.append(self.__kombinovany_strom.vymaz(nehnutelnost, suradnice1))
            vysledky.append(self.__kombinovany_strom.vymaz(nehnutelnost, suradnice2))

            if False in vysledky:
                return False
            else:

                for vrchol in najdene_nehnutelnosti:
                    if nehnutelnost == vrchol.get_data():
                        nehnutelnost = vrchol.get_data()
                        parcely_v_nehnutelnosti = nehnutelnost.get_parcely()
                        nehnutelnost.vymaz_parcely()
                        for parcela in parcely_v_nehnutelnosti:
                            parcela.vyrad_nehnutelnost(nehnutelnost)

                return True
            
        return False
        
        
        

    #9
    def vyradenie_parcely(self, kopia_vrcholu):
        """
        Vyradí parcelu z databázy.
        """
        parcela = kopia_vrcholu.get_data()
        if isinstance(parcela, Parcela):
            

            suradnice1 = parcela.get_pozicia_GPS1().get_suradnice()
            suradnice2 = parcela.get_pozicia_GPS2().get_suradnice()

            if parcela.get_nehnutelnosti():
                najdene_parcely = self.__parcely_strom.najdi(suradnice1)
            else:
                najdene_parcely = []

            vysledky = []

            vysledky.append(self.__parcely_strom.vymaz(parcela, suradnice1))
            vysledky.append(self.__parcely_strom.vymaz(parcela, suradnice2))
            vysledky.append(self.__kombinovany_strom.vymaz(parcela, suradnice1))
            vysledky.append(self.__kombinovany_strom.vymaz(parcela, suradnice2))

            if False in vysledky:
                return False
            else:
                  
                for vrchol in najdene_parcely:
                    if parcela == vrchol.get_data():
                        parcela = vrchol.get_data()
                        nehnutelnosti_v_parcele = parcela.get_nehnutelnosti()
                        parcela.vymaz_nehnutelnosti()
                        for nehnutelnost in nehnutelnosti_v_parcele:
                            nehnutelnost.vyrad_parcelu(parcela)
                
                
                return True
            
        return False
    
    
    
    def uloz_do_suboru(self, nazov_suboru):
        """
        Uloží dáta do CSV súboru.
        """
        csv_spravca = CSVSpravca('system/praca_so_subormi/'+ nazov_suboru + '.csv')
        
        ukladane_objekty = []

        def filtruj_objekty(vrchol):
            objekt = vrchol.get_data()
            if objekt not in ukladane_objekty:
                ukladane_objekty.append(objekt)
            
        self.__kombinovany_strom.level_order(filtruj_objekty)

        if ukladane_objekty:
            csv_spravca.uloz(ukladane_objekty)
            return True
        
        return False

    def nacitaj_zo_suboru(self, nazov_suboru, konzola):
        """
        Načíta dáta z CSV súboru.
        """

        self.__nehnutelnosti_strom = KDStrom(2)
        self.__parcely_strom = KDStrom(2)
        self.__kombinovany_strom = KDStrom(2)
        
        csv_spravca = CSVSpravca('system/praca_so_subormi/' + nazov_suboru + '.csv')
        nacitane_udaje = csv_spravca.nacitaj()

        for udaj in nacitane_udaje:
            if udaj[0] == 'N':
                id = int(udaj[1])
                supisne_cislo = int(udaj[2])
                popis = udaj[3]
                suradnice1 = PoziciaGPS(udaj[4], float(udaj[5]), udaj[6], float(udaj[7]))
                suradnice2 = PoziciaGPS(udaj[8], float(udaj[9]), udaj[10], float(udaj[11]))
                nehnutelnost = Nehnutelnost(id, supisne_cislo, popis, suradnice1, suradnice2)
                self.__pridaj_nehnutelnost(nehnutelnost)
                text = nehnutelnost.to_string()
            elif udaj[0] == 'P':
                id = int(udaj[1])
                cislo_parcely = udaj[2]
                popis = udaj[3]
                suradnice1 = PoziciaGPS(udaj[4], float(udaj[5]), udaj[6], float(udaj[7]))
                suradnice2 = PoziciaGPS(udaj[8], float(udaj[9]), udaj[10], float(udaj[11]))
                parcela = Parcela(id, cislo_parcely, popis, suradnice1, suradnice2)
                self.__pridaj_parcelu(parcela)
                text = parcela.to_string()

            konzola.config(state='normal')
            konzola.insert(tk.END, text + '\n')
            konzola.config(state='disabled')
            konzola.see(tk.END)

    def generuj_data(self, pocet_nehnutelnosti, pocet_parciel, prekrytie, konzola):
        """
        Generuje náhodné dáta pre nehnuteľnosti a parcely.
        """
        nehnutelnosti_pouzite_kluce = []
        vygenerovane_objekty = []

        for i in range(pocet_nehnutelnosti):
            
            nehnutelnost = self.__vygeneruj_objekt()
            nehnutelnosti_pouzite_kluce.append(nehnutelnost.get_pozicia_GPS1())
            nehnutelnosti_pouzite_kluce.append(nehnutelnost.get_pozicia_GPS2())
            self.__pridaj_nehnutelnost(nehnutelnost)
            vygenerovane_objekty.append(nehnutelnost)
            

        for i in range(pocet_parciel):
            parcela = self.__vygeneruj_objekt(True)
            nahodna_sanca = random.uniform(0, 1)
            if nahodna_sanca < prekrytie:
                parcela.set_pozicia_GPS1(random.choice(nehnutelnosti_pouzite_kluce))
                

            self.__pridaj_parcelu(parcela)
            vygenerovane_objekty.append(parcela)

        for objekt in vygenerovane_objekty:
            text = objekt.to_string()
            konzola.config(state='normal')
            konzola.insert(tk.END, text + '\n')
            konzola.config(state='disabled')
            konzola.see(tk.END)
            

    def __vygeneruj_objekt(self, generovanie_parcely = False):
            """
            Vygeneruje objekt podľa zadaného parametra boolean - buď nehnuteľnosť alebo parcelu.
            """
            cislo = random.randint(1, 1000)     
            sirka1 = random.choice(['N', 'S'])
            pozicia_sirky1 = round(random.uniform(0, 90), 2)
            dlzka1 = random.choice(['E', 'W'])
            pozicia_dlzky1 = round(random.uniform(0, 180), 2)
            sirka2 = random.choice(['N', 'S'])
            pozicia_sirky2 = round(random.uniform(0, 90), 2)
            dlzka2 = random.choice(['E', 'W'])
            pozicia_dlzky2 = round(random.uniform(0, 180), 2)

            if generovanie_parcely:
                popis = 'P: ' + self.__vygeneruj_string()
                parcela = Parcela(self.__nasledujuce_volne_id, cislo, popis, PoziciaGPS(sirka1, pozicia_sirky1, dlzka1, pozicia_dlzky1), PoziciaGPS(sirka2, pozicia_sirky2, dlzka2, pozicia_dlzky2))
                return parcela
            else:
                popis = 'N: ' + self.__vygeneruj_string()
                nehnutelnost = Nehnutelnost(self.__nasledujuce_volne_id, cislo, popis, PoziciaGPS(sirka1, pozicia_sirky1, dlzka1, pozicia_dlzky1), PoziciaGPS(sirka2, pozicia_sirky2, dlzka2, pozicia_dlzky2))
                return nehnutelnost



    def __vygeneruj_string(self):
        """
        Vygeneruje náhodný reťazec o veľkosti 10 znakov.
        """
        pismena = string.ascii_letters
        return ''.join(random.choice(pismena) for i in range(10))


    

        

        
        
    