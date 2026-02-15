from interface.interface import PodporujeRovnost
from system.pozicia_gps import PoziciaGPS


class Nehnutelnost(PodporujeRovnost):
    """
    Trieda Nehnutelnost predstavuje nehnuteľnosť s rôznymi atribútmi a metódami na manipuláciu s nimi.
    Atribúty:
    __id (int): Identifikátor nehnuteľnosti.
    __supisne_cislo (str): Súpisné číslo nehnuteľnosti.
    __popis (str): Popis nehnuteľnosti.
    __parcely (list): Zoznam parciel, na ktorých sa nehnuteľnosť nachádza - ich referencie.
    __pozicia_GPS1 (PoziciaGPS): Prvá GPS pozícia nehnuteľnosti.
    __pozicia_GPS2 (PoziciaGPS): Druhá GPS pozícia nehnuteľnosti.
    """

    def __init__(self, id, supisne_cislo, popis, pozicia_GPS1, pozicia_GPS2):
        """
        Inicializuje objekt Nehnutelnost.
        """
        self.__id = id
        self.__supisne_cislo = supisne_cislo
        self.__popis = popis
        self.__parcely = []
        self.__pozicia_GPS1 = pozicia_GPS1
        self.__pozicia_GPS2 = pozicia_GPS2


    def __eq__(self, porovnavany):
        """
        Porovnáva rovnosť dvoch objektov na základe ich atribútov.
        """
        return (self.__id == porovnavany.get_id() and
                self.__supisne_cislo == porovnavany.get_cislo() and
                self.__popis == porovnavany.get_popis())
    
    # Gettery
    def get_id(self):
        return self.__id

    def get_cislo(self):
        return self.__supisne_cislo

    def get_popis(self):
        return self.__popis

    def get_parcely(self):
        return self.__parcely

    def get_pozicia_GPS1(self):
        return self.__pozicia_GPS1

    def get_pozicia_GPS2(self):
        return self.__pozicia_GPS2

    # Settery
    def set_cislo(self, supisne_cislo):
        self.__supisne_cislo = supisne_cislo

    def set_popis(self, popis):
        self.__popis = popis

    def set_pozicia_GPS1(self, pozicia_GPS):
        self.__pozicia_GPS1 = pozicia_GPS

    def set_pozicia_GPS2(self, pozicia_GPS):
        self.__pozicia_GPS2 = pozicia_GPS

    def pridaj_parcelu(self, parcela):
        self.__parcely.append(parcela)

    def vyrad_parcelu(self, vyradovana_parcela):
        for parcela in self.__parcely:
            if parcela == vyradovana_parcela:
                self.__parcely.remove(parcela)

    def vymaz_parcely(self):
        self.__parcely = []


    def zmen_vsetko(self, cislo, popis, sirka, pozicia_sirky, dlzka, pozicia_dlzky, sirka2, pozicia_sirky2, dlzka2, pozicia_dlzky2):
        """
        Zmení všetky atribúty nehnuteľnosti.
        """
        self.__supisne_cislo = cislo
        self.__popis = popis
        self.__pozicia_GPS1 = PoziciaGPS(sirka, pozicia_sirky, dlzka, pozicia_dlzky)
        self.__pozicia_GPS2 = PoziciaGPS(sirka2, pozicia_sirky2, dlzka2, pozicia_dlzky2)

    def zmen_neklucove_atributy(self, cislo, popis):
        """
        Zmení neklúčové atribúty nehnuteľnosti.
        """
        self.__supisne_cislo = cislo
        self.__popis = popis

    def vypis(self):
        """
        Vypíše informácie o nehnuteľnosti.
        """
        print(f'Supisne cislo: {self.__supisne_cislo} \n Popis: {self.__popis} \n Pozicia GPS1: {self.__pozicia_GPS1.vypis()} \n Pozicia GPS2: {self.__pozicia_GPS2.vypis()}')
        print('Parcely, na ktorych sa nachadza nehnutelnost: ')
        for parcela in self.__parcely:
            parcela.vypis()

    def to_string(self):
        """
        Vráti reťazcovú reprezentáciu objektu Nehnutelnost.
        """
        parcely_str = ', '.join([parcela.get_popis() for parcela in self.__parcely])
        return (f'N C: {self.__supisne_cislo} {self.__popis} GPS1: {self.__pozicia_GPS1.to_string()} GPS2: {self.__pozicia_GPS2.to_string()} \nParcely: {parcely_str} ')

    def vypis_pre_csv(self):
        """
        Vráti reťazec pre CSV súbor.
        """
        return f'N;{self.__id};{self.__supisne_cislo};{self.__popis};{self.__pozicia_GPS1.vypis_pre_csv()};{self.__pozicia_GPS2.vypis_pre_csv()}'
