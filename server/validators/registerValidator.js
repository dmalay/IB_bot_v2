import Joi from 'joi'

const registerValidation = (data) => {
  const schema = Joi.object({
    username: Joi.string().min(3).max(30).required(),
    email: Joi.string().email({ minDomainSegments: 2 }),
    password: Joi.string().min(3).max(30).required(),
  })
  return schema.validate(data)
}

export default registerValidation
