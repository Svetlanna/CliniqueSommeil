import express from 'express';
import * as NuitController from '../controllers/nuitController.js';

const router = express.Router();

router.get('/:id/run', NuitController.runNuit);
router.get('/:id/stats', NuitController.getStats);

export default router;