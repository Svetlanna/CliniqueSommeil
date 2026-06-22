import { pool } from '../config/db.js';

export const login = async (req, res) => {
    const { login, mot_de_passe } = req.body;

    if (!login || !mot_de_passe) {
        return res.status(400).json({ status: 'error', message: 'Login et mot de passe requis' });
    }

    const [rows] = await pool.query(
        'SELECT id_utilisateur, login, role FROM utilisateur WHERE login = ? AND mot_de_passe = ? AND actif = 1',
        [login, mot_de_passe]
    );

    if (rows.length === 0) {
        return res.status(401).json({ status: 'error', message: 'Identifiants invalides' });
    }

    res.json({ status: 'success', data: rows[0] });
};
