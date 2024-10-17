# Uppgiftshanterare (ToDo-lista)
# En kommandoradsbaserad uppgiftshanterare där användaren kan lägga
# till, ta bort och markera uppgifter som klara, samt visa alla kvarstående
# uppgifter. Uppgifterna sparas så att de finns kvar nästa gång programmet körs.

from rich.console import Console    # importerar rich-klassen för att kunna visa färger i terminalen
console = Console()

# Skapar motiverande text som skrivs ut en gång när programmet körs.
motiverande_text = ["Börja med det svåraste som känns överkomligt först.", 
                    "Det kommer kännas bättre att börja utföra uppgiften, än att inte börja alls.",
                    "Fokusera på att göra det allra första steget av uppgiften.",
                    "Dela upp uppgiften i hanterbara delar.",
                    "Gör en genomtänkt plan.",
                    "Unna dig något efter varje uppgift eller delmål.",
                    "Att skriva ner uppgifter friar upp och lugnar sinnet.",
                    "Ta ett par djupa andetag innan du börjar."
                    "Det svåraste är oftast att börja."]
import random
# Generera en slumpmässig text från listan med motiverande text
slumptext = motiverande_text[random.randint(0, len(motiverande_text)-1)]    # slumpmässig text mellan första och sista indexet
console.print(f"\n{slumptext}", style="orange3")


class Uppgift:
    def __init__(self, title):
        self.title = title
        self.markerad = False   # Uppgiften är från början avmarkerad

    def markera(self):      # Metod som sätter attributet 'markerad' som True
        self.markerad = True

import pickle       # Importerar pickle-modulen för att läsa uppgifter till och från en fil.

class ToDo:
    def __init__(self):
        self.uppgifter = []

    def lägg_till_uppgift(self, namn):      # Metod som lägger till en uppgift till ToDo-listan.
        for uppgift in self.uppgifter:      # Kolla om uppgiften redan finns
            if uppgift.title == namn:
                raise ValueError(f"Uppgiften '{namn}' finns redan i listan.")   # kastar ett ValueError med ett meddelande om uppgiften redan finns
        self.uppgifter.append(Uppgift(namn))

    def ta_bort_uppgift(self, namn):        # Metod som tar bort en uppgift från ToDo-listan.
        # Använder funktionen 'any' för att kolla om uppgiften finns
        if not any(uppgift.title == namn for uppgift in self.uppgifter):    # Kolla om uppgiften finns innan vi tar bort den
            raise ValueError(f"Uppgiften '{namn}' finns inte i listan.")    # kastar ett ValueError om uppgiften inte finns
        
        # Använder en list comprehension för att skapa en ny lista utan den angivna uppgiften
        self.uppgifter = [uppgift for uppgift in self.uppgifter if uppgift.title != namn]

    def markera(self, namn):        # Metod som markerar en uppgift som klar.
        for uppgift in self.uppgifter:
            if uppgift.title == namn:
                uppgift.markera()   # Använder Uppgift-klassens markera-metod för att sätta attributet till 'True' för angivna uppgiften
                console.print(f"Uppgiften '{namn}' har klarmarkerats. Bra jobbat!", style="bright_green")
                return
        console.print(f"Uppgiften '{namn}' finns inte i listan.", style="grey37")

    def visa_uppgifter(self):       # Metod som visar eventuella uppgifter i listan, och om de är klarmarkerade eller inte.
        if not self.uppgifter:
            console.print("Du har just nu inga uppgifter tillagda.", style="grey37")
        else:
            print("\nUppgifter i listan:")
            for uppgift in self.uppgifter:
                status = "✔" if uppgift.markerad else ""   # Status tilldelas en bockmarkering om uppgiftens markerad-attribut är 'True'
                print(f"{uppgift.title} {status}")      # En bockmarkering skrivs ut bredvid den klarmarkerade uppgiften

    def spara_uppgifter(self, filnamn):     # Metod för att spara uppgifterna till en fil
        with open(filnamn, 'wb') as fil:    # 'with' för säker hantering. Binärläge eftersom en textfil i sig inte ska användas.
            pickle.dump(self.uppgifter, fil)

    def ladda_uppgifter(self, filnamn):     # Metod för att ladda och öppna dem sparade uppgifterna.
        try:
            with open(filnamn, 'rb') as fil:        # Öppnar filen i läsläge
                self.uppgifter = pickle.load(fil)
        except FileNotFoundError:                   # Om filen inte finns, fångas detta och skapar en ny lista av uppgifter.
            print("Ingen sparad uppgiftslista hittades. En ny lista har skapats.")


