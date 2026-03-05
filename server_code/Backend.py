import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.files
from anvil.files import data_files
import anvil.server
import sqlite3
# This is a server module. It runs on the Anvil server,
# rather than in the user's browser.
#
# To allow anvil.server.call() to call functions here, we mark
# them with @anvil.server.callable.
# Here is an example - you can replace it with your own:
#
# @anvil.server.callable
# def say_hello(name):
#   print("Hello, " + name + "!")
#   return 42
#

@anvil.server.callable
def query_database(query: str):
  with sqlite3.connect(data_files["logistik_zentrum.db"]) as conn: # Alternative für eine Variabelsetzung
    cur = conn.cursor()
    result = cur.execute(query).fetchall()
  return result


@anvil.server.callable
def query_database_dict(query: str):
  with sqlite3.connect(data_files["logistik_zentrum.db"]) as conn: 
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    result = cur.execute(query).fetchall()
  return [dict(row) for row in result]

@anvil.server.callable
def get_sales_from_db():
  with sqlite3.connect(data_files["logistik_zentrum.db"]) as conn:
    cur = conn.cursor()

    query = """
    SELECT
      w.Datum, w.Kosten, l.Firma
    FROM
      Wartung w
    LEFT JOIN 
      LKW l
    ON 
      l.LID = w.LID
    ORDER BY 
      Datum ASC
    """

    results = cur.execute(query).fetchall()
    datum_liste = [row[0] for row in results]
    kosten_liste = [row[1] for row in results]
    return datum_liste, kosten_liste