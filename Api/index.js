import express from 'express';
import 'dotenv/config';
import nuitRoutes from './routes/nuitRoutes.js';


const app = express();
app.use(express.json());


app.use('/api/nuit', nuitRoutes);

app.listen(8888, () => console.log(`Server running on http://localhost:8888`));

