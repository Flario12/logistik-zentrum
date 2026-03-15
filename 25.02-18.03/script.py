import sqlite3

# Name der Datenbank-Datei, die erstellt wird
DB_FILE = "logistik_zentrum.db"


def create_tables():
    # Verbindung zur Datenbank herstellen
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # SQL-Befehle zum Erstellen der Tabellen
    sql_script = '''
    -- Tabelle Fahrer
    CREATE TABLE IF NOT EXISTS Fahrer (
        FID INTEGER PRIMARY KEY AUTOINCREMENT,
        Name TEXT NOT NULL
    );

    -- Tabelle LKW (Stammfahrer-Prinzip)
    CREATE TABLE IF NOT EXISTS LKW (
        LID INTEGER PRIMARY KEY AUTOINCREMENT,
        Traglast INTEGER,
        FIRMA TEXT,
        FID INTEGER,
        FOREIGN KEY (FID) REFERENCES Fahrer(FID)
    );

    -- Tabelle Route
    CREATE TABLE IF NOT EXISTS Route (
        RID INTEGER PRIMARY KEY AUTOINCREMENT,
        Startort TEXT,
        Zielort TEXT
    );

    -- Tabelle Kunde
    CREATE TABLE IF NOT EXISTS Kunde (
        KID INTEGER PRIMARY KEY AUTOINCREMENT,
        Name TEXT NOT NULL
    );

    -- Tabelle Wartung (Zugeordnet zu einem LKW)
    CREATE TABLE IF NOT EXISTS Wartung (
        WID INTEGER PRIMARY KEY AUTOINCREMENT,
        Datum DATE,
        Kosten INTEGER,
        Beschreibung TEXT,
        LID INTEGER,
        FOREIGN KEY (LID) REFERENCES LKW(LID)
    );

    -- Tabelle Fahrt (Zentrale Verbindung von LKW, Fahrer und Route)
    CREATE TABLE IF NOT EXISTS Fahrt (
        FAID INTEGER PRIMARY KEY AUTOINCREMENT,
        Datum DATE,
        LID INTEGER,
        FID INTEGER,
        RID INTEGER,
        FOREIGN KEY (LID) REFERENCES LKW(LID),
        FOREIGN KEY (FID) REFERENCES Fahrer(FID),
        FOREIGN KEY (RID) REFERENCES Route(RID)
    );

    -- Tabelle Sendung (Zugeordnet zu einer Fahrt und einem Kunden)
    CREATE TABLE IF NOT EXISTS Sendung (
        SID INTEGER PRIMARY KEY AUTOINCREMENT,
        Gewicht INTEGER,
        Beschreibung TEXT,
        FAID INTEGER,
        KID INTEGER,
        FOREIGN KEY (FAID) REFERENCES Fahrt(FAID),
        FOREIGN KEY (KID) REFERENCES Kunde(KID)
    );


    -- Fahrer hinzufügen
    INSERT INTO Fahrer (Name) \
    VALUES  ('Max Mustermann'), \
            ('Julia Schmidt'), \
            ('Hans Peter'), \
            ('Lina Meyer');

    -- LKW hinzufügen (verknüpft mit Stammfahrern FID 1-4)
    INSERT INTO LKW (Traglast, Firma, FID) \
    VALUES (7500, "Mustermann GmbH", 1), \
            (12000, "Toyota", 2), \
            (3500, "Rauch", 3), \
            (18000, "Kraftwerk AG", 4);

    -- Routen hinzufügen
    INSERT INTO Route (Startort, Zielort) \
    VALUES ('Zürich', 'Genf'), \
            ('Berlin', 'Hamburg'), \
            ('München', 'Wien'), \
            ('Basel', 'Mailand'), \
            ('Hong Kong', 'Stockholm');

    -- Kunden hinzufügen
    INSERT INTO Kunde (Name) \
    VALUES ('Logistik GmbH'), \
            ('Auto Express'), \
            ('Frisch & Co.'), \
            ('Global Trade');

    -- Wartung hinzufügen (verknüpft mit LKW LID 1-4)
    INSERT INTO Wartung (Datum, Kosten, Beschreibung, LID) \
    VALUES ('2024-01-15', 450, 'Ölwechsel', 1), \
            ('2024-02-10', 1200, 'Reifentausch', 2), \
            ('2024-03-05', 300, 'Lichtmaschine geprüft', 3), \
            ('2024-03-20', 2500, 'Getriebeschaden repariert', 4), \
            ('2024-02-25', 700, 'Kohle Lieferung', 4), \
            ('2024-02-25', 800, 'Gewürze Lieferung', 4), \
            ('2024-3-21', 1200, 'Reifentausch', 2);

    -- Fahrten hinzufügen (Verknüpfung von Datum, LKW, Fahrer und Route)
    -- Hier nutzen wir die IDs 1 bis 4 für LKW, Fahrer und Route
    INSERT INTO Fahrt (Datum, LID, FID, RID) \
    VALUES ('2024-01-15', 1, 1, 1), \
            ('2024-02-10', 2, 2, 2), \
            ('2024-03-05', 3, 4, 3), \
            ('2024-03-20', 4, 4, 4), \
            ('2024-02-25', 1, 4, 2), \
            ('2024-02-25', 2, 4, 5), \
            ('2024-03-21', 2, 3, 4);

    -- Sendungen hinzufügen (Verknüpfung zu Fahrt und Kunde)
    INSERT INTO Sendung (Gewicht, Beschreibung, FAID, KID) \
    VALUES (500, 'Elektronikbauteile', 1, 1), \
            (2000, 'Lebensmittel-Konserven', 2, 2), \
            (150, 'Dokumente/Eilgut', 3, 3), \
            (8000, 'Maschinenteile', 4, 4), \
            (1000, 'Gewürze', 5, 4);
    '''


    try:
        cursor.executescript(sql_script)
        conn.commit()
        print(f"Erfolg: Die Datei '{DB_FILE}' wurde mit allen Tabellen erstellt.")
    except sqlite3.Error as e:
        print(f"Fehler beim Erstellen der Tabellen: {e}")
    finally:
        conn.close()


if __name__ == "__main__":
    create_tables()