# Instansierar ToDo-klassen
todo = ToDo()
todo.ladda_uppgifter('uppgifter.pk1')  # Laddar uppgifter vid start

# Interaktiv meny
while True:
    console.print("\nVad vill du göra?", style="cyan")
    console.print("1. Visa nuvarande uppgifter", style="cyan")
    console.print("2. Lägg till uppgift", style="cyan")
    console.print("3. Ta bort uppgift", style="cyan")
    console.print("4. Markera uppgift som klar", style="cyan")
    console.print("5. Spara uppgifter", style="cyan")
    console.print("6. Ta bort alla uppgifter", style="cyan")
    console.print("7. Spara och Avsluta", style="cyan")

    val = input("Välj ett alternativ (1-7): ")

    if val == "1":
        todo.visa_uppgifter()       # Använder 'visa_uppgifter'-metoden för att visa alla uppgifter i ToDo-listan
    
    elif val == "2":
        namn = input("Ange uppgift att lägga till: ")
        try:
            todo.lägg_till_uppgift(namn)        # Använder metoden som lägger till en angiven uppgift till ToDo-listan
            console.print(f"Uppgiften '{namn}' har lagts till i listan.", style="bright_blue")
        except ValueError as e:     # Fångar undantaget från metoden 'lägg_till_uppgift'
            print(e)                # Skriver ut undantaget.
    
    elif val == "3":
        namn = input("Ange uppgift att ta bort: ")
        try:
            todo.ta_bort_uppgift(namn)
            console.print(f"Uppgiften '{namn}' har tagits bort från listan.", style="grey37")
        except ValueError as e:     # Fångar undantaget från metoden 'ta_bort_uppgift'
            print(e)                # Skriver ut undantaget.
    
    elif val == "4":
        if len(todo.uppgifter) == 0:        # Om ToDo-listans längd är 0, d.v.s. inte har några uppgifter.
            console.print("Det finns inga uppgifter i listan att klarmarkera.", style="bright_red")
        else:
            todo.visa_uppgifter()
            uppgift = input("Vilken uppgift vill du markera som klar? ")
            todo.markera(uppgift)           # Markerar den angivna uppgiften med hjälp av 'markera'-metoden.

    elif val == "5":
        from rich.progress import track     # Importerar 'track'-funktionen från 'rich'
        import time                         # Importerar 'time'-modulen
        for step in track(range(10), description="Sparar..."):      # Skapar en progress bar med rich för visuell effekt.
            time.sleep(0.05)
        todo.spara_uppgifter('uppgifter.pk1')       # Sparar ToDo-listan med dess uppgifter.
        console.print("Uppgifterna har sparats.", style="grey37")

    elif val == "6":
        bekrafta = input("Bekräfta genom att skriva 'ja': ")    # Ber användaren bekräfta valet om att ta bort alla uppgifter
        if bekrafta == "ja":
            if not todo.uppgifter:      # Kollar först om det finns uppgifter i listan.
                console.print("\nDet finns inga uppgifter att ta bort.", style="bright_red")
            else:
                for uppgift in todo.uppgifter[:]:  # Skapar en kopia av listan att iterera över.
                    todo.ta_bort_uppgift(uppgift.title)     # Tar bort varje uppgift i ursprungslistan.
                console.print("\nAlla uppgifter har tagits bort.", style="grey37")
        else:
            continue        # Om annat input än "ja" ges, kommer användaren tillbaka till menyn.
        
    elif val == "7":
        from rich.progress import track
        import time
        for step in track(range(10), description="Sparar..."):      # Skapar en prograss bar även här eftersom vi sparar.
            time.sleep(0.05)
        todo.spara_uppgifter('uppgifter.pk1')  # Spara innan avslut.
        console.print("Avslutar programmet.", style="grey37")
        break

    else:
        console.print("\nOgiltigt val. Försök igen.", style="bright_red")       # Om inget av valen 1-7 matades in.
