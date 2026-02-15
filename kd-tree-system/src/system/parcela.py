from interface.interface import PodporujeRovnost
from system.pozicia_gps import PoziciaGPS

class Parcela(PodporujeRovnost):
    """
    Trieda Parcela reprezentuje pozemok s rôznymi atribútmi a metódami na manipuláciu s nimi.
    Atribúty:
    __id (int): Identifikátor parcely.
    __cislo_parcely (str): Číslo parcely.
    __popis (str): Popis parcely.
    __nehnutelnosti (list): Zoznam nehnuteľností na parcele - ich referencie.
    __pozicia_GPS1 (PoziciaGPS): GPS pozícia 1.
    __pozicia_GPS2 (PoziciaGPS): GPS pozícia 2.
    """

    def __init__(self, id, cislo_parcely, popis ,pozicia_GPS1, pozicia_GPS2):
        """
        Inicializuje atribúty parcely.
        """
        self.__id = id
        self.__cislo_parcely = cislo_parcely
        self.__popis = popis
        self.__nehnutelnosti = []
        self.__pozicia_GPS1 = pozicia_GPS1
        self.__pozicia_GPS2 = pozicia_GPS2


    def __eq__(self, porovnavany):
        """
        Porovnáva rovnosť dvoch parciel na základe ich atribútov.
        """
        return (self.__id == porovnavany.get_id() and 
                self.__cislo_parcely == porovnavany.get_cislo() and 
                self.__popis == porovnavany.get_popis())
    
    # Gettery
    def get_id(self):
        return self.__id
    
    def get_cislo(self):
        return self.__cislo_parcely

    def get_popis(self):
        return self.__popis

    def get_nehnutelnosti(self):
        return self.__nehnutelnosti

    def get_pozicia_GPS1(self):
        return self.__pozicia_GPS1

    def get_pozicia_GPS2(self):
        return self.__pozicia_GPS2

    # Settery
    def set_cislo(self, cislo_parcely):
        self.__cislo_parcely = cislo_parcely

    def set_popis(self, popis):
        self.__popis = popis

    def set_pozicia_GPS1(self, pozicia_GPS1):
        self.__pozicia_GPS1 = pozicia_GPS1

    def set_pozicia_GPS2(self, pozicia_GPS2):
        self.__pozicia_GPS2 = pozicia_GPS2

    def pridaj_nehnutelnost(self, nehnutelnost):
        self.__nehnutelnosti.append(nehnutelnost)

    def vyrad_nehnutelnost(self, vyradovana_nehnutelnost):
        for nehnutelnost in self.__nehnutelnosti:
            if nehnutelnost == vyradovana_nehnutelnost:
                self.__nehnutelnosti.remove(nehnutelnost)

    def vymaz_nehnutelnosti(self):
        self.__nehnutelnosti = []

    def zmen_vsetko(self, cislo, popis, sirka, pozicia_sirky, dlzka, pozicia_dlzky, sirka2, pozicia_sirky2, dlzka2, pozicia_dlzky2):
        """
        Zmení všetky atribúty parcely.
        """
        self.__cislo_parcely = cislo
        self.__popis = popis
        self.__pozicia_GPS1 = PoziciaGPS(sirka, pozicia_sirky, dlzka, pozicia_dlzky)
        self.__pozicia_GPS2 = PoziciaGPS(sirka2, pozicia_sirky2, dlzka2, pozicia_dlzky2)

    def zmen_neklucove_atributy(self, cislo, popis):
        """
        Zmení neklúčové atribúty parcely.
        """
        self.__cislo_parcely = cislo
        self.__popis = popis

    def vypis(self):
        """
        Vypíše informácie o parcele.
        """
        print(f'Cislo parcely: {self.__cislo_parcely} \n Popis: {self.__popis} \n Pozicia GPS1: {self.__pozicia_GPS1.vypis()} \n Pozicia GPS2: {self.__pozicia_GPS2.vypis()}')
        print('Nehnutelnosti, ktore sa nachadzaju na parcele: ')
        for nehnutelnost in self.__nehnutelnosti:
            nehnutelnost.vypis()

    def to_string(self):
        """
        Vráti reťazcovú reprezentáciu objektu Parcela.
        """
        nehnutelnosti_str = ', '.join([nehnutelnost.get_popis() for nehnutelnost in self.__nehnutelnosti])
        return (f'P C: {self.__cislo_parcely} {self.__popis} GPS1: {self.__pozicia_GPS1.to_string()} GPS2: {self.__pozicia_GPS2.to_string()} \nNehnutelnosti: {nehnutelnosti_str}')

    def vypis_pre_csv(self):
        """
        Vráto reťazec pre CSV súbor
        """
        return f'P;{self.__id};{self.__cislo_parcely};{self.__popis};{self.__pozicia_GPS1.vypis_pre_csv()};{self.__pozicia_GPS2.vypis_pre_csv()}'
            