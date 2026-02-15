import struct
from Interface.interface import PodporujePracuSByteArray
from typing import List
from datetime import datetime


class ZaznamONavsteve(PodporujePracuSByteArray):
    """
    Trieda ZaznamONavsteve reprezentuje záznam o návšteve zákazníka.
    Atribúty:
        __datum (int): Dátum návštevy v tvare unix timestamp.
        __cena (float): Cena návštevy.
        __popis_prac (List[str]): Zoznam popisov práce vykonanej na vozidle.
    """
    def __init__(self, datum, cena: float):
        """
        Inicializuje objekt ZaznamONavsteve.
        """
        
        if isinstance(datum, datetime):
            self.__datum = int(datum.timestamp()) # prevod na unix timestamp
        else:
            raise ValueError("Datum musí byť typu datetime")

        self.__cena = cena
        self.__pocet_platnych_znakov_v_popise = ''
        self.__aktualny_popis = ''
        self.__popis_prac : List[str] = [] #10 * 20 znakov

            

    def get_datum(self) -> str:
        """
        Vráti dátum návštevy ako string.
        """
        return datetime.fromtimestamp(self.__datum).strftime('%d.%m.%Y')

    def get_cena(self) -> float:
        """
        Vráti cenu návštevy.
        """
        return self.__cena

    def get_popis(self) -> List[str]:
        """
        Vráti zoznam popisov práce vykonanej na vozidle.
        """
        return self.__popis_prac

    def je_klon(self, kontrolovany) -> bool:
        """
        Porovná záznamy o návšteve na základe ceny a podľa toho určí či je kontrolvaný záznam klonom (má zápornú cenu).
        """
        if isinstance(kontrolovany, ZaznamONavsteve):
            return kontrolovany.get_cena() < 0

    def vrat_velkost(self) -> int:
        """
        Vráti veľkosť záznamu v bajtoch.
        """
        return 219 # 4 + 4 + 1 + (10 * 20 + 1) = datum + cena + pocet_platnych_popisov + 10 popisov prac
    
    def pridaj_popis_prac(self, popis: str):
        """
        Pridá popis práce do zoznamu popisov práce, ak je platný a zoznam nie je plný.
        """
        if isinstance(popis, str) and len(popis) <= 20 and len(self.__popis_prac) < 10:
            self.__popis_prac.append(popis)
    
    def na_byte_array(self) -> bytearray:
        """
        Konvertuje objekt na byte array.
        """
        byte_array = bytearray()
        byte_array += self.__datum.to_bytes(4, byteorder='big')
        byte_array += struct.pack('>f', self.__cena) #4B - single precision - umoznuje uchovavanie cisel do 7 desatinnych miest = postacujuce
        byte_array += len(self.__popis_prac).to_bytes(1, byteorder='big') #pocet platnych popisov prac
        # pridanie popisov prac
        for i in range(10):
            if i < len(self.__popis_prac):
                self.__aktualny_popis = self.__popis_prac[i]
                self.__pocet_platnych_znakov_v_popise = len(self.__aktualny_popis)
            else:
                self.__aktualny_popis = ''
                self.__pocet_platnych_znakov_v_popise = 0

            byte_array += self.__pocet_platnych_znakov_v_popise.to_bytes(1, byteorder='big')
            byte_array += self.__dopln_znaky_do_popisu().encode('utf-8')

        return byte_array
    
    def z_byte_array(self, byte_array: bytearray):
        """
        Konvertuje byte array na objekt.
        """
        self.__datum = int.from_bytes(byte_array[:4], byteorder='big')
        self.__cena = round(struct.unpack('>f', byte_array[4:8])[0], 2)
        pocet_platnych_popisov_prac = int.from_bytes(byte_array[8:9], byteorder='big')
        byte_array = byte_array[9:]
        for i in range(pocet_platnych_popisov_prac):
            self.__pocet_platnych_znakov_v_popise = int.from_bytes(byte_array[:1], byteorder='big')
            nacitany_popis = byte_array[1:21].decode('utf-8')
            self.__odstran_znaky_z_popisu(nacitany_popis)
            self.__popis_prac.append(self.__aktualny_popis)
            byte_array = byte_array[21:]


    def __dopln_znaky_do_popisu(self) -> str: 
        """
        Doplní znaky do popisu práce, aby mal vždy 20 znakov.
        """
        doplneny_popis = self.__aktualny_popis
        while len(doplneny_popis) < 20:
            doplneny_popis += '*'

        return doplneny_popis

    def __odstran_znaky_z_popisu(self, nacitany_popis):
        """
        Odstráni doplnené znaky z popisu práce.
        """
        self.__aktualny_popis = nacitany_popis[:self.__pocet_platnych_znakov_v_popise]

    def to_string(self):
        """
        Vráti objekt ako string.
        """
        if self.__cena < 0:
            return ""
        else:
            popisy_prac_str = ''
            for i in range(len(self.__popis_prac)):
                popisy_prac_str += f'{i + 1}. {self.__popis_prac[i]}\n'

            if popisy_prac_str == '':
                popisy_prac_str = "Neobsahuje žiadne popisy prác\n"
            return f"Datum: {datetime.fromtimestamp(self.__datum).strftime('%d.%m.%Y')}, Cena: {self.__cena}, Popisy prac: \n{popisy_prac_str}"
        
        

        