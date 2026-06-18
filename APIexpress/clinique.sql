-- Schéma SQLite — Clinique du Sommeil

CREATE TABLE IF NOT EXISTS personnel (
  id_personnel INTEGER PRIMARY KEY AUTOINCREMENT,
  nom          TEXT NOT NULL,
  prenom       TEXT NOT NULL,
  date_embauche TEXT,
  telephone    TEXT,
  email        TEXT UNIQUE,
  actif        INTEGER NOT NULL DEFAULT 1
);

CREATE TABLE IF NOT EXISTS medecin (
  id_personnel INTEGER NOT NULL PRIMARY KEY,
  specialite   TEXT NOT NULL,
  numero_rpps  TEXT UNIQUE,
  FOREIGN KEY (id_personnel) REFERENCES personnel(id_personnel)
);

CREATE TABLE IF NOT EXISTS infirmier (
  id_personnel  INTEGER NOT NULL PRIMARY KEY,
  diplome       TEXT,
  experience_ans INTEGER,
  FOREIGN KEY (id_personnel) REFERENCES personnel(id_personnel)
);

CREATE TABLE IF NOT EXISTS patient (
  id_patient        INTEGER PRIMARY KEY AUTOINCREMENT,
  nom               TEXT NOT NULL,
  prenom            TEXT NOT NULL,
  date_naissance    TEXT NOT NULL,
  sexe              TEXT NOT NULL CHECK (sexe IN ('M', 'F')),
  adresse           TEXT,
  telephone         TEXT,
  email             TEXT,
  numero_secu       TEXT UNIQUE,
  imc_initial       REAL,
  fumeur            INTEGER DEFAULT 0,
  pa_tabac          INTEGER,
  consommation_alcool TEXT,
  profession        TEXT,
  niveau_activite   TEXT,
  date_creation_dpi TEXT NOT NULL DEFAULT (date('now')),
  actif             INTEGER DEFAULT 1
);

CREATE TABLE IF NOT EXISTS appareil (
  id_appareil      INTEGER PRIMARY KEY AUTOINCREMENT,
  modele           TEXT NOT NULL,
  numero_serie     TEXT UNIQUE,
  fabricant        TEXT,
  date_installation TEXT,
  statut           TEXT NOT NULL DEFAULT 'actif',
  localisation     TEXT
);

CREATE TABLE IF NOT EXISTS appareil_psg (
  id_appareil      INTEGER NOT NULL PRIMARY KEY,
  version_firmware TEXT,
  type_montage     TEXT,
  FOREIGN KEY (id_appareil) REFERENCES appareil(id_appareil)
);

CREATE TABLE IF NOT EXISTS nuit_etude (
  id_nuit          INTEGER PRIMARY KEY AUTOINCREMENT,
  id_patient       INTEGER NOT NULL,
  id_superviseur   INTEGER NOT NULL,
  id_medecin       INTEGER NOT NULL,
  id_appareil_psg  INTEGER NOT NULL,
  date_nuit        TEXT NOT NULL,
  type_etude       TEXT NOT NULL CHECK (type_etude IN ('polysomnographie', 'polygraphie', 'titration CPAP')),
  notes_techniques TEXT,
  FOREIGN KEY (id_patient)      REFERENCES patient(id_patient),
  FOREIGN KEY (id_superviseur)  REFERENCES infirmier(id_personnel),
  FOREIGN KEY (id_medecin)      REFERENCES medecin(id_personnel),
  FOREIGN KEY (id_appareil_psg) REFERENCES appareil_psg(id_appareil)
);

CREATE TABLE IF NOT EXISTS evenement_respiratoire (
  id_evenement  INTEGER PRIMARY KEY AUTOINCREMENT,
  id_nuit       INTEGER NOT NULL,
  type_evenement TEXT NOT NULL CHECK (type_evenement IN ('apnée obstructive', 'apnée centrale', 'hypopnée', 'RERA')),
  debut_sec     INTEGER NOT NULL CHECK (debut_sec >= 0),
  fin_sec       INTEGER NOT NULL CHECK (fin_sec > debut_sec),
  severite      TEXT CHECK (severite IN ('légère', 'modérée', 'sévère')),
  decibels      REAL,
  spo2_avant    REAL CHECK (spo2_avant BETWEEN 0 AND 100),
  spo2_apres    REAL CHECK (spo2_apres BETWEEN 0 AND 100),
  FOREIGN KEY (id_nuit) REFERENCES nuit_etude(id_nuit)
);

