import { Router } from 'express'

import * as authController from '../controllers/authController'

const authRouter = Router()

authRouter.get('/login', authController.tokenController)
authRouter.post('/login', authController.loginController)
authRouter.post('/register', authController.registerController)

export default authRouter
