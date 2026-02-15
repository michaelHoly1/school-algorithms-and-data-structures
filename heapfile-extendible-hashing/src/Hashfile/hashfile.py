from Hashfile.hashfile_blok import HashFileBlok
from typing import List
from Interface.interface import IHashData, PodporujePracuSByteArray
from bitarray import bitarray
import os

class HashFile(PodporujePracuSByteArray):
    """
    Trieda HashFile reprezentuje hashovací súbor s adresárom a blokmi.
    Atribúty:
        __nazov_suboru (str): Názov súboru.
        __velkost_bloku (int): Veľkosť bloku.
        __hlbka (int): Hĺbka adresára.
        __adresar (List[int]): Adresár.
        __hlbky_blokov (List[int]): Hĺbky blokov.
        __pocet_blokov (int): Počet blokov.
    """

    def __init__(self, nazov_suboru, velkost_bloku, instancia_zaznamu: IHashData):
        """
        Inicializuje objekt HashFile.
        """
        self.__nazov_suboru = nazov_suboru
        self.__velkost_bloku = velkost_bloku
        self.__hlbka = 1
        self.__adresar : List[int] = [-1, -1]
        self.__hlbky_blokov : List[int] = [1, 1] 
        self.__pocet_blokov = 0

        blok = HashFileBlok(self.__velkost_bloku, instancia_zaznamu)
        if blok.vrat_velkost() + instancia_zaznamu.vrat_velkost() > self.__velkost_bloku:
            raise ValueError("Velkost bloku je prilis mala pre ukladany zaznam")
        
        if isinstance(instancia_zaznamu, IHashData):
            self.__instancia_zaznamu = instancia_zaznamu
        else:
            raise ValueError("Instancia zaznamu musi implementovat interface IHashData")
        
        try:
            self.__subor = open(self.__nazov_suboru, 'rb+')
        except FileNotFoundError:
            
            self.__subor = open(self.__nazov_suboru, 'wb+')
            self.__subor.close()
            self.__subor = open(self.__nazov_suboru, 'rb+')
        
    def get_blok(self, adresa_bloku) -> HashFileBlok:
        """
        Vráti blok na základe adresy bloku.
        """
        blok = HashFileBlok(self.__velkost_bloku, self.__instancia_zaznamu)
        self.__subor.seek(adresa_bloku)
        blok.z_byte_array(self.__subor.read(self.__velkost_bloku))
        return blok
    
    def get_pocet_blokov(self) -> int:
        """
        Vráti počet blokov.
        """
        return self.__pocet_blokov

    def nacitaj_riadiaci_subor(self):
        """
        Načíta riadiaci súbor.
        """
        nazov_konfiguracneho_suboru =  self.__nazov_suboru + '_hash_config'
        
        try:
            konfiguracny_subor = open(nazov_konfiguracneho_suboru, 'rb+')
            velkost_suboru = os.path.getsize(nazov_konfiguracneho_suboru)
            self.z_byte_array(konfiguracny_subor.read(velkost_suboru))
            konfiguracny_subor.close()
        except FileNotFoundError:
            
            konfiguracny_subor = open(nazov_konfiguracneho_suboru, 'wb+')
            konfiguracny_subor.close()

    def zavri_subor(self):
        """
        Zavrie súbor a uloží riadiace informácie do riadiceho súboru.
        """
        self.__subor.close()

        nazov_konfiguracneho_suboru = self.__nazov_suboru + '_hash_config'
        try:
            konfiguracny_subor = open(nazov_konfiguracneho_suboru, 'rb+')
            konfiguracny_subor.write(self.na_byte_array())
            konfiguracny_subor.close()
        except FileNotFoundError:
            konfiguracny_subor = open(nazov_konfiguracneho_suboru, 'wb+')
            konfiguracny_subor.write(self.na_byte_array())
            konfiguracny_subor.close()
        

    def __get_index_v_adresari(self, bity : bitarray, pocet_bitov) -> int:
        """
        Vráti index v adresári na základe bitového poľa a zadaného počtu bitov.
        """
        bity = bity[:pocet_bitov]
        index_v_adresari = int(bity.to01(), 2)
        return index_v_adresari
    
    def __zdvojnasob_adresar(self):
        """
        Zdvojnásobí adresár.
        """
        zdvojnasobeny_adresar = []
        zdvojnasobene_hlbky_blokov = []
        for i in range(len(self.__adresar)):
            zdvojnasobovana_adresa = self.__adresar[i]
            zdvojnasobovana_hlbka = self.__hlbky_blokov[i]
            zdvojnasobeny_adresar.append(zdvojnasobovana_adresa)
            zdvojnasobeny_adresar.append(zdvojnasobovana_adresa)
            zdvojnasobene_hlbky_blokov.append(zdvojnasobovana_hlbka)
            zdvojnasobene_hlbky_blokov.append(zdvojnasobovana_hlbka)
        
        self.__adresar = zdvojnasobeny_adresar
        self.__hlbky_blokov = zdvojnasobene_hlbky_blokov
        self.__hlbka += 1

        
    def vrat_zaznam(self, hladany_zaznam: IHashData) -> IHashData:
        """
        Vráti záznam na základe záznamu, ktorý sa hľadá, pokiaľ sa nachádza v súbore.
        """
        hash_kluca = hladany_zaznam.get_hash()
        index_v_adresari = self.__get_index_v_adresari(hash_kluca, self.__hlbka)
        adresa_bloku = self.__adresar[index_v_adresari]
        if adresa_bloku != -1:
            blok = HashFileBlok(self.__velkost_bloku, self.__instancia_zaznamu)
            self.__subor.seek(adresa_bloku)
            blok.z_byte_array(self.__subor.read(self.__velkost_bloku))
            return blok.vrat_zaznam(hladany_zaznam)
        
        return None
    

    def vloz_zaznam(self, vkladany_zaznam: IHashData):
        """
        Vloží záznam do súboru.
        """
        hash_kluca = vkladany_zaznam.get_hash()
        zaznam_je_vlozeny = False
        while not zaznam_je_vlozeny:
            index_bloku_v_adresari = self.__get_index_v_adresari(hash_kluca, self.__hlbka)
            adresa_bloku = self.__adresar[index_bloku_v_adresari]

            
            if adresa_bloku == -1: 
                novy_blok = HashFileBlok(self.__velkost_bloku, self.__instancia_zaznamu)
                novy_blok.pridaj_zaznam(vkladany_zaznam)
                adresa_noveho_bloku = self.__pocet_blokov * self.__velkost_bloku
                # Pokiaľ je hĺbka bloku menšia ako hĺbka súboru, tak sa nová adresa bloku zapíše po celom rozsahu blokov
                if self.__hlbky_blokov[index_bloku_v_adresari] < self.__hlbka:
                    rozsah = 2 ** (self.__hlbka - self.__hlbky_blokov[index_bloku_v_adresari])
                    index_bloku = index_bloku_v_adresari
                    while True:
                        if index_bloku % rozsah == 0:
                            zaciatok_splitu = index_bloku
                            break
                        else:
                            index_bloku -= 1

                    koniec_splitu = zaciatok_splitu + rozsah
                    index_po_splite = int((zaciatok_splitu + koniec_splitu) / 2)
                    if index_bloku_v_adresari < index_po_splite:
                        for i in range (zaciatok_splitu, index_po_splite):
                            self.__adresar[i] = adresa_noveho_bloku
                            self.__hlbky_blokov[i] += 1
                    else:
                        for i in range(index_po_splite, koniec_splitu):
                            self.__adresar[i] = adresa_noveho_bloku
                            self.__hlbky_blokov[i] += 1

                else:
                    self.__adresar[index_bloku_v_adresari] = adresa_noveho_bloku
                    self.__hlbky_blokov[index_bloku_v_adresari] = self.__hlbka
                    

                self.__subor.seek(adresa_noveho_bloku)
                self.__subor.write(novy_blok.na_byte_array())
                self.__pocet_blokov += 1
                zaznam_je_vlozeny = True

            else:
                blok = HashFileBlok(self.__velkost_bloku, self.__instancia_zaznamu)
                self.__subor.seek(adresa_bloku)
                blok.z_byte_array(self.__subor.read(self.__velkost_bloku))

                #Zdvojnásobenie adresára
                if not blok.ma_volne_zaznamy():
                    if self.__hlbky_blokov[index_bloku_v_adresari] == self.__hlbka:
                        self.__zdvojnasob_adresar()

                    #SPLIT
                    pridavany_blok = HashFileBlok(self.__velkost_bloku, self.__instancia_zaznamu)
                    adresa_noveho_bloku = self.__pocet_blokov * self.__velkost_bloku
                    index_bloku_v_splite = self.__get_index_v_adresari(hash_kluca, self.__hlbka)
                    rozsah_splitovania = 2 ** (self.__hlbka - self.__hlbky_blokov[index_bloku_v_splite])
                    
                    index_bloku = index_bloku_v_splite
                    while True:
                        if index_bloku % rozsah_splitovania == 0:
                            zaciatok_splitu = index_bloku
                            break 
                        else:
                            index_bloku -= 1
                    koniec_splitu = zaciatok_splitu + rozsah_splitovania
                    index_po_splite = int((zaciatok_splitu + koniec_splitu) / 2)
                    zaznamy: List[IHashData] = blok.get_zaznamy()
                    pocet_platnych_zaznamov = blok.get_pocet_platnych_zaznamov()
                    presuvane_zaznamy: List[IHashData] = []
                    for i in range(pocet_platnych_zaznamov):
                        presuvane_zaznamy.append(zaznamy[i])
                    blok.vymaz_zaznamy()


                    for zaznam in presuvane_zaznamy:
                        hash_zaznamu = zaznam.get_hash()
                        index_presuvaneho_zaznamu = self.__get_index_v_adresari(hash_zaznamu, self.__hlbka) 
                        if index_presuvaneho_zaznamu < index_po_splite:
                            blok.pridaj_zaznam(zaznam)
                        else:
                            pridavany_blok.pridaj_zaznam(zaznam)

                    if blok.get_pocet_platnych_zaznamov() != 0 and pridavany_blok.get_pocet_platnych_zaznamov() != 0:
                        for i in range(zaciatok_splitu, koniec_splitu):
                            if i < index_po_splite:
                                self.__adresar[i] = adresa_bloku
                                self.__hlbky_blokov[i] += 1
                            else:
                                self.__adresar[i] = adresa_noveho_bloku
                                self.__hlbky_blokov[i] += 1

                        self.__subor.seek(adresa_bloku)
                        self.__subor.write(blok.na_byte_array())
                        self.__subor.seek(adresa_noveho_bloku)
                        self.__subor.write(pridavany_blok.na_byte_array())
                        self.__pocet_blokov += 1

                    else:
                        if blok.get_pocet_platnych_zaznamov() != 0:
                            for i in range(zaciatok_splitu, koniec_splitu):
                                if i < index_po_splite:
                                    self.__adresar[i] = adresa_bloku
                                    self.__hlbky_blokov[i] += 1
                                else:
                                    self.__adresar[i] = -1
                                    self.__hlbky_blokov[i] += 1

                            

                        else:
                            for i in range(zaciatok_splitu, koniec_splitu):
                                if i < index_po_splite:
                                    self.__adresar[i] = -1
                                    self.__hlbky_blokov[i] += 1
                                else:
                                    self.__adresar[i] = adresa_bloku
                                    self.__hlbky_blokov[i] += 1

                            
                            
                else:
                    blok.pridaj_zaznam(vkladany_zaznam)
                    self.__subor.seek(adresa_bloku)
                    self.__subor.write(blok.na_byte_array())
                    zaznam_je_vlozeny = True


    def vrat_velkost(self) -> int:
        """
        Vráti veľkosť súboru v bajtoch.
        """
        return 8 + (4 * len(self.__adresar)) + (4 * len(self.__hlbky_blokov))
    
    def na_byte_array(self) -> bytearray:
        """
        Konvertuje objekt na byte array.
        """
        byte_array = bytearray()
        byte_array += self.__pocet_blokov.to_bytes(4, byteorder='big')
        byte_array += self.__hlbka.to_bytes(4, byteorder='big')
        for adresa in self.__adresar:
            byte_array += adresa.to_bytes(4, byteorder='big', signed=True)
        for hlbka in self.__hlbky_blokov:
            byte_array += hlbka.to_bytes(4, byteorder='big', signed=True)

        return byte_array
    
    def z_byte_array(self, byte_array: bytearray):
        """
        Konvertuje byte array na objekt.
        """
        byte_array = byte_array
        self.__pocet_blokov = int.from_bytes(byte_array[:4], byteorder='big')
        self.__hlbka = int.from_bytes(byte_array[4:8], byteorder='big')
        velkosti_dynamickych_poli = 2 ** self.__hlbka
        self.__adresar = []
        self.__hlbky_blokov = []
        byte_array = byte_array[8:]
        for i in range(velkosti_dynamickych_poli):
            self.__adresar.append(int.from_bytes(byte_array[:4], byteorder='big', signed=True))
            byte_array = byte_array[4:]

        for i in range(velkosti_dynamickych_poli):
            self.__hlbky_blokov.append(int.from_bytes(byte_array[:4], byteorder='big', signed=True))
            byte_array = byte_array[4:]
                

    def sekvencny_vypis(self) -> str:
        """
        Vráti obsah súboru sekvenčne vo forme stringu.
        """
        vystup = ""
        if self.__pocet_blokov == 0:
            vystup += f'\n------------ RIADECIE INFORMACIE ------------\n'
            vystup += f'Hlbka: {self.__hlbka}\n'
            vystup += f'Adresar: {self.__adresar}\n'
            vystup += f'Hlbky blokov: {self.__hlbky_blokov}\n'
            vystup += 'Subor je prazdny\n'
        else:
            vystup += f'\n------------ RIADECIE INFORMACIE ------------\n'
            vystup += f'Adresar: {self.__adresar}\n'
            vystup += f'Hlbky blokov: {self.__hlbky_blokov}\n'
            vystup += f'Pocet blokov: {self.__pocet_blokov}\n'

            self.__subor.seek(0)
            for i in range(self.__pocet_blokov):
                blok = HashFileBlok(self.__velkost_bloku, self.__instancia_zaznamu)
                adresa_bloku = i * self.__velkost_bloku
                blok.z_byte_array(self.__subor.read(self.__velkost_bloku))
            
                vystup += f'\n------------ BLOK {i + 1} Adresa: {adresa_bloku} ------------\n'
                vystup += blok.to_string()
                vystup += '\n'
        return vystup