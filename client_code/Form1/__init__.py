from ._anvil_designer import Form1Template
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server


class Form1(Form1Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    
    sql = """
      SELECT 
        f.Name,
        r.Zielort
      FROM Fahrer f 
      INNER JOIN Route r ON f.FID = r.RID;
    """    
    print(sql)
    
    return_value = anvil.server.call("query_database_dict", sql)
    return_value
    self.repeating_panel_1.items = return_value
    print(return_value)
    # Any code you write here will run before the form opens.
    