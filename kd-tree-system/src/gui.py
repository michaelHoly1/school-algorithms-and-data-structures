import tkinter as tk
from tkinter import ttk
from system.vyhladavaci_system import System


class GUI:
    """
    GUI pre vyhľadávací systém
    Tento modul obsahuje triedu GUI, ktorá vytvára jednoduché užívateľské rozhranie pre vyhľadávací systém pomocou knižnice tkinter.
    """
   
    def __init__(self, root):
        """
        Inicializuje GUI a nastaví základné prvky - ako napr. menu, tlačidlá, vstupné polia, konzolu atď.
        """
        self.root = root
        self.root.title("GUI pre vyhladavaci system")
        self.index_zvolenej_operacie = 0
        self.vyhladavaci_system = System()
        self.najdene_objekty = []
        
        # Nastavenie veľkosti okna
        self.root.geometry('1300x650')
        self.root.resizable(True, True)

        # Hlavné menu
        self.menu = tk.Menu(self.root)
        self.root.config(menu=self.menu)

        # Systémové menu
        self.ukladanie_menu = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="Systém", menu=self.ukladanie_menu)
        self.ukladanie_menu.add_command(label="1 Ulož", command= lambda: self.zvolenie_operacie(9))
        self.ukladanie_menu.add_command(label="2 Načítaj", command= lambda: self.zvolenie_operacie(10))
        self.ukladanie_menu.add_command(label="3 Generuj", command= lambda: self.zvolenie_operacie(11))
        
        # Menu pre operácie
        self.operacie_menu = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="Operácie", menu=self.operacie_menu)
        for i in range(9):
            self.operacie_menu.add_command(label=f"{self.get_nazov_operacie(i)}", command=lambda i=i: self.zvolenie_operacie(i))

        # Inicializácia prvkov GUI:

        # Popis zvolenej operácie
        self.zvolena_operacia = tk.Label(self.root, text="Zvolená operácia: ")
        self.zvolena_operacia.grid(row=0, column=0, padx=10, pady=10, sticky='w')

        # Vstupné pole pre prácu so súborom
        self.praca_so_suborom_input_frame = tk.Frame(self.root)
        self.praca_so_suborom_input_frame.grid(row=1, column=0, padx=10, pady=10, sticky='nw')
        self.praca_so_suborom_popis = tk.Label(self.praca_so_suborom_input_frame, text='Názov súboru')
        self.praca_so_suborom_popis.grid(row=1, column=0, padx=5, pady=2, sticky='e')
        self.praca_so_suborom_input_okno = tk.Entry(self.praca_so_suborom_input_frame, width=30)
        self.praca_so_suborom_input_okno.grid(row=1, column=1, padx=5, pady=2, sticky='w')

        # Vstupné polia pre generovanie
        self.generovanie_input_frame = tk.Frame(self.root)
        self.generovanie_popis = [tk.Label(self.generovanie_input_frame, text='Počet generovaných nehnuteľností'), tk.Label(self.generovanie_input_frame, text='Počet generovaných parciel'), tk.Label(self.generovanie_input_frame, text='Prekrytie ')]
        self.generovanie_input_okna = [tk.Entry(self.generovanie_input_frame, width=20) for _ in range(3)]

        # Vstupné polia pre prvú súradnicu
        self.pozicia1_input_frame = tk.Frame(self.root)
        self.pozicia1_popis = [tk.Label(self.pozicia1_input_frame, text='Zemepisná šírka 1'), tk.Label(self.pozicia1_input_frame, text='Zemepisná dĺžka 1')]
        self.pozicia1_input_okna = [tk.Entry(self.pozicia1_input_frame, width=30) for _ in range(2)]
        self.pozicia1_combo_boxes = [
            ttk.Combobox(self.pozicia1_input_frame, values=["N", "S"], width=28),
            ttk.Combobox(self.pozicia1_input_frame, values=["W", "E"], width=28)
        ]
        
        # Vstupné polia pre druhú súradnicu
        self.pozicia2_input_frame = tk.Frame(self.root)
        self.pozicia2_popis = [tk.Label(self.pozicia2_input_frame, text='Zemepisná šírka 2'), tk.Label(self.pozicia2_input_frame, text='Zemepisná dĺžka 2')]
        self.pozicia2_input_okna = [tk.Entry(self.pozicia2_input_frame, width=30) for _ in range(2)]
        self.pozicia2_combo_boxes = [
            ttk.Combobox(self.pozicia2_input_frame, values=["N", "S"], width=28),
            ttk.Combobox(self.pozicia2_input_frame, values=["W", "E"], width=28)
        ]

        # Vstupné polia pre vkladanie
        self.vkladanie_input_frame = tk.Frame(self.root)
        self.vkladanie_popis = [tk.Label(self.vkladanie_input_frame, text='Číslo'), tk.Label(self.vkladanie_input_frame, text='Popis')]
        self.vkladanie_input_okna = [tk.Entry(self.vkladanie_input_frame, width=30) for _ in range(2)]

       
        # Tlačidlo pre spustenie operácie
        self.spustit_button = tk.Button(self.root, text="Spustiť", command=self.spusti_operaciu)
        self.spustit_button.grid(row=11, column=0, padx=10, pady=10, sticky='w')

        # Tlačidlo pre vyhľadanie objektov
        self.vyhladaj_button = tk.Button(self.root, text="Vyhľadaj", command=self.vyhladaj_objekty)
        
        
        # Listbox pre voľbu z nájdených objektov
        self.listbox_frame = tk.Frame(self.root)
        self.listbox_frame.grid(row=15, column=0, rowspan=4, padx=10, pady=10, sticky='nsew')

        self.najdene_objekty_listbox = tk.Listbox(self.listbox_frame, height=10, selectmode=tk.SINGLE)
        self.najdene_objekty_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.listbox_scrollbar = tk.Scrollbar(self.listbox_frame, command=self.najdene_objekty_listbox.yview)
        self.listbox_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.najdene_objekty_listbox.config(yscrollcommand=self.listbox_scrollbar.set)
        self.najdene_objekty_listbox.bind("<<ListboxSelect>>", self.volba_z_listboxu)

        # Konzola
        self.console_output_frame = tk.Frame(self.root)
        self.console_output_frame.grid(row=20, column=0, padx=10, pady=10, sticky='nsew')
        
        self.console_output = tk.Text(self.console_output_frame, height=10, width=80,  state='disabled') #30x100
        self.console_output.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.scrollbar = tk.Scrollbar(self.console_output_frame, command=self.console_output.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.console_output.config(yscrollcommand=self.scrollbar.set)

    
    """
    Vráti názov operácie na základe indexu stlačeného tlačidla.
    """
    def get_nazov_operacie(self, index_operacie):
        nazvy_operacii = [
            '1 Vyhľadanie nehnuteľností', '2 Vyhľadanie parciel', '3 Vyhľadanie všetkých objektov',
            '4 Pridanie nehnuteľnosti', '5 Pridanie parcely', '6 Editácia nehnuteľnosti',
            '7 Editácia parcely', '8 Vymazanie nehnuteľnosti', '9 Vymazanie parcely'
        ]
        return nazvy_operacii[index_operacie]
    

    def zvolenie_operacie(self, index_operacie):
        """
        Nastaví zvolenú operáciu na základe indexu stlačeného tlačidla a prepíše obsah prvkov GUI.
        """
        self.index_zvolenej_operacie = index_operacie
        if index_operacie == 0:
            self.zvolena_operacia.config(text="Zvolená operácia: Vyhľadanie nehnuteľností\nPopis: Zadaj suradnicu vyhladavanej nehnuteľnosti")
        elif index_operacie == 1:
            self.zvolena_operacia.config(text="Zvolená operácia: Vyhľadanie parciel\nPopis: Zadaj suradnicu vyhladavanej parcely")
        elif index_operacie == 2:
            self.zvolena_operacia.config(text="Zvolená operácia: Vyhľadanie všetkých objektov\nPopis: Zadaj suradnice vyhladavanej oblasti")
        elif index_operacie == 3:
            self.zvolena_operacia.config(text="Zvolená operácia: Pridanie nehnuteľnosti\nPopis: Zadaj hodnoty pre novu nehnuteľnost")
        elif index_operacie == 4:
            self.zvolena_operacia.config(text="Zvolená operácia: Pridanie parcely\nPopis: Zadaj hodnoty pre novu parcelu")
        elif index_operacie == 5:
            self.zvolena_operacia.config(text="Zvolená operácia: Editácia nehnuteľnosti\nPopis: Vyhľadaj podľa prvej súradnice nehnuteľnosť, zvoľ ktorú chceš editovať a uprav jej hodnoty")
        elif index_operacie == 6:
            self.zvolena_operacia.config(text="Zvolená operácia: Editácia parcely\nPopis: Vyhľadaj podľa prvej súradnice parcely, zvoľ ktorú chceš editovať a uprav jej hodnoty")
        elif index_operacie == 7:
            self.zvolena_operacia.config(text="Zvolená operácia: Vymazanie nehnuteľnosti\nPopis: Zvoľ nehnuteľnosť ktorú chceš odstrániť")
        elif index_operacie == 8:
            self.zvolena_operacia.config(text="Zvolená operácia: Vymazanie parcely\nPopis: Zvoľ parcelu ktorú chceš odstrániť")
        elif index_operacie == 9:
            self.zvolena_operacia.config(text="Zvolená operácia: Uloženie\nPopis: Zadaj názov súboru do akého chceš uložiť dáta")
        elif index_operacie == 10:
            self.zvolena_operacia.config(text="Zvolená operácia: Načítanie\nPopis: Zadaj názov súboru z ktorého chceš načítať dáta")
        elif index_operacie == 11:
            self.zvolena_operacia.config(text="Zvolená operácia: Generovanie\nPopis: Zadaj parametre pre generovanie dát")
        
        self.vykresli_prvky(index_operacie)


    def vykresli_prvky(self, index_operacie):
        """
        Zobrazí prvky GUI na základe zvolenej operácie.
        """
        self.skry_prvky()
        self.console_output.config(height=20, width=80)

        # Zobrazenie prvkov GUI pre operácie 1 - 2
        if index_operacie in [0, 1]:
            self.pozicia1_input_frame.grid(row=1, column=0, rowspan=4, padx=10, pady=10, sticky='nw')
            
            for idx, label in enumerate(self.pozicia1_popis):
                label.grid(row=idx , column=0, padx=5, pady=2, sticky='e')
            
            for idx, input_field in enumerate(self.pozicia1_input_okna):
                input_field.grid(row=idx , column=1, padx=5, pady=2, sticky='w')
            
            for idx, combo_box in enumerate(self.pozicia1_combo_boxes):
                combo_box.grid(row=idx , column=2, padx=5, pady=2, sticky='w')

        # Zobrazenie prvkov GUI pre operácie spojené s prácou so súborom
        elif index_operacie in [9,10]:
            self.praca_so_suborom_input_frame.grid(row=1, column=0, padx=10, pady=10, sticky='nw')
            self.praca_so_suborom_popis.grid(row=1, column=0, padx=5, pady=2, sticky='e')
            self.praca_so_suborom_input_okno.grid(row=1, column=1, padx=5, pady=2, sticky='w')
            self.console_output.config(height=25, width=100)

        # Zobrazenie prvkov GUI pre generovanie dát
        elif index_operacie == 11:
            self.generovanie_input_frame.grid(row=1, column=0, padx=10, pady=10, sticky='nw')
            for idx, label in enumerate(self.generovanie_popis):
                label.grid(row=idx , column=0, padx=5, pady=2, sticky='w')
            for idx, input_field in enumerate(self.generovanie_input_okna):
                input_field.grid(row=idx , column=1, padx=5, pady=2, sticky='w')
                self.console_output.config(height=25, width=100)


        # Zobrazenie prvkov GUI pre operácie 3 - 9
        else:

            if index_operacie in [2,3,4,5,6]:

                self.pozicia2_input_frame.grid(row=1, column=3, rowspan=4, padx=10, pady=10, sticky='nw')

                for idx, label in enumerate(self.pozicia2_popis):
                    label.grid(row=idx , column=3, padx=5, pady=2, sticky='e')

                for idx, input_field in enumerate(self.pozicia2_input_okna):
                    input_field.grid(row=idx , column=4, padx=5, pady=2, sticky='w')

                for idx, combo_box in enumerate(self.pozicia2_combo_boxes):
                    combo_box.grid(row=idx , column=5, padx=5, pady=2, sticky='w')

                self.vkladanie_input_frame.grid(row = 6, column=0, rowspan=4, padx=10, pady=10, sticky='nw')

                for idx, label in enumerate(self.vkladanie_popis):
                    label.grid(row=idx , column=0, padx=5, pady=2, sticky='w')

                for idx, input_field in enumerate(self.vkladanie_input_okna):
                    input_field.grid(row=idx , column=1, padx=5, pady=2, sticky='w')
            
            
            self.pozicia1_input_frame.grid(row=1, column=0, rowspan=4, padx=10, pady=10, sticky='nw')
            
            for idx, label in enumerate(self.pozicia1_popis):
                label.grid(row=idx , column=0, padx=5, pady=2, sticky='e')
            
            for idx, input_field in enumerate(self.pozicia1_input_okna):
                input_field.grid(row=idx , column=1, padx=5, pady=2, sticky='w')
            
            for idx, combo_box in enumerate(self.pozicia1_combo_boxes):
                combo_box.grid(row=idx , column=2, padx=5, pady=2, sticky='w')

            if index_operacie in [5,6,7,8]:
                self.listbox_frame.grid(row=15, column=0, rowspan=4, padx=10, pady=10, sticky='nsew')
                self.vyhladaj_button.grid(row=11, column=1, padx=10, pady=10, sticky='w')
                self.console_output.config(height=12, width=80)
        

    def skry_prvky(self):
        """
        Skryje všetky prvky GUI, ktoré by sa mohli prekrívať.
        """
        
        self.praca_so_suborom_input_frame.grid_forget()
        self.generovanie_input_frame.grid_forget()
        self.pozicia1_input_frame.grid_forget()
        self.pozicia2_input_frame.grid_forget()
        self.vkladanie_input_frame.grid_forget()
        self.listbox_frame.grid_forget()
        self.vyhladaj_button.grid_forget()

    def spusti_operaciu(self):
        """
        Vykoná príslušné akcie a spustí zvolenú operáciu.
        """
        self.zapis_do_konzoly(f"Spustenie operácie {self.index_zvolenej_operacie + 1} \n")
        vsetko_ok = True
        
        # Výber hôdnot z jednotlivých vstupných polí

        # Výber hodnôt pre prácu so súborom
        nazov_suboru = self.praca_so_suborom_input_okno.get()

        # Výber hodnôt pre generovanie
        pocet_nehnutelnosti = self.generovanie_input_okna[0].get()
        pocet_parciel = self.generovanie_input_okna[1].get()
        prekrytie = self.generovanie_input_okna[2].get()
        
        # Výber hodnôt zadaných pre pozíciu 1
        sirka1 = self.pozicia1_combo_boxes[0].get()
        pozicia_sirky1 = self.pozicia1_input_okna[0].get()
        dlzka1 = self.pozicia1_combo_boxes[1].get()
        pozicia_dlzky1 = self.pozicia1_input_okna[1].get()

        # Výber hodnôt zadaných pre pozíciu 2
        sirka2 = self.pozicia2_combo_boxes[0].get()
        pozicia_sirky2 = self.pozicia2_input_okna[0].get()
        dlzka2 = self.pozicia2_combo_boxes[1].get()
        pozicia_dlzky2 = self.pozicia2_input_okna[1].get()

        # Výber hodnôt pre vkladanie

        cislo = self.vkladanie_input_okna[0].get()
        popis = self.vkladanie_input_okna[1].get()

        
        if self.index_zvolenej_operacie in [0,1,2,3,4,5,6]:

            # Kontroly vstupných hodnôt pre všetky operácie

            # Kontrola vstupu pre poziciu 1
            if not all([sirka1, pozicia_sirky1, dlzka1, pozicia_dlzky1]):
                self.zapis_do_konzoly('Error: Všetky polia musia byť vyplnené')
                vsetko_ok = False

            try:
                pozicia_sirky1 = float(pozicia_sirky1)
                pozicia_dlzky1 = float(pozicia_dlzky1)

                if pozicia_sirky1 < 0 or pozicia_sirky1 > 90:
                    raise ValueError
                elif pozicia_dlzky1 < 0 or pozicia_dlzky1 > 180:
                    raise ValueError
            except ValueError:
                self.zapis_do_konzoly('Error: Nesprávne zadané hodnoty')
                vsetko_ok = False

            # Kontrola vstupu pre poziciu 2
            if self.index_zvolenej_operacie in [2,3,4,5,6]:

                if not all([sirka2, pozicia_sirky2, dlzka2, pozicia_dlzky2]):
                    self.zapis_do_konzoly('Error: Všetky polia musia byť vyplnené')
                    vsetko_ok = False

                try:
                    pozicia_sirky2 = float(pozicia_sirky2)
                    pozicia_dlzky2 = float(pozicia_dlzky2)

                    if pozicia_sirky2 < 0 or pozicia_sirky2 > 90:
                        raise ValueError
                    elif pozicia_dlzky2 < 0 or pozicia_dlzky2 > 180:
                        raise ValueError

                    if self.index_zvolenej_operacie in [3,4,5,6]:
                        cislo = int(cislo)

                except ValueError:
                    self.zapis_do_konzoly('Error: Nesprávne zadané hodnoty')
                    vsetko_ok = False

        # Kontrola vstupu pre prácu so súborom
        elif self.index_zvolenej_operacie in [9,10]:
            if not nazov_suboru:
                self.zapis_do_konzoly('Error: Názov súboru musí byť vyplnený')
                vsetko_ok = False

        # Kontrola vstupu pre generovanie
        elif self.index_zvolenej_operacie == 11:
            if not all([pocet_nehnutelnosti, pocet_parciel, prekrytie]):
                self.zapis_do_konzoly('Error: Všetky polia musia byť vyplnené')
                vsetko_ok = False

            try:
                pocet_nehnutelnosti = int(pocet_nehnutelnosti)
                pocet_parciel = int(pocet_parciel)
                prekrytie = float(prekrytie)

                if pocet_nehnutelnosti <= 0 or pocet_parciel > pocet_nehnutelnosti or prekrytie < 0 or prekrytie > 1:
                    raise ValueError

            except ValueError:
                self.zapis_do_konzoly('Error: Nesprávne zadané hodnoty')
                vsetko_ok = False

        if vsetko_ok:

            if self.index_zvolenej_operacie in [0,1,2]:

                if self.index_zvolenej_operacie == 0:
                    self.najdene_objekty = self.vyhladavaci_system.najdi_nehnutelnosti(sirka1, pozicia_sirky1, dlzka1, pozicia_dlzky1)
                elif self.index_zvolenej_operacie == 1:
                    self.najdene_objekty = self.vyhladavaci_system.najdi_parcely(sirka1, pozicia_sirky1, dlzka1, pozicia_dlzky1)
                else:
                    self.najdene_objekty = self.vyhladavaci_system.najdi_vsetky_objekty(sirka1, pozicia_sirky1, dlzka1, pozicia_dlzky1, sirka2, pozicia_sirky2, dlzka2, pozicia_dlzky2)
                
                if self.najdene_objekty:
                    self.najdene_objekty_listbox.delete(0, tk.END)
                    for objekt in self.najdene_objekty:
                        self.najdene_objekty_listbox.insert(tk.END, objekt.get_data().to_string())
                        self.zapis_do_konzoly(objekt.get_data().to_string())

                else:
                    pomenovanie_objektu = 'nehnuteľnosti' if self.index_zvolenej_operacie == 0 else 'parcely' if self.index_zvolenej_operacie == 1 else 'objekty'
                    self.zapis_do_konzoly(f'Nenašli sa žiadne {pomenovanie_objektu} na danej pozícii')

            elif self.index_zvolenej_operacie == 3:
                self.vyhladavaci_system.pridaj_nehnutelnost(cislo, popis, sirka1, pozicia_sirky1, dlzka1, pozicia_dlzky1, sirka2, pozicia_sirky2, dlzka2, pozicia_dlzky2)

            elif self.index_zvolenej_operacie == 4:
                self.vyhladavaci_system.pridaj_parcelu(cislo, popis, sirka1, pozicia_sirky1, dlzka1, pozicia_dlzky1, sirka2, pozicia_sirky2, dlzka2, pozicia_dlzky2)
            
            elif self.index_zvolenej_operacie in [5,6]:

                if self.najdene_objekty_listbox.size() > 0:

                    if self.zvoleny_objekt:
                        
                        editovany_objekt = self.zvoleny_objekt
                        if self.index_zvolenej_operacie == 5:
                            vysledok_editacie = self.vyhladavaci_system.editacia_nehnutelnosti(editovany_objekt, cislo, popis, sirka1, pozicia_sirky1, dlzka1, pozicia_dlzky1, sirka2, pozicia_sirky2, dlzka2, pozicia_dlzky2)
                        else:
                            vysledok_editacie = self.vyhladavaci_system.editacia_parcely(editovany_objekt, cislo, popis, sirka1, pozicia_sirky1, dlzka1, pozicia_dlzky1, sirka2, pozicia_sirky2, dlzka2, pozicia_dlzky2)
                        
                        pomenovanie_objektu = 'Nehnuteľnosť' if self.index_zvolenej_operacie == 5 else 'Parcela'

                        if vysledok_editacie:
                            self.zapis_do_konzoly(f'{pomenovanie_objektu} bola úspešne editovaná')
                            self.najdene_objekty_listbox.delete(self.index_zvoleneho_objektu)
                        else:
                            self.zapis_do_konzoly(f'{pomenovanie_objektu} sa nepodarilo editovať')

                    else:
                        self.zapis_do_konzoly(f'Nebola vybraná {pomenovanie_objektu} na editáciu')

            elif self.index_zvolenej_operacie in [7,8]:
                if self.najdene_objekty_listbox.size() > 0:
                    
                    
                    if self.zvoleny_objekt:
            
                        vymazavany_objekt = self.zvoleny_objekt
                        if self.index_zvolenej_operacie == 7:
                            vysledok_mazania = self.vyhladavaci_system.vyradenie_nehnutelnosti(vymazavany_objekt)
                        else:
                            vysledok_mazania = self.vyhladavaci_system.vyradenie_parcely(vymazavany_objekt)


                        pomenovanie_objektu = 'Nehnuteľnosť' if self.index_zvolenej_operacie == 7 else 'Parcela'
                        if vysledok_mazania:
                            self.zapis_do_konzoly(f'{pomenovanie_objektu} bola úspešne vymazaná')
                            self.najdene_objekty.remove(vymazavany_objekt)
                            self.najdene_objekty_listbox.delete(self.index_zvoleneho_objektu)

                        else:
                            self.zapis_do_konzoly(f'{pomenovanie_objektu} sa nepodarilo vymazať')
                    else:
                        self.zapis_do_konzoly(f'Nebola vybraná {pomenovanie_objektu} na vymazanie')

                else:
                    self.zapis_do_konzoly('Neboli vyhľadané žiadne objekty')

            elif self.index_zvolenej_operacie == 9:
                vysledok_ukladania = self.vyhladavaci_system.uloz_do_suboru(nazov_suboru)
                if vysledok_ukladania:
                    self.zapis_do_konzoly('Dáta boli úspešne uložené')
                else:
                    self.zapis_do_konzoly('Dáta sa nepodarilo uložiť')

            elif self.index_zvolenej_operacie == 10:
                self.vyhladavaci_system.nacitaj_zo_suboru(nazov_suboru, self.console_output)

            elif self.index_zvolenej_operacie == 11:
                self.vyhladavaci_system.generuj_data(pocet_nehnutelnosti, pocet_parciel, prekrytie, self.console_output)


    def vyhladaj_objekt(self):
        """
        Vyhľadá objekty na základe zvolenej operácie.
        """
        if self.index_zvolenej_operacie in [5,7]:
            povodny_index = self.index_zvolenej_operacie
            self.index_zvolenej_operacie = 0
            self.spusti_operaciu()
            self.index_zvolenej_operacie = povodny_index
        elif self.index_zvolenej_operacie in [6,8]:
            povodny_index = self.index_zvolenej_operacie
            self.index_zvolenej_operacie = 1
            self.spusti_operaciu()
            self.index_zvolenej_operacie = povodny_index
    
    def volba_z_listboxu(self, event):
        """
        Spracuje výber objektu z listboxu.
        """
        index = self.najdene_objekty_listbox.curselection()
        if index and self.index_zvolenej_operacie in [5,6,7,8]:
            index = index[0]
            self.zvoleny_objekt = self.najdene_objekty[index]
            self.index_zvoleneho_objektu = index

            self.aktualizuj_vstupne_elementy(self.zvoleny_objekt)

    def aktualizuj_vstupne_elementy(self, objekt):
        """
        Aktualizuje vstupné polia pre operáciu editácie na základe vybraného objektu.
        """
        data = objekt.get_data()

        #Aktuálizácia hodnôť vo vstupných poliach počas editácie
        self.vkladanie_input_okna[0].delete(0, tk.END)
        self.vkladanie_input_okna[0].insert(0, data.get_cislo())
        self.vkladanie_input_okna[1].delete(0, tk.END)
        self.vkladanie_input_okna[1].insert(0, data.get_popis())

        self.pozicia1_input_okna[0].delete(0, tk.END)
        self.pozicia1_input_okna[0].insert(0, abs(data.get_pozicia_GPS1().get_pozicia_sirky()))
        self.pozicia1_input_okna[1].delete(0, tk.END)
        self.pozicia1_input_okna[1].insert(0, abs(data.get_pozicia_GPS1().get_pozicia_dlzky()))
        self.pozicia1_combo_boxes[0].set(data.get_pozicia_GPS1().get_sirka())
        self.pozicia1_combo_boxes[1].set(data.get_pozicia_GPS1().get_dlzka())

        self.pozicia2_input_okna[0].delete(0, tk.END)
        self.pozicia2_input_okna[0].insert(0, abs(data.get_pozicia_GPS2().get_pozicia_sirky()))
        self.pozicia2_input_okna[1].delete(0, tk.END)
        self.pozicia2_input_okna[1].insert(0, abs(data.get_pozicia_GPS2().get_pozicia_dlzky()))
        self.pozicia2_combo_boxes[0].set(data.get_pozicia_GPS2().get_sirka())
        self.pozicia2_combo_boxes[1].set(data.get_pozicia_GPS2().get_dlzka())


    def zapis_do_konzoly(self, message):
        """
        Zapíše správu do konzoly.
        """
        self.console_output.config(state='normal')
        self.console_output.insert(tk.END, message + '\n')
        self.console_output.config(state='disabled')
        self.console_output.see(tk.END)
    

if __name__ == "__main__":
    root = tk.Tk()
    app = GUI(root)
    root.mainloop()       
        