import express from 'express';
import 'dotenv/config';
import nuitRoutes from './routes/nuitRoutes.js';
import MedecinsRoute from './routes/MedecinsRoute.js';
import appareilRoutes from './routes/appareilRoutes.js';
import {medecineRoute} from "./controllers/medecineController.js";

const app = express();
app.use(express.json());
app.use('/api/nuit', nuitRoutes);
app.use('/api/med', medecineRoute);
app.use('/api/appareil', appareilRoutes);

app.listen(8888, () => console.log(`Server running on http://localhost:8888`));