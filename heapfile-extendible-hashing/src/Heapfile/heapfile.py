from Interface.interface import IData, PodporujePracuSByteArray
from Heapfile.heapfile_blok import HeapfileBlok as Blok

class HeapFile(PodporujePracuSByteArray):
    """
    Trieda HeapFile reprezentuje súbor v pamäti s dĺžkou bloku, záznamami a s adresami nasledovného a predchádzajúceho bloku.
    Atribúty:
        __nazov_suboru (str): Názov súboru.
        __velkost_bloku (int): Veľkosť bloku.
        __instancia_zaznamu (IData): Inštancia záznamu.
        __pocet_blokov (int): Počet blokov v súbore.
        __nasledujuci_ciastocne_prazdny_blok (int): Adresa nasledovného čiastočne prázdneho bloku.
        __nasledujuci_uplne_prazdny_blok (int): Adresa nasledovného úplne prázdneho bloku.
        __subor (file): Súbor.
    """

    def __init__(self, nazov_suboru, velkost_bloku, instancia_zaznamu: IData):
        """
        Inicializuje objekt HeapFile.
        """
        self.__nazov_suboru = nazov_suboru
        self.__velkost_bloku = velkost_bloku
        blok = Blok(self.__velkost_bloku, instancia_zaznamu)
        if blok.vrat_velkost() + instancia_zaznamu.vrat_velkost() > self.__velkost_bloku:
            raise ValueError("Velkost bloku je prilis mala pre ukladany zaznam")
        
        self.__pocet_blokov = 0

        if isinstance(instancia_zaznamu, IData):
            self.__instancia_zaznamu = instancia_zaznamu
        else:
            raise ValueError("Instancia zaznamu musi implementovat interface IData")
        self.__nasledujuci_ciastocne_prazdny_blok = -1
        self.__nasledujuci_uplne_prazdny_blok = -1

        try:
            self.__subor = open(self.__nazov_suboru, 'rb+')
        except FileNotFoundError:
            
            self.__subor = open(self.__nazov_suboru, 'wb+')
            self.__subor.close()
            self.__subor = open(self.__nazov_suboru, 'rb+')

    def nacitaj_riadiaci_subor(self):
        """
        Načíta riadiaci súbor.
        """
        nazov_konfiguracneho_suboru =  self.__nazov_suboru + '_config'
        
        try:
            konfiguracny_subor = open(nazov_konfiguracneho_suboru, 'rb+')
            self.z_byte_array(konfiguracny_subor.read(16))
            konfiguracny_subor.close()
        except FileNotFoundError:
            
            konfiguracny_subor = open(nazov_konfiguracneho_suboru, 'wb+')
            konfiguracny_subor.close()
            
        


    def zavri_subor(self):
        """
        Zavrie súbor a uloží riadiace informácie do riadiceho súboru.
        """
        self.__subor.close()

        nazov_konfiguracneho_suboru = self.__nazov_suboru + '_config'
        
        try:
            konfiguracny_subor = open(nazov_konfiguracneho_suboru, 'rb+')
            konfiguracny_subor.write(self.na_byte_array())
            konfiguracny_subor.close()
        except FileNotFoundError:
            konfiguracny_subor = open(nazov_konfiguracneho_suboru, 'wb+')
            konfiguracny_subor.write(self.na_byte_array())
            konfiguracny_subor.close()


    def get_pocet_blokov(self) -> int:
        """
        Vráti počet blokov v súbore.
        """
        return self.__pocet_blokov
    
    def get_prvy_ciastocne_prazdny_blok(self) -> int:
        """
        Vráti adresu prvého čiastočne prázdneho bloku v zreťazení.
        """
        return self.__nasledujuci_ciastocne_prazdny_blok
    
    def get_prvy_uplne_prazdny_blok(self) -> int:
        """
        Vráti adresu prvého úplne prázdneho bloku v zreťazení.
        """
        return self.__nasledujuci_uplne_prazdny_blok
    
    def get_blok(self, adresa : int) -> Blok:
        """
        Vráti blok na základe adresy.
        Metóda pre kontrolu v generátore operácií.
        """
        self.__subor.seek(adresa)
        blok = Blok(self.__velkost_bloku, self.__instancia_zaznamu)
        blok.z_byte_array(self.__subor.read(self.__velkost_bloku))
        return blok
    
    def na_byte_array(self) -> bytearray:
        """
        Konvertuje objekt na byte array.
        """

        byte_array = bytearray()
        byte_array += self.__velkost_bloku.to_bytes(4, byteorder='big')
        byte_array += self.__pocet_blokov.to_bytes(4, byteorder='big')
        byte_array += self.__nasledujuci_ciastocne_prazdny_blok.to_bytes(4, byteorder='big', signed=True)
        byte_array += self.__nasledujuci_uplne_prazdny_blok.to_bytes(4, byteorder='big', signed=True)
        return byte_array
    
    def z_byte_array(self, byte_array: bytearray):
        """
        Konvertuje byte array na objekt.
        """
        self.__velkost_bloku = int.from_bytes(byte_array[:4], byteorder='big')
        self.__pocet_blokov = int.from_bytes(byte_array[4:8], byteorder='big')
        self.__nasledujuci_ciastocne_prazdny_blok = int.from_bytes(byte_array[8:12], byteorder='big', signed=True)
        self.__nasledujuci_uplne_prazdny_blok = int.from_bytes(byte_array[12:16], byteorder='big', signed=True)

    def vrat_velkost(self) -> int:
        """
        Vráti veľkosť súboru v bajtoch.
        """
        return 16

    def vloz_zaznam(self, zaznam : IData) -> int:
        """
        Vloží záznam do súboru.
        """
        if isinstance(zaznam, type(self.__instancia_zaznamu)):
           
            if self.__pocet_blokov == 0:
                self.__pocet_blokov += 1
                blok = Blok(self.__velkost_bloku, self.__instancia_zaznamu)
                if blok.pridaj_zaznam(zaznam):
                    if blok.ma_volne_zaznamy():
                        if blok.get_maximalny_pocet_zaznamov() != 1: 
                            self.__nasledujuci_ciastocne_prazdny_blok = 0

                    self.__subor.seek(0)
                    self.__subor.write(blok.na_byte_array())

                    print(f'Zaznam bol uspesne vlozeny na adrese 0 -> {zaznam.get_id()}')
                    
                    return 0
                else:
                    return -1

            #Vkladanie na koniec súboru keďže neexistuje čiastočne ani úplne prázdny blok
            elif self.__pocet_blokov > 0 and self.__nasledujuci_ciastocne_prazdny_blok == -1 and self.__nasledujuci_uplne_prazdny_blok == -1:
                adresa_noveho_bloku = self.__pocet_blokov * self.__velkost_bloku
                novy_blok = Blok(self.__velkost_bloku, self.__instancia_zaznamu)

                if novy_blok.pridaj_zaznam(zaznam):
                    self.__pocet_blokov += 1
                    if novy_blok.ma_volne_zaznamy():
                        if novy_blok.get_maximalny_pocet_zaznamov() != 1: 
                            novy_blok = self.__pridaj_blok_do_zretazenia(adresa_noveho_bloku, novy_blok, True)

                    
                    self.__subor.seek(adresa_noveho_bloku)
                    self.__subor.write(novy_blok.na_byte_array())

                    
                    
                    print(f'Zaznam bol uspesne vlozeny na adrese {adresa_noveho_bloku} -> {zaznam.get_id()}')
                    return adresa_noveho_bloku
                else:
                    return -1

            else:
                #ak je počet blokov viac ako 0 a existuje čiastočne prázdny blok alebo úplne prázdny blok 
                if self.__nasledujuci_ciastocne_prazdny_blok != -1:
                    adresa_bloku = self.__nasledujuci_ciastocne_prazdny_blok
                elif self.__nasledujuci_uplne_prazdny_blok != -1:
                    adresa_bloku = self.__nasledujuci_uplne_prazdny_blok

                
                self.__subor.seek(adresa_bloku)
                blok = Blok(self.__velkost_bloku, self.__instancia_zaznamu)
                blok.z_byte_array(self.__subor.read(self.__velkost_bloku))

                if blok.pridaj_zaznam(zaznam):

                    if adresa_bloku == self.__nasledujuci_ciastocne_prazdny_blok:
                        if not blok.ma_volne_zaznamy():
                            blok = self.__vymaz_blok_zo_zretazenia(adresa_bloku, blok, True)
                        
                        self.__subor.seek(adresa_bloku)
                        self.__subor.write(blok.na_byte_array())



                    else:
                        blok = self.__vymaz_blok_zo_zretazenia(adresa_bloku, blok, False)
                        if blok.get_maximalny_pocet_zaznamov() != 1:
                            blok = self.__pridaj_blok_do_zretazenia(adresa_bloku, blok, True)

                        self.__subor.seek(adresa_bloku)
                        self.__subor.write(blok.na_byte_array())

                else:
                    return -1

                    

                    
                
                print(f'Zaznam bol uspesne vlozeny na adrese {adresa_bloku} -> {zaznam.get_id()}')
                return adresa_bloku


    def vrat_zaznam(self, adresa, zaznam)-> IData:
        """
        Vráti záznam zo zadanej adresy, pokiaľ sa na danej adrese nájde.
        """
        #Ak sú zadané neplatné adresy
        if adresa > (self.__pocet_blokov - 1) * self.__velkost_bloku:
            return None
        elif adresa % self.__velkost_bloku != 0: 
            return None

        self.__subor.seek(adresa)
        blok = Blok(self.__velkost_bloku, self.__instancia_zaznamu)
        blok.z_byte_array(self.__subor.read(self.__velkost_bloku))
        return blok.vrat_zaznam(zaznam)
    
    def aktualizuj_zaznam(self, adresa, aktualizovany_zaznam: IData) -> bool:
        """
        Aktualizuje záznam na zadanej adrese, pokiaľ sa na danej adrese nájde.
        """
        #Ak sú zadané neplatné adresy
        if adresa > (self.__pocet_blokov - 1) * self.__velkost_bloku: 
            return False
        elif adresa % self.__velkost_bloku != 0:
            return False
        
        self.__subor.seek(adresa)
        blok = Blok(self.__velkost_bloku, self.__instancia_zaznamu)
        blok.z_byte_array(self.__subor.read(self.__velkost_bloku))
        if blok.aktualizuj_zaznam(aktualizovany_zaznam):
            self.__subor.seek(adresa)
            self.__subor.write(blok.na_byte_array())
            return True
        else:
            return False
        

        

    def vymaz_zaznam(self, adresa, instancia_zaznamu) -> bool:
        """
        Vymaze zaznam na zadanej adrese.
        """

        if adresa > (self.__pocet_blokov - 1) * self.__velkost_bloku: 
            return False
        elif adresa % self.__velkost_bloku != 0: 
            return False
        
        self.__subor.seek(adresa)
        blok = Blok(self.__velkost_bloku, self.__instancia_zaznamu)
        blok.z_byte_array(self.__subor.read(self.__velkost_bloku))

        if blok.vymaz_zaznam(instancia_zaznamu):
            
            #Blok sa stal úplne prázdny
            if blok.get_pocet_platnych_zaznamov() == 0:
                
                # Ak je blok posledný v súbore
                if adresa == (self.__pocet_blokov - 1) * self.__velkost_bloku: 

                    if blok.get_maximalny_pocet_zaznamov() != 1: 
                        blok = self.__vymaz_blok_zo_zretazenia(adresa, blok, True)
                    self.__pocet_blokov -= 1
                    adresa_kontrolovaneho_bloku = adresa - self.__velkost_bloku
                    kontrolovany_blok = Blok(self.__velkost_bloku, self.__instancia_zaznamu)
                    
                    adresy_blokov_na_vymazavanie_zo_zretazenia = []
                    vymazavane_bloky_zo_zretazenia = []

                    while True:
                        if self.__pocet_blokov > 0:
                            self.__subor.seek(adresa_kontrolovaneho_bloku)
                            kontrolovany_blok.z_byte_array(self.__subor.read(self.__velkost_bloku))

                            if kontrolovany_blok.get_pocet_platnych_zaznamov() != 0:
                                break
                            
                            adresy_blokov_na_vymazavanie_zo_zretazenia.append(adresa_kontrolovaneho_bloku)
                            vymazavane_bloky_zo_zretazenia.append(kontrolovany_blok)
                            
                            self.__pocet_blokov -= 1
                            adresa_kontrolovaneho_bloku -= self.__velkost_bloku
                            kontrolovany_blok = Blok(self.__velkost_bloku, self.__instancia_zaznamu)
                        else:
                            break
                    
                    #Pokiaľ sa súbor neskráti až na začiatok, tak sa vymažú všetky prázdne bloky zo zreťazenia, ktoré sa skrátením vymažú
                    #Pokiaľ sa súbor skráti až na začiatok, čiže sa vymažú všetky bloky, nie je potrebné pristupovať k súboru navyše tým že sa postupne vymažú zo zreťazenia
                    if self.__pocet_blokov != 0:
                        for i in range(len(adresy_blokov_na_vymazavanie_zo_zretazenia)):
                            kontrolovany_blok = self.__vymaz_blok_zo_zretazenia(adresy_blokov_na_vymazavanie_zo_zretazenia[i], vymazavane_bloky_zo_zretazenia[i], False)
                    if self.__pocet_blokov == 0:
                        self.__nasledujuci_ciastocne_prazdny_blok = -1
                        self.__nasledujuci_uplne_prazdny_blok = -1
                    self.__subor.truncate(adresa_kontrolovaneho_bloku + self.__velkost_bloku)
                    
                    return True
                # Ak blok nie je posledný v súbore  
                else: 
                    if blok.get_maximalny_pocet_zaznamov() != 1:
                        blok = self.__vymaz_blok_zo_zretazenia(adresa, blok, True) #Vymazanie z čiastočného zreťazenia, stane sa prázdnym blokom

                    blok = self.__pridaj_blok_do_zretazenia(adresa, blok, False) #Pridanie do úplného zreťazenia
                    self.__subor.seek(adresa)
                    self.__subor.write(blok.na_byte_array())
                    return True
            # Blok sa stal čiastočne prázdnym
            else: 
                
                if blok.get_pocet_platnych_zaznamov() == blok.get_maximalny_pocet_zaznamov() - 1 and blok.get_maximalny_pocet_zaznamov() != 1:
                    blok = self.__pridaj_blok_do_zretazenia(adresa, blok, True)
                    
                self.__subor.seek(adresa)
                self.__subor.write(blok.na_byte_array())
                return True

            
        else:
            return False
            
    def __vymaz_blok_zo_zretazenia(self, adresa_bloku, vymazavany_blok: Blok, ciastocne_prazdne_zretazenia: bool) -> Blok:
        """
        Vymaze blok zo zretazenia blokov.
        """
        
            
        blok = vymazavany_blok
        
        #Ak je blok prvý v zreťazení
        if adresa_bloku == self.__nasledujuci_ciastocne_prazdny_blok or adresa_bloku == self.__nasledujuci_uplne_prazdny_blok: 
            adresa_nasledujuceho_bloku = blok.get_nasledovny_blok()
            if ciastocne_prazdne_zretazenia:
                self.__nasledujuci_ciastocne_prazdny_blok = adresa_nasledujuceho_bloku
            else:
                self.__nasledujuci_uplne_prazdny_blok = adresa_nasledujuceho_bloku

            if adresa_nasledujuceho_bloku != -1:
                self.__subor.seek(adresa_nasledujuceho_bloku)
                nasledujuci_blok = Blok(self.__velkost_bloku, self.__instancia_zaznamu)
                nasledujuci_blok.z_byte_array(self.__subor.read(self.__velkost_bloku))
                nasledujuci_blok.set_predchadzajuci_blok(-1)
                self.__subor.seek(adresa_nasledujuceho_bloku)
                self.__subor.write(nasledujuci_blok.na_byte_array())

        #Ak je blok posledný v zreťazení
        elif blok.get_predchadzajuci_blok() != -1 and blok.get_nasledovny_blok() == -1: 

            adresa_predchadzajuceho_bloku = blok.get_predchadzajuci_blok()
            predchadzajuci_blok = Blok(self.__velkost_bloku, self.__instancia_zaznamu)
            self.__subor.seek(adresa_predchadzajuceho_bloku)
            predchadzajuci_blok.z_byte_array(self.__subor.read(self.__velkost_bloku))
            predchadzajuci_blok.set_nasledovny_blok(-1)
            self.__subor.seek(adresa_predchadzajuceho_bloku)
            self.__subor.write(predchadzajuci_blok.na_byte_array())

        #Ak je blok uprostred zreťazenia
        elif blok.get_predchadzajuci_blok() != -1 and blok.get_nasledovny_blok() != -1: 
            adresa_predchadzajuceho_bloku = blok.get_predchadzajuci_blok()
            adresa_nasledujuceho_bloku = blok.get_nasledovny_blok()
            predchadzajuci_blok = Blok(self.__velkost_bloku, self.__instancia_zaznamu)
            nasledujuci_blok = Blok(self.__velkost_bloku, self.__instancia_zaznamu)

            self.__subor.seek(adresa_predchadzajuceho_bloku)
            predchadzajuci_blok.z_byte_array(self.__subor.read(self.__velkost_bloku))

            self.__subor.seek(adresa_nasledujuceho_bloku)
            nasledujuci_blok.z_byte_array(self.__subor.read(self.__velkost_bloku))

            predchadzajuci_blok.set_nasledovny_blok(adresa_nasledujuceho_bloku)
            nasledujuci_blok.set_predchadzajuci_blok(adresa_predchadzajuceho_bloku)
            
            self.__subor.seek(adresa_predchadzajuceho_bloku)
            self.__subor.write(predchadzajuci_blok.na_byte_array())

            self.__subor.seek(adresa_nasledujuceho_bloku)
            self.__subor.write(nasledujuci_blok.na_byte_array())

        blok.set_nasledovny_blok(-1)
        blok.set_predchadzajuci_blok(-1)
        return blok

    def __pridaj_blok_do_zretazenia(self, adresa_bloku, pridavany_blok: Blok, ciastocne_prazdne_zretazenia: bool) -> Blok:
        """
        Prida blok do zretazenia blokov.
        """
        
        blok = pridavany_blok
        #Ak je zreťazenie prázdne
        if ciastocne_prazdne_zretazenia and self.__nasledujuci_ciastocne_prazdny_blok == -1: 
            self.__nasledujuci_ciastocne_prazdny_blok = adresa_bloku
        #Ak je zreťazenie prázdne
        elif not ciastocne_prazdne_zretazenia and self.__nasledujuci_uplne_prazdny_blok == -1: 
            self.__nasledujuci_uplne_prazdny_blok = adresa_bloku
        #Doplňenie už do existujúceho zreťazenia
        else: 

            if ciastocne_prazdne_zretazenia:
                adresa_dalsieho_bloku = self.__nasledujuci_ciastocne_prazdny_blok
            else:
                adresa_dalsieho_bloku = self.__nasledujuci_uplne_prazdny_blok

            while True:
                self.__subor.seek(adresa_dalsieho_bloku)
                dalsi_blok = Blok(self.__velkost_bloku, self.__instancia_zaznamu)
                dalsi_blok.z_byte_array(self.__subor.read(self.__velkost_bloku))
                if dalsi_blok.get_nasledovny_blok() == -1:
                    break
                adresa_dalsieho_bloku = dalsi_blok.get_nasledovny_blok()

            dalsi_blok.set_nasledovny_blok(adresa_bloku)
            blok.set_predchadzajuci_blok(adresa_dalsieho_bloku)
            self.__subor.seek(adresa_dalsieho_bloku)
            self.__subor.write(dalsi_blok.na_byte_array())

        return blok
    

    def sekvencny_vypis(self) -> str:
        """
        Vypise zaznamy v subore.
        """
        vystup = ""
        if self.__pocet_blokov == 0:
            vystup += f'\n------------ RIADECIE INFORMACIE ------------\n'
            vystup += f'Nasledujuci ciastocne prazdny blok: {self.__nasledujuci_ciastocne_prazdny_blok}\n'
            vystup += f'Nasledujuci uplne prazdny blok: {self.__nasledujuci_uplne_prazdny_blok}\n'
            vystup += 'Subor je prazdny\n'
        else:
            vystup += f'\n------------ RIADECIE INFORMACIE ------------\n'
            vystup += f'Nasledujuci ciastocne prazdny blok: {self.__nasledujuci_ciastocne_prazdny_blok}\n'
            vystup += f'Nasledujuci uplne prazdny blok: {self.__nasledujuci_uplne_prazdny_blok}\n'
            vystup += f'Pocet blokov: {self.__pocet_blokov}\n'

            self.__subor.seek(0)
            for i in range(self.__pocet_blokov):
                blok = Blok(self.__velkost_bloku, self.__instancia_zaznamu)
                adresa_bloku = i * self.__velkost_bloku
                blok.z_byte_array(self.__subor.read(self.__velkost_bloku))
            
                vystup += f'\n------------ BLOK {i + 1} Adresa: {adresa_bloku} ------------\n'
                vystup += blok.to_string() + '\n'
        return vystup
            