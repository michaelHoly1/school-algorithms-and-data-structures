
from system.nehnutelnost import Nehnutelnost
from system.parcela import Parcela

class CSVSpravca:
    """
    Trieda CSVSpravca slúži na ukladanie a načítanie objektov do/z CSV súboru.
    """

    def __init__(self, nazov_suboru):
        """
        Inicializuje inštanciu triedy CSVSpravca s názvom súboru.
        """
        self.nazov_suboru = nazov_suboru

    def uloz(self, objekty):
        """
        Uloží zoznam objektov do CSV súboru. Podporované objekty sú inštancie tried Nehnutelnost a Parcela.
        """
        if objekty:
            with open(self.nazov_suboru, mode='w', newline='') as subor:
                subor.write('Typ;ID;Cislo;Popis;Sirka1;PoziciaSirky1;Dlzka1;PoziciaDlzky1;Sirka2;PoziciaSirky2;Dlzka2;PoziciaDlzky2\n')
                for objekt in objekty:
                    if isinstance(objekt, Nehnutelnost) or isinstance(objekt, Parcela):
                        subor.write(objekt.vypis_pre_csv() + '\n')

    def nacitaj(self):
        """
        Načíta údaje z CSV súboru a vráti ich ako zoznam zoznamov. Ak súbor neexistuje, vypíše chybovú správu a vráti prázdny zoznam.
        """
        nacitane_udaje = []
        try:
            with open(self.nazov_suboru, mode='r', newline='') as subor:
                next(subor) #preskoci riadok s hlavickami 
                for riadok in subor:
                    riadok = riadok.strip()
                    if riadok:
                        nacitane_udaje.append(riadok.split(';'))
        except FileNotFoundError:
            print("Subor neexistuje")
        return nacitane_udaje

