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
        f.Name AS Name,
        fa.Datum AS Datum,
        r.Zielort AS Zielort,
        r.Startort AS Startort,
        l.Firma AS Firma
      FROM Fahrer f 
      LEFT JOIN Fahrt fa ON f.FID = fa.FID
      LEFT JOIN Route r ON fa.RID = r.RID
      LEFT JOIN LKW l ON f.FID = l.FID
      ;
    """ 
    
    print(sql)
    
    return_value = anvil.server.call("query_database_dict", sql)
    
    # Die Liste dem RepeatingPanel übergeben
    self.repeating_panel_1.items = return_value
    self.drop_down_1()
    # Any code you write here will run before the form opens.

  @handle("overview", "click")
  def overview_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('Form1.Form2')
    pass

  @handle("drop_down_1", "change")
  def drop_down_change(self):
    sql = """
      SELECT 
        f.Name AS Name,
        fa.Datum AS Datum,
        r.Zielort AS Zielort,
        r.Startort AS Startort,
        l.Firma AS Firma
      FROM Fahrer f 
      LEFT JOIN Fahrt fa ON f.FID = fa.FID
      LEFT JOIN Route r ON fa.RID = r.RID
      LEFT JOIN LKW l ON f.FID = l.FID
      ;
    """ 
    
    return_value = anvil.server.call("query_database_dict", sql)
    for d in return_value:
      # d["gebaeude_name"] = self.drop_down_gefaengnisliste.selected_value
      d["Firma"] = self.drop_down_1.selected_value
    print(return_value)
    self.repeating_panel_1.items = return_value
    pass
    