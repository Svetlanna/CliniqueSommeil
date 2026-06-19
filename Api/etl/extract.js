import fs from 'fs';
import path from 'path';
import mysql from 'mysql2/promise';
import csvParser from 'csv-parser';
import { fileURLToPath } from 'url';




const pool = mysql.createPool({
    host: process.env.DB_HOST || 'localhost',
    user: process.env.DB_USER || 'root',
    port: process.env.DB_PORT || 3306,
    password: process.env.DB_PASSWORD || 'Kiljaeden34!',
    database: process.env.DB_NAME || "clinique_arles",
    waitForConnections: true,
    connectionLimit: 10
});

export async function recupererDonnees(idNuit) {
    const __filename = fileURLToPath(import.meta.url);
    const __dirname = path.dirname(__filename);
    const baseDir = path.join(__dirname, '..', 'raw', 'traite');
    const cheminCsv = path.join(baseDir, `signal-psg-patient-${idNuit}-nuit-${idNuit}.csv`);
    

    // pool.execute directement
const dfCapteur = await new Promise((resolve, reject) => {

    if (!fs.existsSync(cheminCsv)) {
        return reject(new Error(`Fichier introuvable : ${cheminCsv}`));
    }

    const results = [];
    fs.createReadStream(cheminCsv)//permet de lire un fichier par morceaux (flux) fs (file system)
        .on('error', (err) => {
            console.error("Erreur spécifique lors de la lecture du CSV :");
            reject(err);
        })
        .pipe(csvParser())
        .on('data', (data) => results.push(data))
        .on('end', () => {
            console.log("Lecture CSV terminée avec succès.");
            resolve(results);
        });
});


    try {
        const [dfEvents] = await pool.execute(
            'SELECT * FROM evenement_respiratoire WHERE id_nuit = ?',
            [idNuit]
        );

        const [nbApnees, nbHypopnees, nbRera, nbrEvents] = await Promise.all([
            pool.query("CALL sp_compteur_apnees()"),
            pool.query("CALL sp_compteur_hypopnee()"),
            pool.query("CALL sp_compteur_rera()"),
            pool.query("CALL sp_compteur_all()")
        ]);

return {
            df_capteur: dfCapteur,
            df_events: dfEvents,
            nbapnees: nbApnees[0][0],
            nbhypopnees: nbHypopnees[0][0],
            nbrera: nbRera[0][0],
            nbr_events: nbrEvents[0][0]
        };
    } catch (error) {
        console.error("Erreur lors de la récupération des données:", error);
        throw error;
    }


}