from ._anvil_designer import Form2Template
from anvil import *
import plotly.graph_objects as go
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class Form2(Form2Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    
    # Any code you write here will run before the form opens.
    self.PlotScatter()
    self.HistoPlot()
    self.drop_down_1_change()

    # Hier sollte man noch es ermöglichen, dass der Plot 

    
  def PlotScatter(self):
    selected_company = self.drop_down_1.selected_value
    #x_werte = [10,20,30,40]
    #y_werte = [5,10,15,20]

    x_db, y_db = anvil.server.call('get_sales_from_db', selected_Company = selected_company)

    Daten = go.Scatter(
      x = x_db,
      y = y_db,
      mode="lines+markers",
      name="Umsatz"
    )

    self.plot_1.data = [Daten]

  def HistoPlot(self):
    selected_company = self.drop_down_1.selected_value
  
    x_db, y_db = anvil.server.call("get_sales_from_db", selected_Company = selected_company)
    
    Daten = go.Histogram(
      x = y_db,
      nbinsx = 20,
      name = "histogramm"
    )

    self.plot_2.data = [Daten]
  
  @handle("drop_down_1", "change")
  def drop_down_1_change(self, **event_args):
    """This method is called when an item is selected"""
    self.PlotScatter()
    self.HistoPlot()


