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
def get_sales_from_db(selected_Company):
  with sqlite3.connect(data_files["logistik_zentrum.db"]) as conn:
    cur = conn.cursor()
    
    query = f"""
      SELECT
        w.Datum, w.Kosten, l.Firma
      FROM
        Wartung w
      LEFT JOIN 
        LKW l
      ON 
        l.LID = w.LID
      WHERE
        ? = 'Alle' OR l.Firma = ?
      ORDER BY 
        Datum ASC
    """

    results = cur.execute(query, (selected_Company,selected_Company)).fetchall()
    datum_liste = [row[0] for row in results]
    kosten_liste = [row[1] for row in results]
    return datum_liste, kosten_liste


@anvil.server.callable
def get_costs_objectiveplaces_from_db():
  with sqlite3.connect(data_files["logistik_zentrum.db"]) as conn:
    cur = conn.cursor()

    query = """
      SELECT
         r.Zielort, w.Kosten
      From Fahrt f
      JOIN Wartung w ON f.LID = w.LID
      JOIN Sendung s ON f.FAID = s.FAID
      JOIN Route r ON f.RID = r.RID
      ORDER BY w.Kosten ASC
    """

    results = cur.execute(query).fetchall()
    Ziel_liste = [row[0] for row in results]
    Kosten_liste = [row[1] for row in results]
    return Ziel_liste, Kosten_liste

@anvil.server.callable
def get_costs_startplaces_from_db():
  with sqlite3.connect(data_files["logistik_zentrum.db"]) as conn:
    cur = conn.cursor()

    query = """
      SELECT
         r.Startort, w.Kosten
      From Fahrt f
      JOIN Wartung w ON f.LID = w.LID
      JOIN Sendung s ON f.FAID = s.FAID
      JOIN Route r ON f.RID = r.RID
      ORDER BY w.Kosten ASC
    """

    results = cur.execute(query).fetchall()
    Start_liste = [row[0] for row in results]
    Kosten_liste = [row[1] for row in results]
    return Start_liste, Kosten_liste


@anvil.server.callable
def get_weights_places_from_db():
  with sqlite3.connect(data_files["logistik_zentrum.db"]) as conn:
    cur = conn.cursor()

    query = """
      SELECT
        r.Zielort, s.Gewicht
      From Fahrt f
      JOIN Wartung w ON f.LID = w.LID
      JOIN Sendung s ON f.FAID = s.FAID
      JOIN Route r ON f.RID = r.RID
      ORDER BY s.Gewicht ASC
    """

    results = cur.execute(query).fetchall()
    Ziel_liste = [row[0] for row in results]
    Gewicht_liste = [row[1] for row in results]
    return Ziel_liste, Gewicht_liste