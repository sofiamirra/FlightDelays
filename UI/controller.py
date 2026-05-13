import flet as ft

class Controller:
    def __init__(self, view, model):
        self._view = view # riferimento alla UI
        self._model = model # riferimento alla logica
        self._choicePartenza = None
        self._choiceArrivo = None

    def handleAnalizza(self, e):
        """Gestisce il click su Analizza Aeroporti"""
        # 1. Lettura e validazione dell'input
        cMinTxt = self._view._txtInCMin.value
        try:
            cMin = int(cMinTxt)
        except ValueError:
            self._view._txtResults.controls.clear()
            self._view._txtResults.controls.append(ft.Text("Inserire un valore numerico per numero minimo compagnia!"))
            self._view.update_page()
            return

        if cMin <= 0:
            self._view._txtResults.controls.clear()
            self._view._txtResults.controls.append(
                ft.Text("Il filtro sul numero di compagnie deve essere un intero positivo!"))
            self._view.update_page()
            return

        # Esecuzione Logica
        self._model.buildGraph(cMin)

        # Recupero Risultati e Aggiornamento UI
        nNodes, nEdges = self._model.getGraphDetails()
        self._view._txtResults.controls.clear()
        self._view._txtResults.controls.append(
            ft.Text("Grafo correttamente creato:", color="green"))
        self._view._txtResults.controls.append(
            ft.Text(f"Il grafo contiene {nNodes} nodi e {nEdges} archi."))

        # Popolamento DropDown
        allNodes = self._model.getAllNodes()
        self._fillDropdown(allNodes)
        self._view.update_page()

    def handleConnessi(self, e):
        pass

    def handleCerca(self, e):
        pass

    def _fillDropdown(self, allNodes):
        """Per ciascun Aeroporto (nodo) si crea un'opzione del menù a tendina"""
        for node in allNodes:
            self._view._ddAeroportoP.options.append(ft.dropdown.Option(data=node,
                                                                       key= node.IATA_CODE,
                                                                       on_click=self._choiceDdPartenza))

            self._view._ddAeroportoA.options.append(ft.dropdown.Option(data=node,
                                                                       key=node.IATA_CODE,
                                                                       on_click=self._choiceDdArrivo))

    def _choiceDdPartenza(self, e):
        """Il Controller estrae l'oggetto Airport e lo salva nella variabile"""
        self._choicePartenza = e.control.data
        print(self._choicePartenza)

    def _choiceDdArrivo(self, e):
        self._choiceArrivo = e.control.data
        print(self._choiceArrivo)