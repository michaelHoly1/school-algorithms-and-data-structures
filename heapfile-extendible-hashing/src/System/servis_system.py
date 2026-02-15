from Heapfile.heapfile import HeapFile
from System.Zakaznik.zakaznik import Zakaznik
from System.Zakaznik.zaznam_o_navsteve import ZaznamONavsteve
from Hashfile.hashfile import HashFile
from System.Hash_zakaznik.hash_zakaznik_ecv import HashZakaznikECV
from System.Hash_zakaznik.hash_zakaznik_id import HashZakaznikID
from typing import List
from datetime import datetime, timedelta 
import random,string, copy, tkinter as tk 




class ServisnySystem():
    """
    Trieda ServisnySystem reprezentuje systém, ktorý spravuje zákazníkov a ich návštevy servisu.
    Atribúty:
        __heap_zakaznici (HeapFile): Heapfile pre ukladanie zákazníkov.
        __hash_zakaznici_podla_id (HashFile): Hashfile pre vyhľadávanie zákazníkov podľa ID.
        __hash_zakaznici_podla_ecv (HashFile): Hashfile pre vyhľadávanie zákazníkov podľa ECV.
    """
    __instancia = None
    
    def __init__(self):
        """
        Inicializuje objekt ServisnySystem.
        Heapfile velkosť bloku 3453 = 12 R.I. bloku + 3* 1147 V. zaznamov
        Hashfile_id veľkosť bloku 84 = 4 R.I. bloku + 10* 8 V. zaznamov
        Hashfile_ecv veľkosť bloku 154 = 4 R.I. bloku + 10* 15 V. zaznamov
        """
        self.__heap_zakaznici = HeapFile('Subory/system_zakaznici', 3453, Zakaznik("John", "Doe", 1, 'sacsa')) 
        self.__hash_zakaznici_podla_id = HashFile('Subory/system_hash_zakaznici_id', 84, HashZakaznikID(-1, -1)) 
        self.__hash_zakaznici_podla_ecv = HashFile('Subory/system_hash_zakaznici_ecv', 154, HashZakaznikECV('sacsa', -1)) 
        
        self.__heap_zakaznici.nacitaj_riadiaci_subor()
        self.__hash_zakaznici_podla_id.nacitaj_riadiaci_subor()
        self.__hash_zakaznici_podla_ecv.nacitaj_riadiaci_subor()

    def __new__(cls):
        """
        Vytvorí novú inštanciu triedy, ak ešte neexistuje.
        """
        if cls.__instancia is None:
            cls.__instancia = super().__new__(cls)
        return cls.__instancia
    
    def zavri_subory(self):
        """
        Uzavrie všetky súbory.
        """
        self.__heap_zakaznici.zavri_subor()
        self.__hash_zakaznici_podla_id.zavri_subor()
        self.__hash_zakaznici_podla_ecv.zavri_subor()
    
    #1 
    def vyhladaj_vozidlo(self, hladany_kluc, hladanie_podla_id: bool, konzola: tk.Text) -> Zakaznik:
        """
        Vyhľadá zákazníka podľa ID alebo ECV.
        """
        if hladanie_podla_id:
            if isinstance(hladany_kluc, int):
                hladane_id = hladany_kluc
                hladany_zakaznik_id = HashZakaznikID(hladane_id, -1)
                vrateny_zaznam: HashZakaznikID = self.__hash_zakaznici_podla_id.vrat_zaznam(hladany_zakaznik_id)
                if vrateny_zaznam is not None:
                    adresa_v_heapfile = vrateny_zaznam.get_adresa()
                    vrateny_zakaznik: Zakaznik = self.__heap_zakaznici.vrat_zaznam(adresa_v_heapfile, Zakaznik('','',hladane_id,''))

                    if vrateny_zakaznik is not None:

                        konzola.config(state='normal')
                        konzola.insert(tk.END, f"Zákazník {vrateny_zakaznik.to_string()} bol úspešne nájdený!\n")
                        konzola.insert(tk.END, f"{vrateny_zakaznik.to_full_string()}\n")
                        konzola.config(state='disabled')
                        konzola.see(tk.END)
                        return copy.deepcopy(vrateny_zakaznik)
                    else:
                        konzola.config(state='normal')
                        konzola.insert(tk.END, f"Zákazníka s ID: {hladany_kluc} sa nepodarilo nájsť!\n")
                        konzola.config(state='disabled')
                        konzola.see(tk.END)
                        return None
                else:
                    konzola.config(state='normal')
                    konzola.insert(tk.END, f"Zákazníka s ID: {hladany_kluc} sa nepodarilo nájsť!\n")
                    konzola.config(state='disabled')
                    konzola.see(tk.END)
                    return None
                
        else:
            if isinstance(hladany_kluc, str):
                hladane_ecv = hladany_kluc
                hladany_zakaznik_ecv = HashZakaznikECV(hladane_ecv, -1)
                vrateny_zaznam: HashZakaznikECV = self.__hash_zakaznici_podla_ecv.vrat_zaznam(hladany_zakaznik_ecv)
                if vrateny_zaznam is not None:
                    adresa_v_heapfile = vrateny_zaznam.get_adresa()
                    vrateny_zakaznik: Zakaznik = self.__heap_zakaznici.vrat_zaznam(adresa_v_heapfile, Zakaznik('','',-1,hladane_ecv))

                    if vrateny_zakaznik is not None:
                        konzola.config(state='normal')
                        konzola.insert(tk.END, f"Zákazník {vrateny_zakaznik.to_string()} bol úspešne nájdený!\n")
                        konzola.insert(tk.END, f"{vrateny_zakaznik.to_full_string()}\n")
                        konzola.config(state='disabled')
                        konzola.see(tk.END)
                        return copy.deepcopy(vrateny_zakaznik)
                    else:
                        konzola.config(state='normal')
                        konzola.insert(tk.END, f"Zákazníka s ECV: {hladany_kluc} sa nepodarilo nájsť!\n")
                        konzola.config(state='disabled')
                        konzola.see(tk.END)
                        return None
                else:
                    konzola.config(state='normal')
                    konzola.insert(tk.END, f"Zákazníka s ECV: {hladany_kluc} sa nepodarilo nájsť!\n")
                    konzola.config(state='disabled')
                    konzola.see(tk.END)
                    return None
    

    #2
    def pridaj_vozidlo(self, meno: str, priezvisko: str, id: int, ecv: str, konzola: tk.Text) -> bool:
        """
        Pridá nového zákazníka do systému.
        """
        kontrolovany_zakaznik_id = HashZakaznikID(id, -1)
        kontrolovany_zakaznik_ecv = HashZakaznikECV(ecv, -1)
        
        hladany_zakaznik_id = self.__hash_zakaznici_podla_id.vrat_zaznam(kontrolovany_zakaznik_id)
        hladany_zakaznik_ecv = self.__hash_zakaznici_podla_ecv.vrat_zaznam(kontrolovany_zakaznik_ecv)
        if hladany_zakaznik_id is None and hladany_zakaznik_ecv is None:
            novy_zakaznik = Zakaznik(meno, priezvisko, id, ecv)
            adresa = self.__heap_zakaznici.vloz_zaznam(novy_zakaznik)
            if adresa != -1:
                self.__hash_zakaznici_podla_id.vloz_zaznam(HashZakaznikID(id, adresa))
                self.__hash_zakaznici_podla_ecv.vloz_zaznam(HashZakaznikECV(ecv, adresa))

                konzola.config(state='normal')
                konzola.insert(tk.END, f"Zákazník {meno} {priezvisko} bol úspešne pridaný do systému!\n")
                konzola.config(state='disabled')
                konzola.see(tk.END)
                
                return True
            else:
                return False
        else:
            if hladany_zakaznik_id is not None and hladany_zakaznik_ecv is not None:
                vypis = f"Zákazník s ID: {id} a ECV: {ecv} už je evidovaný v systéme!\n"
            elif hladany_zakaznik_id is not None:
                vypis = f"Zákazník s ID: {id} už je evidovaný v systéme!\n"
            elif hladany_zakaznik_ecv is not None:
                vypis = f"Zákazník s ECV: {ecv} už je evidovaný v systéme!\n"

            konzola.config(state='normal')
            konzola.insert(tk.END, f"{vypis}\n")
            konzola.config(state='disabled')
            konzola.see(tk.END)
            
            return False

    #3
    def pridaj_navstevu_servisu(self, kluc, rok, mesiac, den, cena, popis_prac: List[str], konzola: tk.Text) -> bool:
        """
        Pridá nový záznam o návšteve servisu zákazníkovi.
        """
        
        if isinstance(kluc, int):
            hladany_zakaznik_id: HashZakaznikID = self.__hash_zakaznici_podla_id.vrat_zaznam(HashZakaznikID(kluc, -1))
            adresa_v_heapfile = hladany_zakaznik_id.get_adresa()
            najdeny_zakaznik: Zakaznik = self.__heap_zakaznici.vrat_zaznam(adresa_v_heapfile, Zakaznik('','',kluc,''))

        elif isinstance(kluc, str):
        
            hladany_zakaznik_ecv: HashZakaznikECV = self.__hash_zakaznici_podla_ecv.vrat_zaznam(HashZakaznikECV(kluc, -1))
            adresa_v_heapfile = hladany_zakaznik_ecv.get_adresa()
            najdeny_zakaznik = self.__heap_zakaznici.vrat_zaznam(adresa_v_heapfile, Zakaznik('','',-1,kluc))

        if najdeny_zakaznik is not None:
            datum = datetime(rok, mesiac, den)
            cena = float(cena)
            novy_zaznam = ZaznamONavsteve(datum, cena)
            for popis in popis_prac:
                novy_zaznam.pridaj_popis_prac(popis)

            if najdeny_zakaznik.pridaj_zaznam_o_navsteve(novy_zaznam):
                if self.__heap_zakaznici.aktualizuj_zaznam(adresa_v_heapfile, najdeny_zakaznik):


                    konzola.config(state='normal')
                    konzola.insert(tk.END, f"Návšteva zákazníka s kľúčom {kluc} bola úspešne pridaná!\n")
                    konzola.config(state='disabled')
                    konzola.see(tk.END)
                    
                    return True
            else:
                konzola.config(state='normal')
                konzola.insert(tk.END, f"Návštevu zákazníka s kľúčom {kluc} nebolo možné pridať!\n")
                konzola.config(state='disabled')
                konzola.see(tk.END)
                return False
            
                
        else:
            konzola.config(state='normal')
            konzola.insert(tk.END, f"Zákazník s kľúčom {kluc} nebol nájdený!\n")
            konzola.config(state='disabled')
            konzola.see(tk.END)
            return False
        
        

    #4
    def edituj_zaznam(self, editovany_zakaznik: Zakaznik, konzola: tk.Text) -> bool:
        """
        Upraví záznam zákazníka.
        """
        if isinstance(editovany_zakaznik, Zakaznik):
            hladany_zakaznik_id: HashZakaznikID = self.__hash_zakaznici_podla_id.vrat_zaznam(HashZakaznikID(editovany_zakaznik.get_id(), -1))
            adresa_v_heapfile = hladany_zakaznik_id.get_adresa()
            

            if hladany_zakaznik_id is not None:

                if self.__heap_zakaznici.aktualizuj_zaznam(adresa_v_heapfile, editovany_zakaznik):
                    konzola.config(state='normal')
                    konzola.insert(tk.END, f"Zákazník s ID: {editovany_zakaznik.get_id()} a ECV: {editovany_zakaznik.get_ecv()} bol úspešne upravený!\n")
                    konzola.config(state='disabled')
                    konzola.see(tk.END)
                    return True
                else:
                    konzola.config(state='normal')
                    konzola.insert(tk.END, f"Zákazníka s ID: {editovany_zakaznik.get_id()} a ECV: {editovany_zakaznik.get_ecv()} sa nepodarilo aktualizovať!\n")
                    konzola.config(state='disabled')
                    konzola.see(tk.END)
                    return False
            else:
                konzola.config(state='normal')
                konzola.insert(tk.END, f"Zákazník s ID: {editovany_zakaznik.get_id()} a ECV: {editovany_zakaznik.get_ecv()} neexistuje!\n")
                konzola.config(state='disabled')
                konzola.see(tk.END)
                return False


    #5 Generovanie udajov
    def generuj_udaje(self, pocet_pozadovanych_udajov: int, konzola: tk.Text):
        """
        Generuje náhodné záznamy zákazníkov.
        """
        konzola.config(state='normal')
        konzola.insert(tk.END, f"Generujem {pocet_pozadovanych_udajov} zákazníkov...\n")
        konzola.config(state='disabled')
        konzola.see(tk.END)
        
        pocet_vygenerovanych_udajov = 0

        while pocet_vygenerovanych_udajov < pocet_pozadovanych_udajov:
            nahodne_meno = self.__vygeneruj_string(15)
            nahodne_priezvisko = self.__vygeneruj_string(20)
            id = random.randint(1, 100000)
            ecv = self.__vygeneruj_string(10)

            kontrolovany_zakaznik_id = HashZakaznikID(id, -1)
            kontrolovany_zakaznik_ecv = HashZakaznikECV(ecv, -1)
            
            #Nenachádzajú sa ani v jednom zo súborov -> môžem pridať, keďže ID aj ECV sú unikátne
            if self.__hash_zakaznici_podla_id.vrat_zaznam(kontrolovany_zakaznik_id) is None and self.__hash_zakaznici_podla_ecv.vrat_zaznam(kontrolovany_zakaznik_ecv) is None:
                vygenerovany_zakaznik = Zakaznik(nahodne_meno, nahodne_priezvisko, id, ecv)
                pocet_zaznamov_o_navsteve = random.randint(1, 5)

                for i in range(pocet_zaznamov_o_navsteve):
                    datum = self.__vygeneruj_nahodny_datum()
                    nahodna_cena = round(random.uniform(10, 10000), 2)
                    vygenerovany_zaznam = ZaznamONavsteve(datum, nahodna_cena)
                    nahodny_pocet_popisov_prac = random.randint(1, 10)

                    for j in range(nahodny_pocet_popisov_prac):
                        vygenerovany_zaznam.pridaj_popis_prac(self.__vygeneruj_string(20))
                        
                    vygenerovany_zakaznik.pridaj_zaznam_o_navsteve(vygenerovany_zaznam)

                adresa = self.__heap_zakaznici.vloz_zaznam(vygenerovany_zakaznik)
                if adresa != -1:
                    self.__hash_zakaznici_podla_id.vloz_zaznam(HashZakaznikID(id, adresa))
                    self.__hash_zakaznici_podla_ecv.vloz_zaznam(HashZakaznikECV(ecv, adresa))
                    pocet_vygenerovanych_udajov += 1
                    
                    konzola.config(state='normal')
                    konzola.insert(tk.END, f"{pocet_vygenerovanych_udajov}. Vytvorený zákazník: {vygenerovany_zakaznik.to_string()} Počet návštev: {len(vygenerovany_zakaznik.get_navstevy())}\n")
                    konzola.config(state='disabled')
                    konzola.see(tk.END)

    #6
    def sekvencny_vypis(self, volba: int, konzola: tk.Text):
        """
        Vypíše sekvenčne súbor, ktorý bol zvolený.
        """
        if volba == 1:
            vypis = self.__heap_zakaznici.sekvencny_vypis()
        elif volba == 2:
            vypis = self.__hash_zakaznici_podla_id.sekvencny_vypis()
        elif volba == 3:
            vypis = self.__hash_zakaznici_podla_ecv.sekvencny_vypis()
        

        konzola.config(state='normal')
        konzola.insert(tk.END, f"{vypis}\n")
        konzola.config(state='disabled')
        konzola.see(tk.END)
        


    def __vygeneruj_string(self, maximalna_dlzka: int) -> str:
        """
        Vygeneruje náhodný string s maximálnou zadanou dĺžkou.
        """
        nahodna_dlzka = random.randint(1, maximalna_dlzka)
        pismena = string.ascii_letters
        return ''.join(random.choice(pismena) for i in range(nahodna_dlzka))
    
    def __vygeneruj_nahodny_datum(self) -> datetime:
        """
        Vygeneruje náhodný dátum od 1.1.1980 do 31.12.2024.
        """
        zaciatocny_datum = datetime(1980, 1, 1)
        konecny_datum = datetime(2024, 12, 31)
        nahodny_pocet_dni = random.randint(0, (konecny_datum - zaciatocny_datum).days)
        nahodny_datum = zaciatocny_datum + timedelta(days=nahodny_pocet_dni)
        
        return nahodny_datum

    