CREATE TABLE IF NOT EXISTS resultat_nuit (
  id_resultat           INTEGER PRIMARY KEY AUTOINCREMENT,
  id_nuit               INTEGER NOT NULL UNIQUE,
  id_medecin_validateur INTEGER NOT NULL,
  date_validation       TEXT NOT NULL,
  iah                   REAL,
  spo2_min              REAL,
  spo2_moy              REAL,
  spo2_mediane          REAL,
  nb_apnees             INTEGER,
  nb_hypopnees          INTEGER,
  nb_rera               INTEGER,
  nb_microeveils        INTEGER,
  duree_sommeil_min     INTEGER,
  duree_hypoxie_min     INTEGER,
  position_dominante    TEXT CHECK (position_dominante IN ('dorsale', 'latérale', 'ventrale', 'mixte')),
  duree_apnee_moy_sec   INTEGER,
  duree_apnee_max_sec   INTEGER,
  decibels_max          REAL,
  decibels_moy          REAL,
  nb_ronflements_forts  INTEGER,
  commentaire_medical   TEXT,
  FOREIGN KEY (id_nuit)               REFERENCES nuit_etude(id_nuit),
  FOREIGN KEY (id_medecin_validateur) REFERENCES medecin(id_personnel)
);

-- Données

INSERT INTO personnel (id_personnel, nom, prenom, date_embauche, telephone, email, actif) VALUES
  (1,  'Estri',    'Thomas',   '2015-09-01', '0611223344', 'thomas.estri@clinique-sommeil-arles.fr',    1),
  (2,  'Faure',    'Isabelle', '2017-03-15', '0622334455', 'isabelle.faure@clinique-sommeil-arles.fr',  1),
  (3,  'Nakamura', 'Kenji',    '2019-06-01', '0633445566', 'kenji.nakamura@clinique-sommeil-arles.fr',  1),
  (4,  'Bencherif','Samia',    '2020-01-10', '0644556677', 'samia.bencherif@clinique-sommeil-arles.fr', 1),
  (5,  'Garnier',  'Laurent',  '2016-04-01', '0655667788', 'laurent.garnier@clinique-sommeil-arles.fr', 1),
  (6,  'Moreau',   'Claire',   '2018-09-01', '0666778899', 'claire.moreau@clinique-sommeil-arles.fr',   1),
  (7,  'Dupuis',   'Marc',     '2021-02-01', '0677889900', 'marc.dupuis@clinique-sommeil-arles.fr',     1),
  (8,  'Roux',     'Nathalie', '2016-01-01', '0688990011', 'nathalie.roux@clinique-sommeil-arles.fr',   1),
  (9,  'Martin',   'Sophie',   '2017-06-01', '0699001122', 'sophie.martin@clinique-sommeil-arles.fr',   1),
  (10, 'Bernard',  'Céline',   '2018-03-01', '0611223355', 'celine.bernard@clinique-sommeil-arles.fr',  1),
  (11, 'Petit',    'Aurélie',  '2019-09-01', '0622334466', 'aurelie.petit@clinique-sommeil-arles.fr',   1),
  (12, 'Leroy',    'Marine',   '2020-04-01', '0633445577', 'marine.leroy@clinique-sommeil-arles.fr',    1),
  (13, 'Simon',    'Julie',    '2021-01-01', '0644556688', 'julie.simon@clinique-sommeil-arles.fr',     1),
  (14, 'Michel',   'Fatima',   '2022-06-01', '0655667799', 'fatima.michel@clinique-sommeil-arles.fr',   1),
  (15, 'Lefebvre', 'Amandine', '2023-01-01', '0666778800', 'amandine.lefebvre@clinique-sommeil-arles.fr', 1);

INSERT INTO medecin (id_personnel, specialite, numero_rpps) VALUES
  (1, 'Médecine du sommeil', 'RPPS10011001'),
  (2, 'Médecine du sommeil', 'RPPS10022002'),
  (3, 'Médecine du sommeil', 'RPPS10033003'),
  (4, 'Médecine du sommeil', 'RPPS10044004'),
  (5, 'Pneumologie',         'RPPS10055005'),
  (6, 'Cardiologie',         'RPPS10066006'),
  (7, 'Endocrinologie',      'RPPS10077007');

