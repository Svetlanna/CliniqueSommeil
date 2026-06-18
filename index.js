import express from 'express';
import 'dotenv/config';
import { recupererDonnees } from './etl/extract.js';

const app = express();
app.use(express.json());

app.get('/api/nuit/:id/run', async (req, res) => {
    try {
        const { id } = req.params;
        const data = await recupererDonnees(id);

        res.status(200).json({
            status: 'success',
            data: data
        });
    } catch (error) {
        console.error('ETL Error:', error);
        res.status(500).json({ status: 'error', message: error.message });
    }
});

app.listen(8888, () => {
    console.log(`Server is running on http://localhost:8888`);
});