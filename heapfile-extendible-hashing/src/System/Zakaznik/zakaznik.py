from typing import List
from Interface.interface import IData
from datetime import datetime
from System.Zakaznik.zaznam_o_navsteve import ZaznamONavsteve

class Zakaznik(IData):
    """
    Trieda Zakaznik reprezentuje zákazníka s menom, priezviskom, ID a ECV. 
    Obsahuje metódy na manipuláciu s údajmi zákazníka a záznamami o návštevách.
    Atribúty:
        __id (int): ID zákazníka.
        __meno (str): Meno zákazníka (maximálne 15 znakov).
        __priezvisko (str): Priezvisko zákazníka (maximálne 20 znakov).
        __ecv (str): Evidenčné číslo vozidla (maximálne 10 znakov).
        zaznamy_o_navsteve (List[ZaznamONavsteve]): Zoznam záznamov o návštevách.
    """
    def __init__(self, meno, priezvisko, id, ecv):
        """
        Inicializuje objekt Zakaznik.
        """
        self.__id = id
        if len(meno) > 15:
            raise ValueError("Meno moze mat maximalne 15 znakov")
        else:
            self.__pocet_platnych_znakov_v_mene = len(meno)
            self.__meno = meno
        if len(priezvisko) > 20:
            raise ValueError("Priezvisko moze mat maximalne 20 znakov")
        else:
            self.__pocet_platnych_znakov_v_priezvisku = len(priezvisko)
            self.__priezvisko = priezvisko
        if len (ecv) > 10:
            raise ValueError("Ecv moze mat maximalne 10 znakov")
        else:
            self.__pocet_platnych_znakov_v_ecv = len(ecv)
            self.__ecv = ecv
            

        self.zaznamy_o_navsteve: List[ZaznamONavsteve] = []

    def get_id(self) -> int:
        """
        Vráti ID zákazníka.
        """
        return self.__id

    def get_meno(self) -> str:
        """
        Vrátí meno zákazníka.
        """
        return self.__meno

    def get_priezvisko(self) -> str:
        """
        Vrátí priezvisko zákazníka.
        """
        return self.__priezvisko
    
    def get_ecv(self) -> str:
        """
        Vrátí ECV zákazníka.
        """
        return self.__ecv
    
    def get_navstevy(self) -> List[ZaznamONavsteve]:
        """
        Vráti zoznam platných záznamov o návštevách.
        """
        navstevy: List[ZaznamONavsteve] = []
        for zaznam in self.zaznamy_o_navsteve:
            if zaznam.get_cena() >= 0:
                navstevy.append(zaznam) 
        return navstevy
    
    def set_meno(self, meno):
        """
        Nastaví meno zákazníka.
        """
        self.__meno = meno
        self.__pocet_platnych_znakov_v_mene = len(meno)

    def set_priezvisko(self, priezvisko):
        """
        Nastaví priezvisko zákazníka.
        """
        self.__priezvisko = priezvisko
        self.__pocet_platnych_znakov_v_priezvisku = len(priezvisko)

    def pridaj_zaznam_o_navsteve(self, zaznam) -> bool:
        """
        Pridá záznam o návšteve, ak je platný a počet záznamov je menší ako 5.
        """
        if isinstance(zaznam, ZaznamONavsteve) and len(self.zaznamy_o_navsteve) < 5:
            self.zaznamy_o_navsteve.append(zaznam)
            return True
        
        return False
    
    def vymaz_zaznamy_o_navsteve(self):
        """
        Vymaže všetky záznamy o návštevách.
        """
        self.zaznamy_o_navsteve = []
            

    def __eq__(self, porovnavany) -> bool:
        """
        Porovnáva dva objekty Zakaznik podľa ID alebo ECV.
        """
        if isinstance(porovnavany, Zakaznik):
            return self.__id == porovnavany.get_id() or self.__ecv == porovnavany.get_ecv()
        return False
    
    def klonuj(self) -> 'Zakaznik':
        """
        Vytvorí klon zákazníka s prednastavenými hodnotami.
        """
        klon = Zakaznik('klon', 'klon', -1, 'klon')
        for i in range (5):
            klon.pridaj_zaznam_o_navsteve(ZaznamONavsteve(datetime.now(), -1))

        return klon
    
    def vrat_velkost(self) -> int:
        """
        Vráti veľkosť objektu v bajtoch.
        """
        return 52 + 219 * 5 #1147

    def na_byte_array(self) -> bytearray:
        """
        Konvertuje objekt na byte array.
        """
        byte_array = bytearray()
        byte_array += self.__id.to_bytes(4, byteorder='big', signed=True)
        byte_array += self.__pocet_platnych_znakov_v_mene.to_bytes(1, byteorder='big')
        byte_array += self.__dopln_znaky_do_mena().encode('utf-8')
        byte_array += self.__pocet_platnych_znakov_v_priezvisku.to_bytes(1, byteorder='big')
        byte_array += self.__dopln_znaky_do_priezviska().encode('utf-8')
        byte_array += self.__pocet_platnych_znakov_v_ecv.to_bytes(1, byteorder='big')
        byte_array += self.__dopln_znaky_do_ecv().encode('utf-8')
        
        self.__dopln_zaznamy()
        for zaznam in self.zaznamy_o_navsteve:
            byte_array += zaznam.na_byte_array()
        return byte_array
    
    def z_byte_array(self, byte_array: bytearray):
        """
        Načíta objekt z byte array.
        """
        self.__id = int.from_bytes(byte_array[:4], byteorder='big', signed=True)
        self.__pocet_platnych_znakov_v_mene = int.from_bytes(byte_array[4:5], byteorder='big')
        nacitane_meno = byte_array[5:20].decode('utf-8')
        self.__odstran_znaky_z_mena(nacitane_meno)
        self.__pocet_platnych_znakov_v_priezvisku = int.from_bytes(byte_array[20:21], byteorder='big')
        nacitane_priezvisko = byte_array[21:41].decode('utf-8')
        self.__odstran_znaky_z_priezviska(nacitane_priezvisko)
        self.__pocet_platnych_znakov_v_ecv = int.from_bytes(byte_array[41:42], byteorder='big')
        self.__ecv = byte_array[42:52].decode('utf-8')
        self.__odstran_znaky_z_ecv(self.__ecv)
        
        self.__nacitaj_zaznamy(byte_array[52:])

    def __dopln_zaznamy(self):
        """
        Doplní záznamy o návštevách na počet 5.
        """
        while len(self.zaznamy_o_navsteve) < 5:
            self.zaznamy_o_navsteve.append(ZaznamONavsteve(datetime.now(), -1))

    def __dopln_znaky_do_mena(self) -> str:
        """
        Doplní meno na dĺžku 15 znakov.
        """
        doplnene_meno = self.__meno
        while len(doplnene_meno) < 15:
            doplnene_meno += '*'
        return doplnene_meno
    
    def __dopln_znaky_do_priezviska(self) -> str:
        """
        Doplní priezvisko na dĺžku 20 znakov.
        """
        doplnene_priezvisko = self.__priezvisko
        while len(doplnene_priezvisko) < 20:
            doplnene_priezvisko += '*'
        return doplnene_priezvisko
    
    def __dopln_znaky_do_ecv(self) -> str:
        """
        Doplní ECV na dĺžku 10 znakov.
        """
        doplnene_ecv = self.__ecv
        while len(doplnene_ecv) < 10:
            doplnene_ecv += '*'
        return doplnene_ecv
    
    def __odstran_znaky_z_mena(self, nacitane_meno):
        """
        Odstráni doplnené znaky z mena.
        """
        self.__meno = nacitane_meno[:self.__pocet_platnych_znakov_v_mene]

    def __odstran_znaky_z_priezviska(self, nacitane_priezvisko):
        """
        Odstráni doplnené znaky z priezviska.
        """
        self.__priezvisko = nacitane_priezvisko[:self.__pocet_platnych_znakov_v_priezvisku]

    def __odstran_znaky_z_ecv(self, nacitane_ecv):
        """
        Odstráni doplnené znaky z ECV.
        """
        self.__ecv = nacitane_ecv[:self.__pocet_platnych_znakov_v_ecv]

    def __nacitaj_zaznamy(self, byte_array):
        """
        Načíta záznamy o návštevách z byte array.
        """
        self.zaznamy_o_navsteve = []
        for i in range(5):
            zaznam = ZaznamONavsteve(datetime.now(), 0)
            zaznam.z_byte_array(byte_array[:zaznam.vrat_velkost()])
            if zaznam.get_cena() >= 0:
                self.zaznamy_o_navsteve.append(zaznam)
            byte_array = byte_array[zaznam.vrat_velkost():]

    def to_string(self) -> str:
        """
        Vráti string základných údajov zákazníka.
        """
        return f"ID: {self.__id} M: {self.__meno} Pr: {self.__priezvisko} ECV: {self.__ecv}\n"

    def to_full_string(self) -> str:
        """
        Vráti string všetkých údajov zákazníka vrátane záznamov o návštevách.
        """
        return f"ID: {self.__id} M: {self.__meno} Pr: {self.__priezvisko} ECV: {self.__ecv}\n" + "".join([zaznam.to_string() for zaznam in self.zaznamy_o_navsteve])
