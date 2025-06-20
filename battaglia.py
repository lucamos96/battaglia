from abc import ABC, abstractmethod
import random

class Soldato(ABC):
    def __init__(self, nome, costo, attacco, difesa, salute):
        self._nome = nome
        self._costo = costo
        self._attacco = attacco
        self._difesa = difesa
        self._salute = salute

    @abstractmethod
    def attacca(self, avversario, esercito_alleato):
        pass

    def difenditi(self, danno):
        danno_effettivo = max(0, danno - self._difesa)
        self._salute -= danno_effettivo

    def e_vivo(self):
        return self._salute > 0

    def stato(self):
        return f"{self.__class__.__name__} {self._nome} - Salute: {self._salute}"

    def get_costo(self):
        return self._costo

class Cavaliere(Soldato):
    def __init__(self, nome):
        super().__init__(nome, costo=300, attacco=40, difesa=30, salute=120)

    def attacca(self, avversario, esercito_alleato):
        critico = random.random() < 0.2
        danno = self._attacco * 2 if critico else self._attacco
        avversario.difenditi(danno)

class Arciere(Soldato):
    def __init__(self, nome):
        super().__init__(nome, costo=200, attacco=50, difesa=10, salute=80)

    def attacca(self, avversario, esercito_alleato):
        avversario.difenditi(self._attacco)

class Guaritore(Soldato):
    def __init__(self, nome):
        super().__init__(nome, costo=200, attacco=10, difesa=10, salute=80)

    def attacca(self, avversario, esercito_alleato):
        alleati_vivi = [s for s in esercito_alleato if s.e_vivo() and s != self]
        if alleati_vivi:
            bersaglio = random.choice(alleati_vivi)
            bersaglio._salute += 30
            print(f"{self._nome} cura {bersaglio._nome} (+30 salute)")

class Mago(Soldato):
    def __init__(self, nome):
        super().__init__(nome, costo=300, attacco=random.randint(10, 40), difesa=5, salute=90)

    def attacca(self, avversario, esercito_alleato):
        if random.random() < 0.25:
            print(f"{self._nome} è stanco e salta il turno!")
        else:
            self._attacco = random.randint(10, 40)
            avversario.difenditi(self._attacco)

def crea_soldato(nome, tipo):
    if tipo == "1":
        return Cavaliere(nome)
    elif tipo == "2":
        return Arciere(nome)
    elif tipo == "3":
        return Guaritore(nome)
    elif tipo == "4":
        return Mago(nome)
    else:
        return None

def acquista_soldati(budget):
    esercito = []
    while True:
        print(f"\nBudget attuale: {budget} monete")
        print("1. Cavaliere (300)\n2. Arciere (200)\n3. Guaritore (200)\n4. Mago (300)\n5. Fine acquisti")
        scelta = input("Scegli un tipo di soldato: ").strip()
        if scelta == "5":
            break
        if scelta not in ["1", "2", "3", "4"]:
            print("Scelta non valida. Riprova.")
            continue
        nome = input("Inserisci il nome del soldato: ").strip()
        soldato = crea_soldato(nome, scelta)
        if soldato and budget >= soldato.get_costo():
            esercito.append(soldato)
            budget -= soldato.get_costo()
        else:
            print("Fondi insufficienti. Riprova.")
    return esercito, budget

def scontro_round(esercito1, esercito2):
    print("\n-- Scontro tra eserciti --")
    for i in range(min(len(esercito1), len(esercito2))):
        s1, s2 = esercito1[i], esercito2[i]
        if not s1.e_vivo() or not s2.e_vivo():
            continue
        print(f"Scontro tra {s1._nome} e {s2._nome}")
        if isinstance(s1, Arciere):
            s1.attacca(s2, esercito1)
            if s2.e_vivo(): s2.attacca(s1, esercito2)
        elif isinstance(s2, Arciere):
            s2.attacca(s1, esercito2)
            if s1.e_vivo(): s1.attacca(s2, esercito1)
        else:
            s1.attacca(s2, esercito1)
            if s2.e_vivo(): s2.attacca(s1, esercito2)
    esercito1[:] = [s for s in esercito1 if s.e_vivo()]
    esercito2[:] = [s for s in esercito2 if s.e_vivo()]

def stampa_stato_esercito(esercito, nome):
    print(f"\n{nome} - Stato esercito:")
    for soldato in esercito:
        print(" -", soldato.stato())

def main():
    print("Benvenuto alla Battaglia dei Regni!")
    budget_giocatore = 1000
    budget_ia = 1000
    print("\nPreparazione esercito giocatore:")
    esercito_giocatore, budget_giocatore = acquista_soldati(budget_giocatore)
    esercito_ia = []
    while budget_ia >= 200:
        tipo = random.choice(["1", "2", "3", "4"])
        nome = "IA_" + str(len(esercito_ia) + 1)
        soldato = crea_soldato(nome, tipo)
        if soldato and budget_ia >= soldato.get_costo():
            esercito_ia.append(soldato)
            budget_ia -= soldato.get_costo()
    round_num = 1
    while esercito_giocatore and esercito_ia:
        print(f"\n===== ROUND {round_num} =====")
        scontro_round(esercito_giocatore, esercito_ia)
        stampa_stato_esercito(esercito_giocatore, "Giocatore")
        stampa_stato_esercito(esercito_ia, "IA")
        if not esercito_giocatore or not esercito_ia:
            break
        round_num += 1
        print("\nFine battaglia: ricevi +300 monete")
        budget_giocatore += 300
        budget_ia += 300
        print("\n--- Acquisti post battaglia ---")
        nuovi, budget_giocatore = acquista_soldati(budget_giocatore)
        esercito_giocatore.extend(nuovi)
        while budget_ia >= 200:
            tipo = random.choice(["1", "2", "3", "4"])
            nome = "IA_" + str(len(esercito_ia) + 1)
            soldato = crea_soldato(nome, tipo)
            if soldato and budget_ia >= soldato.get_costo():
                esercito_ia.append(soldato)
                budget_ia -= soldato.get_costo()
    print("\n===== FINE DELLA BATTAGLIA =====")
    if esercito_giocatore:
        print(f"Hai vinto in {round_num} battaglie con {len(esercito_giocatore)} soldati rimasti!")
    else:
        print(f"L'IA ha vinto in {round_num} battaglie con {len(esercito_ia)} soldati rimasti!")

if __name__ == "__main__":
    main()
