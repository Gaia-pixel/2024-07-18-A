import flet as ft
from UI.view import View
from model.modello import Model


class Controller:
    def __init__(self, view: View, model: Model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model


    def fillDD(self):
        ch = self._model.get_cromosomi()
        for c in ch:
            self._view.dd_min_ch.options.append(ft.dropdown.Option(c))
            self._view.dd_max_ch.options.append(ft.dropdown.Option(c))
        self._view.update_page()

    def handle_graph(self, e):
        self._view.txt_result1.controls.clear()
        self.cMin = int(self._view.dd_min_ch.value)
        self.cMax = int(self._view.dd_max_ch.value)
        if self.cMin is None or self.cMax is None:
            self._view.txt_result1.controls.append(ft.Text("Selezionare sia cMin che cMax"))
            self._view.update_page()
            return
        if self.cMin > self.cMax:
            self._view.txt_result1.controls.append(ft.Text("cMin deve essere <= di cMax"))
            self._view.update_page()
            return

        self._model.buildGraph(self.cMin, self.cMax)
        n, a = self._model.getGraphDetails()
        self._view.txt_result1.controls.append(ft.Text(f"grafo creato con {n} nodi e {a} archi"))
        nodiMaxConNum = self._model.getNodiMaxConNum()
        for nodo, num, peso in nodiMaxConNum:
            self._view.txt_result1.controls.append(ft.Text(f"{nodo} | num archi uscenti: {num} | peso tot: {peso}"))
        self._view.update_page()

    def handle_dettagli(self, e):
        cammino, pesoTot = self._model.getMaxCammino()
        self._view.txt_result2.controls.append(ft.Text(f"Cammino massimo trovato con {len(cammino)} nodi e peso {pesoTot}, di seguito i nodi:"))
        for n in cammino:
            self._view.txt_result2.controls.append(ft.Text(n))
        self._view.update_page()


    def handle_path(self, e):
        pass