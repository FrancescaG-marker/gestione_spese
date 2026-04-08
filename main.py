from database import (
    inizializza_database,
    aggiungi_categoria,
    aggiungi_spesa,
    salva_budget,
    report_totale_per_categoria,
    report_spese_vs_budget,
    report_elenco_spese
)

def mostra_menu():
    print("-------------------------")
    print("SISTEMA SPESE PERSONALI")
    print("-------------------------")
    print("1. Gestione Categorie")
    print("2. Inserisci Spesa")
    print("3. Definisci Budget")
    print("4. Visualizza Report")
    print("5. Esci")
    print("-------------------------")

def mostra_menu_report():
    print("\n----- MENU REPORT -----")
    print("1. Totale spese per categoria")
    print("2. Spese mensili vs budget")
    print("3. Elenco completo delle spese ordinate per data")
    print("4. Ritorna al menu principale")
    print("-----------------------")

def main():
    inizializza_database()
    print("Benvenuto nel sistema di gestione spese personali!")

    while True:
        mostra_menu()
        scelta = input("Inserisci la tua scelta: ")

        if scelta == "1":
            nome = input("Inserisci il nome della categoria: ")
            print(aggiungi_categoria(nome))

        elif scelta == "2":
            data = input("Inserisci la data (YYYY-MM-DD): ")
            importo = float(input("Inserisci l'importo: "))
            categoria = input("Inserisci la categoria: ")
            descrizione = input("Inserisci la descrizione: ")

            print(aggiungi_spesa(data, importo, categoria, descrizione))

        elif scelta == "3":
            mese = input("Inserisci il mese (YYYY-MM): ")
            categoria = input("Inserisci la categoria: ")
            budget = float(input("Inserisci il budget: "))

            print(salva_budget(mese, categoria, budget))

        elif scelta == "4":
            while True:
                mostra_menu_report()
                scelta_report = input("Scegli un report: ")

                if scelta_report == "1":
                    risultati = report_totale_per_categoria()
                    print("\nCategoria..........Totale Speso")
                    for c, t in risultati:
                        print(f"{c:<18}{t:.2f}")

                elif scelta_report == "2":
                    mese = input("Inserisci il mese (YYYY-MM): ")
                    risultati = report_spese_vs_budget(mese)

                    print(f"\nMese: {mese}")

                    for c, b, s in risultati:
                        if b == 0:
                            stato = "NESSUN BUDGET"
                        elif s > b:
                            stato = "SUPERAMENTO BUDGET"
                        else:
                            stato = "OK"

                        print(f"\nCategoria: {c}")
                        print(f"Budget: {b:.2f}")
                        print(f"Speso: {s:.2f}")
                        print(f"Stato: {stato}")

                elif scelta_report == "3":
                    risultati = report_elenco_spese()

                    print("\nData        Categoria         Importo   Descrizione")
                    print("---------------------------------------------------")

                    for d, c, i, desc in risultati:
                        print(f"{d:<12}{c:<18}{i:<10.2f}{desc}")

                elif scelta_report == "4":
                    break

                else:
                    print("Scelta non valida.")

        elif scelta == "5":
            print("Uscita...")
            break

        else:
            print("Scelta non valida.")

main()