import tkinter as tk
from tkinter import ttk
from System.servis_system import ServisnySystem
from System.Zakaznik.zakaznik import Zakaznik
from System.Zakaznik.zaznam_o_navsteve import ZaznamONavsteve
from datetime import datetime


class GUI:
    """
    Trieda GUI reprezentuje grafické užívateľské rozhranie pre auto-servisný systém.
    Atribúty:
        root (tk.Tk): Hlavné okno aplikácie.
        index_zvolenej_operacie (int): Index zvolenej operácie.
        system (ServisnySystem): Inštancia servisného systému.
        najdeny_objekt (Zakaznik): Nájdený zákazník.
        index_zvolenej_navstevy (int): Index zvolenej návštevy.
        index_zvoleneho_popisu (int): Index zvoleného popisu.
        editovane_navstevy (List[ZaznamONavsteve]): Zoznam editovaných návštev.
        pocet_editovanych_navstev (int): Počet editovaných návštev.
    """
   
    def __init__(self, root):
        """
        Inicializuje GUI a nastaví základné prvky - ako napr. menu, tlačidlá, vstupné polia, konzolu atď.
        """
        self.root = root
        # Zabezpečí uzavretie súborov a uloženie riadiacich súborov pri zatvorení aplikácie
        self.root.protocol("WM_DELETE_WINDOW", self.ukladanie_dat)
        self.root.title("GUI pre auto-servisný systém")
        self.index_zvolenej_operacie = 0
        self.system = ServisnySystem()
        self.najdeny_objekt: Zakaznik = None
        self.index_zvolenej_navstevy = -1
        self.index_zvoleneho_popisu = -1
        self.editovane_navstevy = []
        self.pocet_editovanych_navstev = 0
        
        # Nastavenie veľkosti okna
        self.root.geometry('800x800')
        self.root.resizable(True, True)

        # Hlavné menu
        self.menu = tk.Menu(self.root)
        self.root.config(menu=self.menu)
        
        # Menu pre operácie
        self.operacie_menu = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="Operácie", menu=self.operacie_menu)
        for i in range(1, 7):
            self.operacie_menu.add_command(label=f"{self.get_nazov_operacie(i)}", command=lambda i=i: self.zvolenie_operacie(i))

        # Inicializácia prvkov GUI:

        # Popis zvolenej operácie
        self.zvolena_operacia_frame = tk.Frame(self.root)
        self.zvolena_operacia = tk.Label(self.zvolena_operacia_frame, text="Zvolená operácia: Nebola zvolená žiadna operácia")

        self.zvolena_operacia.config(text="Nebola zvolená žiadna operácia", font=("Helvetica", 16))

        self.zvolena_operacia_frame.grid(row=0, column=0, padx=10, pady=10, sticky='w')
        self.zvolena_operacia.pack(side=tk.LEFT, anchor="w")
        

        # Vstupné polia pre generovanie
        self.generovanie_input_frame = tk.Frame(self.root)
        self.generovanie_popis = tk.Label(self.generovanie_input_frame, text='Počet generovaných záznamov')
        self.generovanie_input_okno = tk.Entry(self.generovanie_input_frame, width=20)


        # Vstupné polia pre vyhľadávanie
        self.vyhladanie_input_frame = tk.Frame(self.root)
        self.vyhladanie_popis = tk.Label(self.vyhladanie_input_frame, text='Kľúč')
        self.vyhladanie_input_okno = tk.Entry(self.vyhladanie_input_frame, width=30)
        self.typ_vyhladavania_popis = tk.Label(self.vyhladanie_input_frame, text='Typ vyhľadávania')
        self.vyhladanie_typ_vyhladavania = ttk.Combobox(self.vyhladanie_input_frame, values=['Podľa ID', 'Podľa ECV'])
        self.vyhladaj_button = tk.Button(self.vyhladanie_input_frame, text="Vyhľadaj", command=self.vyhladaj_zaznam)

        
        # Vstupné polia pre vkladanie zákazníka
        self.vkladanie_input_frame = tk.Frame(self.root)
        self.vkladanie_popis = [tk.Label(self.vkladanie_input_frame, text='Meno'), tk.Label(self.vkladanie_input_frame, text='Priezvisko'), tk.Label(self.vkladanie_input_frame, text='ID'), tk.Label(self.vkladanie_input_frame, text='ECV')]
        self.vkladanie_input_okna = [tk.Entry(self.vkladanie_input_frame, width=30) for _ in range(4)]

        #Vstupné polia pre vkladanie návštevy servisu
        self.vkladanie_navsteva_input_frame = tk.Frame(self.root)
        self.vkladanie_navsteva_popis = [tk.Label(self.vkladanie_navsteva_input_frame, text='Deň'), tk.Label(self.vkladanie_navsteva_input_frame, text='Mesiac'), tk.Label(self.vkladanie_navsteva_input_frame, text='Rok'), tk.Label(self.vkladanie_navsteva_input_frame, text='Cena'), tk.Label(self.vkladanie_navsteva_input_frame, text='Popis práce')]
        self.vkladanie_navsteva_input_okna = [tk.Entry(self.vkladanie_navsteva_input_frame, width=30) for _ in range(5)]
        self.pridaj_button = tk.Button(self.vkladanie_navsteva_input_frame, text="Pridaj Popis", command=self.pridaj_popis)

        self.pridane_popisy_frame = tk.Frame(self.root)
        self.pridane_popisy_label = tk.Label(self.pridane_popisy_frame, text="Pridané popisy:")
        self.pridane_popisy_listbox = tk.Listbox(self.pridane_popisy_frame, height=5)
       
        # Tlačidlo pre spustenie operácie
        self.spustit_button = tk.Button(self.root, text="Spustiť", command=self.spusti_operaciu)
    

        # Konzola pre operacie 1 - 4
        self.console_output_frame = tk.Frame(self.root)
        self.console_output = tk.Text(self.console_output_frame, height=10, width=80,  state='disabled')

        # Konzola pre sekvencny vypis
        self.console_output_sekvencny_frame = tk.Frame(self.root)
        self.console_output_sekvencny = tk.Text(self.console_output_sekvencny_frame, height=10, width=80,  state='disabled') 
        

        self.sekvencny_scrollbar = tk.Scrollbar(self.console_output_sekvencny_frame, command=self.console_output_sekvencny.yview)
        self.console_output_sekvencny.config(yscrollcommand=self.sekvencny_scrollbar.set)

        #Prvky pre voľbu návštev
        self.volba_navstevy_frame = tk.Frame(self.root)
        self.volba_navstevy_listbox = tk.Listbox(self.volba_navstevy_frame, height=5)
        self.volba_navstevy_popis = tk.Label(self.volba_navstevy_frame, text="Vyberte návštevu")

        #Prvky pre sekvenčný výpis
        self.sekvencny_vypis_frame = tk.Frame(self.root)
        self.vyber_typu_suboru_combobox = ttk.Combobox(self.root, values=["Heapfile", "Hashfile ID", "Hashfile ECV"], width=20)
    
    def ukladanie_dat(self):
        """
        Uloží dáta do súboru pri zatvorení aplikácie a zavrie okno.
        """
        self.system.zavri_subory()
        self.root.destroy()

    
    def get_nazov_operacie(self, index_operacie):
        """
        Vráti názov operácie na základe indexu.
        """
        nazvy_operacii = [
            '1 Vyhľadanie záznamu', '2 Pridanie vozidla', '3 Pridanie návštevy servisu',
            '4 Zmena záznamu', '5 Generuj dáta', '6 Sekvenčný výpis štruktúr'
        ]
        return nazvy_operacii[index_operacie - 1]
    

    def zvolenie_operacie(self, index_operacie):
        """
        Nastaví zvolenú operáciu na základe indexu a prepíše obsah prvkov GUI, taktiež zavolá metódu pre vykreslenie ostatných prvkov v GUI.
        """
        self.index_zvolenej_operacie = index_operacie
        if index_operacie == 1:
            self.zvolena_operacia.config(text="Zvolená operácia: Vyhľadanie záznamu", font=("Helvetica", 16))
        elif index_operacie == 2:
            self.zvolena_operacia.config(text="Zvolená operácia: Pridanie vozidla", font=("Helvetica", 16))
        elif index_operacie == 3:
            self.zvolena_operacia.config(text="Zvolená operácia: Pridanie návštevy servisu", font=("Helvetica", 16))
        elif index_operacie == 4:
            self.zvolena_operacia.config(text="Zvolená operácia: Zmena evidovaných údajov", font=("Helvetica", 16))
        elif index_operacie == 5:
            self.zvolena_operacia.config(text="Zvolená operácia: Generovanie dát", font=("Helvetica", 16))
        elif index_operacie == 6:
            self.zvolena_operacia.config(text="Zvolená operácia: Vypísanie štruktúry sekvenčne", font=("Helvetica", 16))
         
        self.vykresli_prvky(index_operacie)


    def vykresli_prvky(self, index_operacie):
        """
        Zobrazí prvky GUI na základe zvolenej operácie.
        """
        self.skry_prvky()

        if index_operacie == 1:
            #Zvolená operácia
            self.zvolena_operacia_frame = tk.Frame(self.root)
            self.zvolena_operacia = tk.Label(self.zvolena_operacia_frame, text="Zvolená operácia: Vyhľadanie záznamu", font=("Helvetica", 16))
            self.zvolena_operacia_frame.grid(row=0, column=0, padx=10, pady=10, sticky='we')
            self.zvolena_operacia.grid(row=0, column=0, padx=10, pady=10, sticky='w')

            #Vstupné pole pre vyhľadávanie
            self.vyhladanie_input_frame = tk.Frame(self.root)
            self.vyhladanie_popis = tk.Label(self.vyhladanie_input_frame, text='Kľúč')
            self.vyhladanie_input_okno = tk.Entry(self.vyhladanie_input_frame, width=30)
            self.typ_vyhladavania_popis = tk.Label(self.vyhladanie_input_frame, text='Typ vyhľadávania')
            self.vyhladanie_typ_vyhladavania = ttk.Combobox(self.vyhladanie_input_frame, values=['Podľa ID', 'Podľa ECV'])
            self.vyhladaj_button = tk.Button(self.vyhladanie_input_frame, text="Vyhľadaj", command=self.vyhladaj_zaznam)
            
            self.vyhladanie_input_frame.grid(row=1, column=0, padx=10, pady=10, sticky='w')
            self.vyhladanie_popis.grid(row=0, column=0, padx=5, pady=5, sticky="w")
            self.vyhladanie_input_okno.grid(row=0, column=1, padx=5, pady=5)
            self.typ_vyhladavania_popis.grid(row=0, column=2, padx=5, pady=5, sticky="w")
            self.vyhladanie_typ_vyhladavania.grid(row=0, column=3, padx=5, pady=5)
            self.vyhladaj_button.grid(row=0, column=4, padx=5, pady=5)
            
            #Konzola pre výpis
            self.console_output_frame = tk.Frame(self.root)
            self.console_output_frame.grid(row=2, column=0, padx=10, pady=10, sticky='nsew')
            self.console_output = tk.Text(self.console_output_frame, height=10, width=80,  state='disabled')
            self.console_output.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')
            self.console_output.config(height=10)

            self.scrollbar = tk.Scrollbar(self.console_output_frame, command=self.console_output.yview)
            self.console_output.config(yscrollcommand=self.scrollbar.set)
            self.scrollbar.grid(row=0, column=1, sticky='ns')

            self.root.grid_rowconfigure(2, weight=1)
            self.root.grid_columnconfigure(0, weight=1)
            self.console_output_frame.grid_rowconfigure(0, weight=1)
            self.console_output_frame.grid_columnconfigure(0, weight=1)


        elif index_operacie == 2:
            
            #Zvolená operácia
            self.zvolena_operacia_frame = tk.Frame(self.root)
            self.zvolena_operacia = tk.Label(self.zvolena_operacia_frame, text="Zvolená operácia: Pridanie vozidla", font=("Helvetica", 16))
            self.zvolena_operacia_frame.grid(row=0, column=0, padx=10, pady=5, sticky='w')
            self.zvolena_operacia.pack(side=tk.LEFT, anchor="w")

            #Vstupné pole pre vkladanie zákazníka
            self.vkladanie_input_frame = tk.Frame(self.root)
            self.vkladanie_popis = [
                tk.Label(self.vkladanie_input_frame, text='Meno'),
                tk.Label(self.vkladanie_input_frame, text='Priezvisko'),
                tk.Label(self.vkladanie_input_frame, text='ID'),
                tk.Label(self.vkladanie_input_frame, text='ECV')
            ]
            self.vkladanie_input_okna = [tk.Entry(self.vkladanie_input_frame, width=30) for _ in range(4)]
            self.spustit_button = tk.Button(self.vkladanie_input_frame, text="Spustiť", command=self.spusti_operaciu)

            self.vkladanie_input_frame.grid(row=1, column=0, padx=10, pady=10, sticky='w')
            self.vkladanie_popis[0].grid(row=0, column=0, padx=5, pady=5, sticky="w")  
            self.vkladanie_input_okna[0].grid(row=0, column=1, padx=5, pady=5)  
            self.vkladanie_popis[2].grid(row=0, column=2, padx=5, pady=5, sticky="w")  
            self.vkladanie_input_okna[2].grid(row=0, column=3, padx=5, pady=5)  

            self.vkladanie_popis[1].grid(row=1, column=0, padx=5, pady=5, sticky="w")  
            self.vkladanie_input_okna[1].grid(row=1, column=1, padx=5, pady=5)  
            self.vkladanie_popis[3].grid(row=1, column=2, padx=5, pady=5, sticky="w")  
            self.vkladanie_input_okna[3].grid(row=1, column=3, padx=5, pady=5)  

            self.spustit_button.grid(row=2, column=0, columnspan=2, padx=20, pady=10, sticky='ew')
            self.console_output_frame = tk.Frame(self.root)
            self.console_output = tk.Text(self.console_output_frame, height=10, width=80,  state='disabled')
            self.scrollbar = tk.Scrollbar(self.console_output_frame, command=self.console_output.yview)
            
            #Konzola pre výpis
            self.console_output_frame.grid(row=3, column=0, columnspan=4, padx=10, pady=10, sticky='nsew')
            self.console_output.grid(row=0, column=0, sticky='nsew')
            self.console_output.config(yscrollcommand=self.scrollbar.set)
            self.scrollbar.grid(row=0, column=1, sticky='ns')

            self.console_output_frame.grid_rowconfigure(0, weight=1)
            self.console_output_frame.grid_columnconfigure(0, weight=1)
            self.root.grid_rowconfigure(3, weight=1)
            self.root.grid_columnconfigure(0, weight=1)


        elif index_operacie == 3:

            #Zvolená operácia
            self.zvolena_operacia_frame = tk.Frame(self.root)
            self.zvolena_operacia = tk.Label(self.zvolena_operacia_frame, text="Zvolená operácia: Pridanie návštevy auto servisu", font=("Helvetica", 16))
            self.zvolena_operacia_frame.grid(row=0, column=0, padx=10, pady=10, sticky='we')
            self.zvolena_operacia.grid(row=0, column=0, padx=10, pady=10, sticky='w')

            #Pole pre vyhľadanie zákazníka
            self.vyhladanie_input_frame = tk.Frame(self.root)
            self.vyhladanie_popis = tk.Label(self.vyhladanie_input_frame, text='Kľúč')
            self.vyhladanie_input_okno = tk.Entry(self.vyhladanie_input_frame, width=30)
            self.typ_vyhladavania_popis = tk.Label(self.vyhladanie_input_frame, text='Typ vyhľadávania')
            self.vyhladanie_typ_vyhladavania = ttk.Combobox(self.vyhladanie_input_frame, values=['Podľa ID', 'Podľa ECV'])
            self.vyhladaj_button = tk.Button(self.vyhladanie_input_frame, text="Vyhľadaj", command=self.vyhladaj_zaznam)
            self.spustit_button = tk.Button(self.vyhladanie_input_frame, text="Spustiť", command=self.spusti_operaciu)
            
            self.vyhladanie_input_frame.grid(row=1, column=0, padx=10, pady=10, sticky='w')
            self.vyhladanie_popis.grid(row=0, column=0, padx=5, pady=5, sticky="w")
            self.vyhladanie_input_okno.grid(row=0, column=1, padx=5, pady=5)
            self.typ_vyhladavania_popis.grid(row=0, column=2, padx=5, pady=5, sticky="w")
            self.vyhladanie_typ_vyhladavania.grid(row=0, column=3, padx=5, pady=5)
            self.vyhladaj_button.grid(row=0, column=4, padx=5, pady=5)
            self.spustit_button.grid(row=0, column=5, padx=5, pady=5)


            #Vstupné polia pre vkladanie návštevy servisu
            self.vkladanie_navsteva_input_frame = tk.Frame(self.root)
            self.vkladanie_navsteva_input_frame.grid(row=2, column=0, padx=10, pady=10, sticky='w')

            self.vkladanie_navsteva_popis = [
                tk.Label(self.vkladanie_navsteva_input_frame, text="Deň"),
                tk.Label(self.vkladanie_navsteva_input_frame, text="Mesiac"),
                tk.Label(self.vkladanie_navsteva_input_frame, text="Rok"),
                tk.Label(self.vkladanie_navsteva_input_frame, text="Cena"),
                tk.Label(self.vkladanie_navsteva_input_frame, text="Popis práce")
            ]
            self.vkladanie_navsteva_input_okna = [
                tk.Entry(self.vkladanie_navsteva_input_frame, width=10),
                tk.Entry(self.vkladanie_navsteva_input_frame, width=10),
                tk.Entry(self.vkladanie_navsteva_input_frame, width=10),
                tk.Entry(self.vkladanie_navsteva_input_frame, width=10),
                tk.Entry(self.vkladanie_navsteva_input_frame, width=40)
            ]

            self.pridaj_button = tk.Button(self.vkladanie_navsteva_input_frame, text="Pridaj Popis", command=self.pridaj_popis)
           
            self.vkladanie_navsteva_popis[0].grid(row=0, column=0, padx=5, pady=5, sticky="w")
            self.vkladanie_navsteva_input_okna[0].grid(row=0, column=1, padx=5, pady=5)
            self.vkladanie_navsteva_popis[1].grid(row=0, column=2, padx=5, pady=5, sticky="w")
            self.vkladanie_navsteva_input_okna[1].grid(row=0, column=3, padx=5, pady=5)
            self.vkladanie_navsteva_popis[2].grid(row=0, column=4, padx=5, pady=5, sticky="w")
            self.vkladanie_navsteva_input_okna[2].grid(row=0, column=5, padx=5, pady=5)
            self.vkladanie_navsteva_popis[3].grid(row=0, column=6, padx=5, pady=5, sticky="w")
            self.vkladanie_navsteva_input_okna[3].grid(row=0, column=7, padx=5, pady=5)

            self.vkladanie_navsteva_popis[4].grid(row=1, column=0, padx=5, pady=5, sticky="w")
            self.vkladanie_navsteva_input_okna[4].grid(row=1, column=1, columnspan=7, padx=5, pady=5, sticky="ew")
            self.pridaj_button.grid(row=1, column=8, padx=5, pady=5, sticky='w')

            
            #Listbox pre voľbu návštevy
            self.pridane_popisy_frame = tk.Frame(self.root)
            self.pridane_popisy_label = tk.Label(self.pridane_popisy_frame, text="Pridané popisy:")
            self.pridane_popisy_listbox = tk.Listbox(self.pridane_popisy_frame, height=10)

            self.pridane_popisy_frame.grid(row=3, column=0, padx=10, pady=10, sticky='ew')
            self.pridane_popisy_label.pack(side=tk.TOP, anchor="w")
            self.pridane_popisy_listbox.pack(fill=tk.BOTH, expand=True)
            self.pridane_popisy_listbox.bind('<<ListboxSelect>>', lambda event: self.volba_popisu())

            
            #Konzola pre výpis
            self.console_output_frame = tk.Frame(self.root)
            self.console_output = tk.Text(self.console_output_frame, height=15, width=80,  state='disabled')
            self.scrollbar = tk.Scrollbar(self.console_output_frame, command=self.console_output.yview)
            self.console_output.config(yscrollcommand=self.scrollbar.set)

            self.console_output_frame.grid(row=4, column=0, padx=10, pady=10, sticky='nsew')
            self.console_output.grid(row=0, column=0, sticky='nsew')
            self.scrollbar.grid(row=0, column=1, sticky='ns')
            

        elif index_operacie == 4:

            #Zvolená operácia
            self.zvolena_operacia_frame = tk.Frame(self.root)
            self.zvolena_operacia = tk.Label(self.zvolena_operacia_frame, text="Zvolená operácia: Editácia záznamu", font=("Helvetica", 16))
            self.zvolena_operacia_frame.grid(row=0, column=0, padx=10, pady=10, sticky='we')
            self.zvolena_operacia.grid(row=0, column=0, padx=10, pady=10, sticky='w')

            #Pole pre vyhľadanie zákazníka
            self.vyhladanie_input_frame = tk.Frame(self.root)
            self.vyhladanie_popis = tk.Label(self.vyhladanie_input_frame, text='Kľúč')
            self.vyhladanie_input_okno = tk.Entry(self.vyhladanie_input_frame, width=30)
            self.typ_vyhladavania_popis = tk.Label(self.vyhladanie_input_frame, text='Typ vyhľadávania')
            self.vyhladanie_typ_vyhladavania = ttk.Combobox(self.vyhladanie_input_frame, values=['Podľa ID', 'Podľa ECV'])
            self.vyhladaj_button = tk.Button(self.vyhladanie_input_frame, text="Vyhľadaj", command=self.vyhladaj_zaznam)
            self.spustit_button = tk.Button(self.vyhladanie_input_frame, text="Potvrď editáciu", command=self.spusti_operaciu)
            
            self.vyhladanie_input_frame.grid(row=1, column=0, padx=10, pady=10, sticky='w')
            self.vyhladanie_popis.grid(row=0, column=0, padx=5, pady=5, sticky="w")
            self.vyhladanie_input_okno.grid(row=0, column=1, padx=5, pady=5)
            self.typ_vyhladavania_popis.grid(row=0, column=2, padx=5, pady=5, sticky="w")
            self.vyhladanie_typ_vyhladavania.grid(row=0, column=3, padx=5, pady=5)
            self.vyhladaj_button.grid(row=0, column=4, padx=5, pady=5)
            self.spustit_button.grid(row=0, column=5, padx=5, pady=5)

            #Polia pre editáciu mena a priezviska
            self.vkladanie_input_frame = tk.Frame(self.root)
            self.vkladanie_popis = [
                tk.Label(self.vkladanie_input_frame, text='Meno'),
                tk.Label(self.vkladanie_input_frame, text='Priezvisko'),
            ]
            self.vkladanie_input_okna = [tk.Entry(self.vkladanie_input_frame, width=30) for _ in range(2)]

            self.vkladanie_input_frame.grid(row=2, column=0, padx=10, pady=10, sticky='w')
            self.vkladanie_popis[0].grid(row=0, column=0, padx=5, pady=5, sticky="w")  
            self.vkladanie_input_okna[0].grid(row=0, column=1, padx=5, pady=5)  
            self.vkladanie_popis[1].grid(row=0, column=2, padx=5, pady=5, sticky="w")  
            self.vkladanie_input_okna[1].grid(row=0, column=3, padx=5, pady=5)  
            
            #Listbox pre voľbu návštev
            self.volba_navstevy_frame = tk.Frame(self.root)
            self.volba_navstevy_listbox = tk.Listbox(self.volba_navstevy_frame, height=5)
            self.volba_navstevy_popis = tk.Label(self.volba_navstevy_frame, text="Vyberte návštevu")
            self.volba_navstevy_frame.grid(row=3, column=0, padx=10, pady=10, sticky='we')
            self.volba_navstevy_popis.pack(side=tk.TOP, anchor="w")
            self.volba_navstevy_listbox.pack(fill=tk.BOTH, expand=True)
            self.volba_navstevy_listbox.bind('<<ListboxSelect>>', lambda event: self.volba_navstevy())

            #Polia pre editáciu údajov o návštevách a ich popisoch
            self.vkladanie_navsteva_input_frame = tk.Frame(self.root)
            self.vkladanie_navsteva_input_frame.grid(row=4, column=0, padx=10, pady=10, sticky='we')

            self.vkladanie_navsteva_popis = [
                tk.Label(self.vkladanie_navsteva_input_frame, text="Deň"),
                tk.Label(self.vkladanie_navsteva_input_frame, text="Mesiac"),
                tk.Label(self.vkladanie_navsteva_input_frame, text="Rok"),
                tk.Label(self.vkladanie_navsteva_input_frame, text="Cena"),
            ]
            self.vkladanie_navsteva_input_okna = [
                tk.Entry(self.vkladanie_navsteva_input_frame, width=10),
                tk.Entry(self.vkladanie_navsteva_input_frame, width=10),
                tk.Entry(self.vkladanie_navsteva_input_frame, width=10),
                tk.Entry(self.vkladanie_navsteva_input_frame, width=10),
            ]

            self.popisy_navstev = [
                tk.Label(self.vkladanie_navsteva_input_frame, text="Popis práce 1"),
                tk.Label(self.vkladanie_navsteva_input_frame, text="Popis práce 2"),
                tk.Label(self.vkladanie_navsteva_input_frame, text="Popis práce 3"),
                tk.Label(self.vkladanie_navsteva_input_frame, text="Popis práce 4"),
                tk.Label(self.vkladanie_navsteva_input_frame, text="Popis práce 5"),
                tk.Label(self.vkladanie_navsteva_input_frame, text="Popis práce 6"),
                tk.Label(self.vkladanie_navsteva_input_frame, text="Popis práce 7"),
                tk.Label(self.vkladanie_navsteva_input_frame, text="Popis práce 8"),
                tk.Label(self.vkladanie_navsteva_input_frame, text="Popis práce 9"),
                tk.Label(self.vkladanie_navsteva_input_frame, text="Popis práce 10"),
            ]

            self.popisy_navstev_input_okna = [
                tk.Entry(self.vkladanie_navsteva_input_frame, width=40) for _ in range(10)
            ]

            self.pridaj_navstevu_button = tk.Button(self.vkladanie_navsteva_input_frame, text="Pridaj/Edituj návštevu", command=self.pridaj_edituj_navstevu)
            self.odstran_navstevu_button = tk.Button(self.vkladanie_navsteva_input_frame, text="Odstráň návštevu", command=self.odstran_navstevu)
           
            self.vkladanie_navsteva_popis[0].grid(row=0, column=0, padx=5, pady=5, sticky="w")
            self.vkladanie_navsteva_input_okna[0].grid(row=0, column=1, padx=5, pady=5)
            self.vkladanie_navsteva_popis[1].grid(row=0, column=2, padx=5, pady=5, sticky="w")
            self.vkladanie_navsteva_input_okna[1].grid(row=0, column=3, padx=5, pady=5)
            self.vkladanie_navsteva_popis[2].grid(row=0, column=4, padx=5, pady=5, sticky="w")
            self.vkladanie_navsteva_input_okna[2].grid(row=0, column=5, padx=5, pady=5)
            self.vkladanie_navsteva_popis[3].grid(row=0, column=6, padx=5, pady=5, sticky="w")
            self.vkladanie_navsteva_input_okna[3].grid(row=0, column=7, padx=5, pady=5)
            self.pridaj_navstevu_button.grid(row=0, column=8, padx=5, pady=5)
            self.odstran_navstevu_button.grid(row=0, column=9, padx=5, pady=5)

            for i in range(10):
                self.popisy_navstev[i].grid(row=i+1, column=0, padx=5, pady=5, sticky="w")
                self.popisy_navstev_input_okna[i].grid(row=i+1, column=1, columnspan=9, padx=5, pady=5, sticky="ew")

            #Konozla pre výpis
            self.console_output_frame = tk.Frame(self.root)
            self.console_output = tk.Text(self.console_output_frame, height=7, width=80,  state='disabled')
            self.scrollbar = tk.Scrollbar(self.console_output_frame, command=self.console_output.yview)
            self.console_output.config(yscrollcommand=self.scrollbar.set)

            self.console_output_frame.grid(row=5, column=0, padx=10, pady=10, sticky='nsew')
            self.console_output.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)


    

        elif index_operacie == 5:

            #Zvolená operácia
            self.zvolena_operacia_frame = tk.Frame(self.root)
            self.zvolena_operacia = tk.Label(self.zvolena_operacia_frame, text="Zvolená operácia: Generovanie dát", font=("Helvetica", 16))
            self.zvolena_operacia_frame.grid(row=0, column=0, padx=10, pady=10, sticky='w')
            self.zvolena_operacia.grid(row=0, column=0, padx=10, pady=10, sticky='w')
            
            #Vstupné pole pre generovanie záznamov
            self.generovanie_input_frame = tk.Frame(self.root)
            self.generovanie_input_okno = tk.Entry(self.generovanie_input_frame, width=20)
            self.generovanie_popis = tk.Label(self.generovanie_input_frame, text='Počet generovaných záznamov')
            self.spustit_button = tk.Button(self.generovanie_input_frame, text="Spustiť", command=self.spusti_operaciu)

            self.generovanie_input_frame.grid(row=1, column=0, padx=10, pady=10, sticky='w')
            self.generovanie_popis.grid(row=0, column=0, padx=5, pady=5, sticky="w") 
            self.generovanie_input_okno.grid(row=0, column=1, padx=5, pady=5) 
            self.spustit_button.grid(row=2, column=0, padx=10, pady=10, sticky='w')

            #Konzola pre výpis
            self.console_output_frame = tk.Frame(self.root)
            self.console_output = tk.Text(self.console_output_frame, height=10, width=80,  state='disabled')
            self.console_output_frame.grid(row=2, column=0, padx=10, pady=10, sticky='nsew')
            self.console_output.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')

            self.scrollbar = tk.Scrollbar(self.console_output_frame, command=self.console_output.yview)
            self.console_output.config(yscrollcommand=self.scrollbar.set)
            self.scrollbar.grid(row=0, column=1, sticky='ns')

            self.root.grid_rowconfigure(2, weight=1)
            self.root.grid_columnconfigure(0, weight=1)
            self.console_output_frame.grid_rowconfigure(0, weight=1)
            self.console_output_frame.grid_columnconfigure(0, weight=1)



        elif index_operacie == 6:
            
            #Zvolená operácia
            self.sekvencny_vypis_frame = tk.Frame(self.root)
            self.zvolena_operacia = tk.Label(self.sekvencny_vypis_frame, text="Zvolená operácia: Vyhľadanie záznamu", font=("Helvetica", 16))
            self.vyber_typu_suboru_combobox = ttk.Combobox(self.sekvencny_vypis_frame, values=["Heapfile", "Hashfile ID", "Hashfile ECV"], width=20)
            self.spustit_button = tk.Button(self.sekvencny_vypis_frame, text="Spustiť", command=self.spusti_operaciu)
            
            #Konzola pre sekvenčný výpis
            self.sekvencny_vypis_frame.grid(row=0, column=0, padx=10, pady=10, sticky='w')
            self.zvolena_operacia.grid(row=0, column=0, padx=10, pady=10, sticky='w')
            self.vyber_typu_suboru_combobox.grid(row=0, column=1, padx=10, pady=5, sticky='w')
            self.vyber_typu_suboru_combobox.set("Zvoľ možnosť")
            self.spustit_button.grid(row=0, column=2, padx=10, pady=10, sticky='w')

            self.console_output_sekvencny_frame.grid(row=1, column=0, columnspan=3, padx=10, pady=10, sticky='nsew')
            self.console_output_sekvencny.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')
            self.console_output_sekvencny.config(height=10)
            self.sekvencny_scrollbar = tk.Scrollbar(self.console_output_sekvencny_frame, command=self.console_output_sekvencny.yview)
            self.sekvencny_scrollbar.grid(row=0, column=1, sticky='ns')
            self.console_output_sekvencny.config(yscrollcommand=self.sekvencny_scrollbar.set)
            
            self.root.grid_rowconfigure(1, weight=1)
            self.root.grid_columnconfigure(0, weight=1)
            self.console_output_sekvencny_frame.grid_rowconfigure(0, weight=1)
            self.console_output_sekvencny_frame.grid_columnconfigure(0, weight=1)


    def skry_prvky(self):
        """
        Skryje všetky prvky GUI, ktoré by sa mohli prekrývať.
        """
        self.zvolena_operacia_frame.grid_forget()
        self.generovanie_input_frame.grid_forget()
        self.vkladanie_input_frame.grid_forget()
        self.vkladanie_navsteva_input_frame.grid_forget()
        self.vyhladanie_input_frame.grid_forget()
        self.vyhladaj_button.grid_forget()
        self.spustit_button.grid_forget()
        self.pridaj_button.grid_forget()
        self.pridane_popisy_frame.grid_forget()
        self.vyber_typu_suboru_combobox.grid_forget()
        

        self.console_output_frame.grid_forget()
        self.volba_navstevy_frame.grid_forget()

        #1
        self.root.grid_rowconfigure(2, weight=0)
        self.root.grid_columnconfigure(0, weight=0)
        self.console_output_frame.grid_rowconfigure(0, weight=0)
        self.console_output_frame.grid_columnconfigure(0, weight=0)

        #2
        self.root.grid_rowconfigure(3, weight=0)
        self.root.grid_columnconfigure(0, weight=0)
        self.console_output_frame.grid_rowconfigure(0, weight=0)
        self.console_output_frame.grid_columnconfigure(0, weight=0)

        #6
        self.sekvencny_vypis_frame.grid_forget()
        self.console_output_sekvencny_frame.grid_forget()
        self.root.grid_rowconfigure(1, weight=0)
        self.root.grid_columnconfigure(0, weight=0)

    def pridaj_popis(self):
        """
        Pridá popis práce do listboxu
        """
        popis_prace = self.vkladanie_navsteva_input_okna[4].get()

        if self.index_zvoleneho_popisu == -1:
            if self.pridane_popisy_listbox.size() >= 10:
                self.console_output.config(state='normal')
                self.console_output.insert(tk.END, "Dosiahli ste maximálny počet popisov (10). Ďalšie popisy nie je možné pridať.\n")
                self.console_output.config(state='disabled')
                self.console_output.see(tk.END)
                return

        if len(popis_prace.strip()) > 20:
            self.console_output.config(state='normal')
            self.console_output.insert(tk.END, "Popis nesmie mať viac ako 20 znakov.\n")
            self.console_output.config(state='disabled')
            self.console_output.see(tk.END)
            return

        if self.index_zvoleneho_popisu == -1:
            if popis_prace.strip():
                self.pridane_popisy_listbox.insert(tk.END, popis_prace)
                self.vkladanie_navsteva_input_okna[4].delete(0, tk.END)
        else:
            if popis_prace.strip():
                self.pridane_popisy_listbox.delete(self.index_zvoleneho_popisu)
                self.pridane_popisy_listbox.insert(self.index_zvoleneho_popisu, popis_prace)
                self.vkladanie_navsteva_input_okna[4].delete(0, tk.END)
                self.index_zvoleneho_popisu = -1

    def volba_popisu(self):
        """
        Získa index zvoleného popisu z listboxu
        """

        if self.pridane_popisy_listbox.size() == 0:
            self.console_output.config(state='normal')
            self.console_output.insert(tk.END, "Nie sú pridané žiadne popisy práce.\n")
            self.console_output.config(state='disabled')
            self.console_output.see(tk.END)
            return
        else:
            self.index_zvoleneho_popisu = self.pridane_popisy_listbox.curselection()[0]
            popis = self.pridane_popisy_listbox.get(self.index_zvoleneho_popisu)
            self.vkladanie_navsteva_input_okna[4].delete(0, tk.END)
            self.vkladanie_navsteva_input_okna[4].insert(0, popis)
            
    def pridaj_edituj_navstevu(self):
        """
        Pridá alebo edituje návštevu nájdeného záznamu
        """
        if self.volba_navstevy_listbox.size() == 0:
            self.zapis_do_konzoly("Záznam neobsahuje žiadne návštevy.\n")
            return
        else:

            kluc = self.vyhladanie_input_okno.get()
            den = self.vkladanie_navsteva_input_okna[0].get()
            mesiac = self.vkladanie_navsteva_input_okna[1].get()
            rok = self.vkladanie_navsteva_input_okna[2].get()
            cena = self.vkladanie_navsteva_input_okna[3].get()
            popisy_prace = []
            for i in range(10):
                popis = self.popisy_navstev_input_okna[i].get()
                if popis.strip():
                    popisy_prace.append(popis)
            vsetko_ok = True
            try:
                typ_vyhladavania = self.vyhladanie_typ_vyhladavania.get()
                if typ_vyhladavania == 'Podľa ID':
                    kluc = int(kluc)

                den = int(den)
                mesiac = int(mesiac)
                rok = int(rok)
                cena = float(cena)

                if den < 1 or den > 31 or mesiac < 1 or mesiac > 12 or rok < 1900 or rok > 2024:
                    raise ValueError

            except ValueError:
                vsetko_ok = False
                self.zapis_do_konzoly('Nesprávne zadané hodnoty')

            if vsetko_ok:
                datum = datetime(rok, mesiac, den)
                novy_zaznam = ZaznamONavsteve(datum, cena)
                for popis in popisy_prace:
                    novy_zaznam.pridaj_popis_prac(popis)
                self.editovane_navstevy[self.index_zvolenej_navstevy] = novy_zaznam

                self.volba_navstevy_listbox.delete(0, tk.END)
                for i in range (5):
                    if self.editovane_navstevy[i] is None:
                        self.volba_navstevy_listbox.insert(tk.END, "Voľná návšteva")
                    else:
                        self.volba_navstevy_listbox.insert(tk.END, self.editovane_navstevy[i].get_datum())

                self.zapis_do_konzoly("Návšteva bola úspešne pridaná/aktualizovaná.\n")
            
            

    def odstran_navstevu(self):
        """
        Odstráni návštevu nájdeného záznamu
        """
        if self.volba_navstevy_listbox.size() == 0:
            self.zapis_do_konzoly("Záznam neobsahuje žiadne návštevy.\n")
            return
        else:
            if self.editovane_navstevy[self.index_zvolenej_navstevy] is None:
                self.zapis_do_konzoly("Snažíte sa vymazať neexistujúci záznam.\n")
                return
            else:
                self.editovane_navstevy[self.index_zvolenej_navstevy] = None
                self.zapis_do_konzoly("Návšteva bola úspešne odstránená.\n")
                self.volba_navstevy_listbox.delete(0, tk.END)
                for i in range (5):
                        
                        if self.editovane_navstevy[i] is None:
                            self.volba_navstevy_listbox.insert(tk.END, "Voľná návšteva")
                        else:
                            self.volba_navstevy_listbox.insert(tk.END, self.editovane_navstevy[i].get_datum())


    def volba_navstevy(self):
        """
        Získa index zvolenej návštevy z listboxu
        """
        if self.najdeny_objekt is None:
            self.console_output.config(state='normal')
            self.console_output.insert(tk.END, "Nebol nájdený žiadny záznam.\n")
            self.console_output.config(state='disabled')
            self.console_output.see(tk.END)
            return
        else:
            if self.volba_navstevy_listbox.size() != 0:
                self.index_zvolenej_navstevy = self.volba_navstevy_listbox.curselection()[0]
                if self.editovane_navstevy[self.index_zvolenej_navstevy] is not None:
                    navsteva: ZaznamONavsteve = self.editovane_navstevy[self.index_zvolenej_navstevy]
                    datum_string = navsteva.get_datum()
                    den, mesiac, rok = datum_string.split('.')
                    cena = str(navsteva.get_cena())
                    self.vkladanie_navsteva_input_okna[0].delete(0, tk.END)
                    self.vkladanie_navsteva_input_okna[0].insert(0, den)
                    self.vkladanie_navsteva_input_okna[1].delete(0, tk.END)
                    self.vkladanie_navsteva_input_okna[1].insert(0, mesiac)
                    self.vkladanie_navsteva_input_okna[2].delete(0, tk.END)
                    self.vkladanie_navsteva_input_okna[2].insert(0, rok)
                    self.vkladanie_navsteva_input_okna[3].delete(0, tk.END)
                    self.vkladanie_navsteva_input_okna[3].insert(0, cena)
                    
                    popisy = navsteva.get_popis()
                    for i in range(10):
                        if i < len(popisy):
                            self.popisy_navstev_input_okna[i].delete(0, tk.END)
                            self.popisy_navstev_input_okna[i].insert(0, popisy[i])
                        else:
                            self.popisy_navstev_input_okna[i].delete(0, tk.END)
                else:

                    for i in range(4):
                        self.vkladanie_navsteva_input_okna[i].delete(0, tk.END)
                    
                    for i in range(10):
                        self.popisy_navstev_input_okna[i].delete(0, tk.END)
                
                
    def spusti_operaciu(self):
        """
        Vykoná príslušné akcie na kontrolu vstupných údajov a spustí zvolenú operáciu.
        """
        #Kontroly vstupných údajov
        vsetko_ok = True
        if self.index_zvolenej_operacie == 1:
            typ_vyhladavania = self.vyhladanie_typ_vyhladavania.get()

            if typ_vyhladavania == 'Podľa ID':
                kluc = self.vyhladanie_input_okno.get()

                if not kluc:
                    self.zapis_do_konzoly('Kľúč musí byť zadaný')
                    vsetko_ok = False

                else:
                    try:
                        kluc = int(kluc)
                    except ValueError:
                        self.zapis_do_konzoly('Nesprávne zadané hodnoty')
                        vsetko_ok = False

            elif typ_vyhladavania == 'Podľa ECV':
                kluc = self.vyhladanie_input_okno.get()

                if not kluc:
                    self.zapis_do_konzoly('Kľúč musí byť zadaný')
                    vsetko_ok = False

                elif len(kluc) > 10:
                    self.zapis_do_konzoly('Nesprávne zadané hodnoty')
                    vsetko_ok = False

            else:
                self.zapis_do_konzoly('Nebol zadaný typ vyhľadávania')
                vsetko_ok = False

        

        elif self.index_zvolenej_operacie == 2:
            meno = self.vkladanie_input_okna[0].get()
            priezvisko = self.vkladanie_input_okna[1].get()
            id = self.vkladanie_input_okna[2].get()
            ecv = self.vkladanie_input_okna[3].get()

            try:
                id = int(id)

                if len(meno) > 15 or len(priezvisko) > 20 or len(ecv) > 10:
                    raise ValueError

            except ValueError:
                self.zapis_do_konzoly('Nespravne zadané hodnoty')
                vsetko_ok = False

        elif self.index_zvolenej_operacie == 3:
            
            kluc = self.vyhladanie_input_okno.get()

            den = self.vkladanie_navsteva_input_okna[0].get()
            mesiac = self.vkladanie_navsteva_input_okna[1].get()
            rok = self.vkladanie_navsteva_input_okna[2].get()
            cena = self.vkladanie_navsteva_input_okna[3].get()
            popisy_prace = self.pridane_popisy_listbox.get(0, tk.END)
            self.pridane_popisy_listbox.delete(0, tk.END)
            popisy = list(popisy_prace)

            try:
                typ_vyhladavania = self.vyhladanie_typ_vyhladavania.get()
                if typ_vyhladavania == 'Podľa ID':
                    kluc = int(kluc)

                den = int(den)
                mesiac = int(mesiac)
                rok = int(rok)
                cena = float(cena)

                if den < 1 or den > 31 or mesiac < 1 or mesiac > 12 or rok < 1900 or rok > 2024:
                    raise ValueError

            except ValueError:
                self.zapis_do_konzoly('Nesprávne zadané hodnoty')
                vsetko_ok = False

        
        elif self.index_zvolenej_operacie == 4:
            meno = self.vkladanie_input_okna[0].get()
            priezvisko = self.vkladanie_input_okna[1].get()
        
            try:

                if len(meno) > 15 or len(priezvisko) > 20:
                    raise ValueError

            except ValueError:
                self.zapis_do_konzoly('Nespravne zadané hodnoty')
                vsetko_ok = False
        
        elif self.index_zvolenej_operacie == 5:

            pocet_generovanych_zaznamov = self.generovanie_input_okno.get()
            if not pocet_generovanych_zaznamov:
                self.zapis_do_konzoly('Počet generovaných záznamov musí byť zadaný')
                vsetko_ok = False

            try:
                pocet_generovanych_zaznamov = int(pocet_generovanych_zaznamov)
            except ValueError:
                self.zapis_do_konzoly('Nesprávne zadané hodnoty')
                vsetko_ok = False
        
        #Spustenie operácie
        if vsetko_ok:

            if self.index_zvolenej_operacie == 1:
                if typ_vyhladavania == 'Podľa ID':
                    vrateny_zakaznik = self.system.vyhladaj_vozidlo(kluc, True, self.console_output)
                else:
                    vrateny_zakaznik = self.system.vyhladaj_vozidlo(kluc, False, self.console_output)

                self.najdeny_objekt = vrateny_zakaznik
    

            elif self.index_zvolenej_operacie == 2:
                self.zapis_do_konzoly(f"Pridanie zakaznika s menom {meno}, priezviskom {priezvisko}, ID {id} a ECV {ecv}")
                self.system.pridaj_vozidlo(meno, priezvisko, id, ecv, self.console_output)
                    

            elif self.index_zvolenej_operacie == 3:
                self.system.pridaj_navstevu_servisu(kluc, rok, mesiac, den, cena, popisy, self.console_output)
                self.najdeny_objekt = None
                    
            elif self.index_zvolenej_operacie == 4:
                if self.najdeny_objekt is not None:
                    self.najdeny_objekt.set_meno(meno)
                    self.najdeny_objekt.set_priezvisko(priezvisko)
                    self.najdeny_objekt.vymaz_zaznamy_o_navsteve()
                    for i in range(5):
                        if self.editovane_navstevy[i] is not None:
                            self.najdeny_objekt.pridaj_zaznam_o_navsteve(self.editovane_navstevy[i])

                    self.system.edituj_zaznam(self.najdeny_objekt, self.console_output)

                self.najdeny_objekt = None

            elif self.index_zvolenej_operacie == 5:
                self.system.generuj_udaje(pocet_generovanych_zaznamov, self.console_output)

            elif self.index_zvolenej_operacie == 6:

                self.console_output_sekvencny.config(state='normal')
                self.console_output_sekvencny.delete('1.0', tk.END)
                self.console_output_sekvencny.config(state='disabled')

                if self.vyber_typu_suboru_combobox.get() == "Zvoľ možnosť":

                    self.console_output_sekvencny.config(state='normal')
                    self.console_output_sekvencny.insert(tk.END, "Nebol vybraný typ súboru\n")
                    self.console_output_sekvencny.config(state='disabled')

                else:

                    if self.vyber_typu_suboru_combobox.get() == "Heapfile":
                        self.system.sekvencny_vypis(1, self.console_output_sekvencny)
                    elif self.vyber_typu_suboru_combobox.get() == "Hashfile ID":
                        self.system.sekvencny_vypis(2, self.console_output_sekvencny)
                    elif self.vyber_typu_suboru_combobox.get() == "Hashfile ECV":
                        self.system.sekvencny_vypis(3, self.console_output_sekvencny)


    def vyhladaj_zaznam(self):
        """
        Vyhľadá objekt na základe vstupných údajov a aktualizuje polia pre príslušnú operáciu (napr. listbox pre výber návštev).
        """
        if self.index_zvolenej_operacie in [1,3,4]:
            povodny_index = self.index_zvolenej_operacie
            self.index_zvolenej_operacie = 1
            self.spusti_operaciu()
            self.index_zvolenej_operacie = povodny_index
            if povodny_index == 4:
                self.volba_navstevy_listbox.delete(0, tk.END)

                if self.najdeny_objekt is None:
                    self.console_output.config(state='normal')
                    self.console_output.insert(tk.END, "Nebol nájdený žiadny záznam.\n")
                    self.console_output.config(state='disabled')
                    self.console_output.see(tk.END)
                    return
                else:
                    self.vkladanie_input_okna[0].delete(0, tk.END)
                    self.vkladanie_input_okna[0].insert(0, self.najdeny_objekt.get_meno())
                    self.vkladanie_input_okna[1].delete(0, tk.END)
                    self.vkladanie_input_okna[1].insert(0, self.najdeny_objekt.get_priezvisko())

                    self.editovane_navstevy = self.najdeny_objekt.get_navstevy()
                    self.pocet_editovanych_navstev = len(self.editovane_navstevy)

                    for i in range (5):
                        if i < self.pocet_editovanych_navstev:
                            self.volba_navstevy_listbox.insert(tk.END, self.editovane_navstevy[i].get_datum())
                        else:
                            self.volba_navstevy_listbox.insert(tk.END, "Voľná návšteva")
                            self.editovane_navstevy.append(None)

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
        