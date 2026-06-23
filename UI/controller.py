import flet as ft
from UI.view import View
from model.modello import Model


class Controller:
    def __init__(self, view: View, model: Model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
    def fillDDYear(self):
        years=self._model.getAllYears()
        yearsDD=list(map(lambda x: ft.dropdown.Option(x), years))
        self._view.ddyear.options=yearsDD
        self._view.update_page()

    def fillDDState(self,e):
        year=self._view.ddyear.value
        states=self._model.getAllStates(year)
        statesDD=list(map(lambda x:ft.dropdown.Option(x), states))
        self._view.ddstate.options=statesDD
        self._view.update_page()


    def handle_graph(self, e):
        year=self._view.ddyear.value
        state=self._view.ddstate.value
        self._model.buildGraph(year,state)
        n, e=self._model.getGraphDetails()
        n_componenti, largest=self._model.getInfoConnessa()
        self._view.txt_result1.controls.clear()
        self._view.txt_result1.controls.append(ft.Text(f'Numero di vertici: {n}'))
        self._view.txt_result1.controls.append(ft.Text(f'Numero di archi: {e}'))
        self._view.txt_result1.controls.append(ft.Text(f'Il grafo ha: {n_componenti} componenti connesse'))
        self._view.txt_result1.controls.append(ft.Text(f'La componente connessa più grande è costituita da {len(largest)} nodi: '))
        for c in largest:
            self._view.txt_result1.controls.append(ft.Text(c))


        self._view.update_page()

    def handle_path(self, e):
        path, score=self._model.getBestPath()
        self._view.txt_result2.controls.clear()
        self._view.txt_result2.controls.append(ft.Text(f'Il punteggio ottenuto dal cammino trovato è: {score}'))
        self._view.txt_result2.controls.append(ft.Text("Di seguito il cammino trovato: "))
        for p in path:
            self._view.txt_result2.controls.append(ft.Text(p))
        self._view.update_page()


