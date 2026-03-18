from ._anvil_designer import Form3Template
from anvil import *
import plotly.graph_objects as go
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class Form3(Form3Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.BarCostEndPlot()
    self.BarWeightEndPlot()
    self.BarCostStartPlot()
    # Any code you write here will run before the form opens.


  def BarCostEndPlot(self):
    #selected_company = self.drop_down_1.selected_value

    x_db, y_db = anvil.server.call("get_costs_objectiveplaces_from_db")

    Daten = go.Bar(
      x = x_db,
      y = y_db,
      name = "Balkendiagramm"
    )

    self.plot_1.data = [Daten]

  def BarWeightEndPlot(self):
    #selected_company = self.drop_down_1.selected_value

    x_db, y_db = anvil.server.call("get_weights_places_from_db")

    Daten = go.Bar(
      x = x_db,
      y = y_db,
      name = "Balkendiagramm"
    )

    self.plot_2.data = [Daten]

  def BarCostStartPlot(self):
    #selected_company = self.drop_down_1.selected_value

    x_db, y_db = anvil.server.call("get_costs_startplaces_from_db")

    Daten = go.Bar(
      x = x_db,
      y = y_db,
      name = "Balkendiagramm"
    )

    self.plot_3.data = [Daten]
    
  @handle("button_1", "click")
  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form("Form1")
    pass

 