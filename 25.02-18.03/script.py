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
        
    -- Dient nur dazu, sodass keine Duplikate bei mehrfach Ausführung enstehen.
    DELETE FROM Sendung;
    DELETE FROM Fahrt;
    DELETE FROM Wartung;
    DELETE FROM Route;
    DELETE FROM LKW;
    DELETE FROM Kunde;
    DELETE FROM Fahrer;
    
    -- FAHRER HINZUFÜGEN
    INSERT INTO Fahrer (FID, Name) VALUES 
    (1, 'Max Mustermann'),
    (2, 'Julia Schmidt'),
    (3, 'Hans Peter'),
    (4, 'Lina Meyer'),
    (5, 'Sven Svensson'),
    (6, 'Elena Rossi'),
    (7, 'Markus Weber'),
    (8, 'Sarah Berger');
    
    -- LKW HINZUFÜGEN (Verknüpft mit Stammfahrern)
    INSERT INTO LKW (LID, Traglast, Firma, FID) VALUES 
    (1, 7500, 'Mustermann GmbH', 1), 
    (2, 12000, 'Toyota', 2), 
    (3, 3500, 'Rauch', 3), 
    (4, 18000, 'Kraftwerk AG', 4),
    (5, 5000, 'Green Logistics', 5), 
    (6, 22000, 'Alpin Transport', 6),
    (7, 15000, 'Green Logistics', 7),
    (8, 9000, 'Alpin Transport', 8);
    
    -- ROUTEN HINZUFÜGEN
    INSERT INTO Route (RID, Startort, Zielort) VALUES 
    (1, 'Zürich', 'Genf'),
    (2, 'Berlin', 'Hamburg'),
    (3, 'München', 'Wien'), 
    (4, 'Basel', 'Mailand'),
    (5, 'Hong Kong', 'Stockholm'),
    (6, 'Innsbruck', 'Verona'),
    (7, 'Paris', 'Lyon'),
    (8, 'Amsterdam', 'Antwerpen'),
    (9, 'Prag', 'Dresden'),
    (10, 'Wien', 'Budapest');
    
    -- KUNDEN HINZUFÜGEN
    INSERT INTO Kunde (KID, Name) VALUES 
    (1, 'Logistik GmbH'),
    (2, 'Auto Express'),
    (3, 'Frisch & Co.'),
    (4, 'Global Trade'),
    (5, 'BioMarkt AG'),
    (6, 'Steel & Iron Ltd'),
    (7, 'Fashion Hub');
    
    -- WARTUNGEN HINZUFÜGEN
    INSERT INTO Wartung (WID, Datum, Kosten, Beschreibung, LID) VALUES 
    (1, '2024-01-15', 450, 'Ölwechsel', 1),
    (2, '2024-02-10', 1200, 'Reifentausch', 2), 
    (3, '2024-03-05', 300, 'Check UP', 3),
    (4, '2024-03-20', 2500, 'Getriebeschaden', 4),
    (5, '2024-04-10', 150, 'Service klein', 5),
    (6, '2024-05-12', 3200, 'Motorinspektion', 6),
    (7, '2024-01-20', 800, 'Bremsen erneuert', 7),
    (8, '2024-02-15', 550, 'Kühlmittel', 8);
    
    -- FAHRTEN HINZUFÜGEN (Der Kern der Logik)
    INSERT INTO Fahrt (FAID, Datum, LID, FID, RID) VALUES 
    (1, '2024-01-15', 1, 1, 1),
    (2, '2024-02-10', 2, 2, 2),
    (3, '2024-03-05', 3, 3, 3), 
    (4, '2024-03-20', 4, 4, 4),
    (5, '2024-04-01', 5, 5, 6),
    (6, '2024-04-05', 6, 6, 7),
    (7, '2024-04-10', 7, 7, 8),
    (8, '2024-04-15', 8, 8, 9),
    (9, '2024-04-20', 1, 1, 10),
    (10, '2024-05-01', 2, 2, 1),
    (11, '2024-05-10', 5, 5, 3),
    (12, '2024-05-15', 6, 6, 4);
    
    -- SENDUNGEN HINZUFÜGEN
    INSERT INTO Sendung (SID, Gewicht, Beschreibung, FAID, KID) VALUES 
    (1, 500, 'Elektronikbauteile', 1, 1),
    (2, 2000, 'Lebensmittel-Konserven', 2, 2),
    (3, 150, 'Eilbriefe', 3, 3), 
    (4, 8000, 'Maschinenteile', 4, 4),
    (5, 1200, 'Bio-Gemüse', 5, 5),
    (6, 15000, 'Stahlträger', 6, 6),
    (7, 3000, 'Textilien', 7, 7),
    (8, 50, 'Laborproben', 8, 3),
    (9, 4500, 'Möbel', 9, 1),
    (10, 2200, 'Ersatzteile Auto', 10, 2),
    (11, 950, 'Früchte-Saison', 11, 5),
    (12, 11000, 'Betonelemente', 12, 6);
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