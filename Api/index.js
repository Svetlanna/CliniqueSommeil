import express from 'express';
import 'dotenv/config';
import nuitRoutes from './routes/nuitRoutes.js';
import appareilRoutes from './routes/appareilRoutes.js';
import authRoutes from './routes/authRoutes.js';

const app = express();
app.use(express.json());

app.use('/api/auth', authRoutes);
app.use('/api/nuit', nuitRoutes);
app.use('/api/appareil', appareilRoutes);

app.listen(8888, () => console.log(`Server running on http://localhost:8888`));