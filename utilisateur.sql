USE clinique2nuitsv2;

CREATE TABLE `utilisateur` (
    `id_utilisateur` INT          NOT NULL AUTO_INCREMENT,
    `id_personnel`   INT          DEFAULT NULL,
    `login`          VARCHAR(50)  NOT NULL UNIQUE,
    `mot_de_passe`   VARCHAR(255) NOT NULL,
    `role`           ENUM('admin','medecin','infirmier','etl','reporting') NOT NULL,
    `actif`          TINYINT(1)   NOT NULL DEFAULT 1,
    PRIMARY KEY (`id_utilisateur`),
    CONSTRAINT `fk_utilisateur_personnel`
        FOREIGN KEY (`id_personnel`) REFERENCES `personnel`(`id_personnel`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

INSERT INTO `utilisateur` (`id_personnel`, `login`, `mot_de_passe`, `role`) VALUES
    (NULL, 'admin',       'Admin@1234',   'admin'),
    (1,    't.estri',     'Mdp@1234',     'medecin'),
    (2,    'i.faure',     'Mdp@1234',     'medecin'),
    (3,    'k.nakamura',  'Mdp@1234',     'medecin'),
    (4,    's.bencherif', 'Mdp@1234',     'medecin'),
    (5,    'l.garnier',   'Mdp@1234',     'medecin'),
    (6,    'c.moreau',    'Mdp@1234',     'medecin'),
    (7,    'm.dupuis',    'Mdp@1234',     'medecin'),
    (8,    'n.roux',      'Mdp@1234',     'infirmier'),
    (9,    's.martin',    'Mdp@1234',     'infirmier'),
    (10,   'c.bernard',   'Mdp@1234',     'infirmier'),
    (11,   'a.petit',     'Mdp@1234',     'infirmier'),
    (12,   'm.leroy',     'Mdp@1234',     'infirmier'),
    (13,   'j.simon',     'Mdp@1234',     'infirmier'),
    (14,   'f.michel',    'Mdp@1234',     'infirmier'),
    (15,   'a.lefebvre',  'Mdp@1234',     'infirmier'),
    (NULL, 'etl_service', 'Etl@1234',     'etl'),
    (NULL, 'reporting',   'Report@1234',  'reporting');