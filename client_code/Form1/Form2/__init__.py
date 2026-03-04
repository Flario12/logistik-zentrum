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
    self.Plot()

    
  def Plot(self):
    x_werte = [10,20,30,40]
    y_werte = [5,10,15,20]

    x_db, y_db = anvil.server.call('get_sales_from_db')

    Daten = go.Scatter(
      x = x_db,
      y = y_db,
      mode="lines+markers",
      name="Umsatz"
    )

    self.plot_1.data = [Daten]
  