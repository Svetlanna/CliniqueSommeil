-- ============================================================
-- Script de création des procédures stockées
-- Base : evenement_respiratoire
-- ============================================================

-- Suppression des procédures existantes avant recréation
DROP PROCEDURE IF EXISTS `sp_compteur_all`;
DROP PROCEDURE IF EXISTS `sp_compteur_rera`;
DROP PROCEDURE IF EXISTS `sp_compteur_apnees`;
DROP PROCEDURE IF EXISTS `sp_compteur_hypopnae`;

DELIMITER $$

-- ------------------------------------------------------------
-- Procédure : sp_compteur_all
-- Description : Compte tous les événements respiratoires
-- ------------------------------------------------------------
CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_compteur_all`()
BEGIN
    SELECT COUNT(*) FROM evenement_respiratoire;
END$$

-- ------------------------------------------------------------
-- Procédure : sp_compteur_rera
-- Description : Compte les événements de type RERA
-- ------------------------------------------------------------
CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_compteur_rera`()
BEGIN
    SELECT COUNT(*) FROM evenement_respiratoire WHERE type_evenement LIKE 'RERA';
END$$

-- ------------------------------------------------------------
-- Procédure : sp_compteur_apnees
-- Description : Compte les apnées obstructives et centrales
-- ------------------------------------------------------------
CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_compteur_apnees`()
BEGIN
    SELECT COUNT(*) FROM evenement_respiratoire WHERE type_evenement 
    LIKE 'apnÃ©e obstructive' OR type_evenement LIKE 'apnÃ©e centrale';
END$$

-- ------------------------------------------------------------
-- Procédure : sp_compteur_hypopnae
-- Description : Compte les hypopnées
-- ------------------------------------------------------------
CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_compteur_hypopnae`()
BEGIN
    SELECT COUNT(*) FROM evenement_respiratoire WHERE type_evenement LIKE 'hypopnÃ©e';
END$$

DELIMITER ;

-- ============================================================
-- Vérification : liste des procédures créées
-- ============================================================
SHOW PROCEDURE STATUS WHERE Db = DATABASE();