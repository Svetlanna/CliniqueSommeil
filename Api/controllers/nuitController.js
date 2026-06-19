

import * as NuitModel from '../models/nuitModel.js';

export const runNuit = async (req, res) => {
    try {
        const data = await NuitModel.getNuitData(req.params.id);
        res.status(200).json({ status: 'success', data });
    } catch (error) {
        res.status(500).json({ status: 'error', message: error.message });
    }
};

export const getStats = async (req, res) => {
    try {
        const stats = await NuitModel.getStatsNuit(req.params.id);
        res.status(200).json({ status: 'success', id_nuit: req.params.id, indicateurs: stats });
    } catch (error) {
        res.status(500).json({ status: 'error', message: error.message });
    }
};