import flet as ft

class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._choicePartenza = None
        self._choiceArrivo = None

    def handleAnalizza(self, e):
        cMinTxt = self._view._txtInCMin.value
        if cMinTxt == "":
            self._view._txtResults.controls.clear()
            self._view._txtResults.controls.append(ft.Text("Inserire un valore numerico per numero minimo compagnia!"))
            self._view.update_page()
            return

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

        self._model.buildGraph(cMin)
        nNodes, nEdges = self._model.getGraphDetails()
        allNodes = self._model.getAllNodes()
        self._fillDropdown(allNodes)

        self._view._txtResults.controls.clear()
        self._view._txtResults.controls.append(
            ft.Text("Grafo correttamente creato:", color="green"))
        self._view._txtResults.controls.append(
            ft.Text(f"Il grafo contiene {nNodes} nodi e {nEdges} archi."))
        self._view.update_page()



    def handleConnessi(self, e):
        pass

    def handleCerca(self, e):
        pass

    def _fillDropdown(self, allNodes):
        """Cicliamo su ogni nodo ed aggiugniamo le opzioni nel menù a tendina"""
        for node in allNodes:
            self._view._ddAeroportoP.options.append(ft.dropdown.Option(data=node,
                                                                       key= node.IATA_CODE,
                                                                       on_click=self._choiceDdPartenza))

            self._view._ddAeroportoA.options.append(ft.dropdown.Option(data=node,
                                                                       key=node.IATA_CODE,
                                                                       on_click=self._choiceDdArrivo))

    def _choiceDdPartenza(self, e):
        self._choicePartenza = e.control.data
        print(self._choicePartenza)

    def _choiceDdArrivo(self, e):
        self._choiceArrivo = e.control.data
        print(self._choiceArrivo)