from ._anvil_designer import Form1Template
from anvil import *
import anvil.server


class Form1(Form1Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    sql = """
      SELECT f.Name, l.LID, r.Zielort, k.Name, w.Datum, f.Datum, s.Beschreibung
      FROM Fahrer f 
      INNER JOIN LKW l ON f.LID = r.LID;
    """    
    print(sql)

    anvil.server.call("query_database", sql)
    # Any code you write here will run before the form opens.