INSERT INTO infirmier (id_personnel, diplome, experience_ans) VALUES
  (8,  'IDE', 8),
  (9,  'IDE', 7),
  (10, 'IDE', 6),
  (11, 'IDE', 5),
  (12, 'IDE', 4),
  (13, 'IDE', 3),
  (14, 'IDE', 2),
  (15, 'IDE', 1);

INSERT INTO patient (id_patient, nom, prenom, date_naissance, sexe, adresse, telephone, email, numero_secu, imc_initial, fumeur, pa_tabac, consommation_alcool, profession, niveau_activite, date_creation_dpi, actif) VALUES
  (1, 'Tessier', 'Bernard',  '1968-07-15', 'M', '3 rue des Tonneliers, Arles',       '0611445588', 'bernard.tessier@gmail.com',  '1 68 07 13 058 114', 35.8, 1, 15, 'occasionnelle', 'Maçon',     'modéré', '2024-09-10', 1),
  (2, 'Vernet',  'Isabelle', '1980-03-28', 'F', '14 allée des Platanes, Tarascon',   '0622556699', 'isabelle.vernet@sfr.fr',     '2 80 03 13 142 225', 27.4, 0,  0, 'aucune',        'Comptable', 'modéré', '2024-10-05', 1);

INSERT INTO appareil (id_appareil, modele, numero_serie, fabricant, date_installation, statut, localisation) VALUES
  (1, 'Natus Embla N7000', 'SN-PSG-001', 'Natus Medical', '2018-03-01', 'actif',       'Salle PSG 1'),
  (2, 'Natus Embla N7000', 'SN-PSG-002', 'Natus Medical', '2018-03-01', 'actif',       'Salle PSG 2'),
  (3, 'Natus Embla N7000', 'SN-PSG-003', 'Natus Medical', '2019-06-15', 'actif',       'Salle PSG 3'),
  (4, 'Somnoscreen Plus',  'SN-PSG-004', 'Somnomedics',   '2020-01-10', 'actif',       'Salle PSG 4'),
  (5, 'Somnoscreen Plus',  'SN-PSG-005', 'Somnomedics',   '2020-01-10', 'maintenance', 'Salle PSG 5');

INSERT INTO appareil_psg (id_appareil, version_firmware, type_montage) VALUES
  (1, '4.2.1', 'complet'),
  (2, '4.2.1', 'complet'),
  (3, '4.2.3', 'complet'),
  (4, '3.1.0', 'ambulatoire'),
  (5, '3.1.0', 'ambulatoire');

INSERT INTO nuit_etude (id_nuit, id_patient, id_superviseur, id_medecin, id_appareil_psg, date_nuit, type_etude, notes_techniques) VALUES
  (1, 1, 8, 1, 1, '2024-10-08', 'polysomnographie', 'Installation 21h00. Patient coopérant. Endormissement 22h12. Ronflements très intenses dès onset sommeil. Réveil naturel 06h28.'),
  (2, 2, 9, 2, 4, '2024-11-05', 'polygraphie',      'Enregistrement ambulatoire posé en consultation à 17h30. Patiente rentrée à domicile. Démarrage automatique 22h00. Signal de bonne qualité.');

INSERT INTO evenement_respiratoire (id_nuit, type_evenement, debut_sec, fin_sec, severite, decibels, spo2_avant, spo2_apres) VALUES
  (1, 'apnée obstructive',  60,   125,  'sévère',  72.40, 95.20, 78.40),
  (1, 'apnée obstructive',  191,  233,  'sévère',  70.80, 95.00, 80.20),
  (1, 'apnée obstructive',  305,  338,  'sévère',  68.40, 94.80, 82.60),
  (1, 'hypopnée',           923,  983,  'modérée', 58.40, 95.40, 87.60),
  (1, 'apnée centrale',     1337, 1362, 'modérée', 42.80, 95.20, 89.40),
  (1, 'RERA',               1712, 1730, 'légère',  44.60, 95.40, 93.20),
  (2, 'hypopnée',           60,   84,   'légère',  44.20, 97.20, 91.80),
  (2, 'hypopnée',           391,  405,  'légère',  42.80, 97.40, 92.40),
  (2, 'RERA',               1224, 1238, 'légère',  38.60, 97.60, 95.40),
  (2, 'hypopnée',           1522, 1539, 'légère',  44.80, 97.20, 91.20);
