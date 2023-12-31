import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import './Register.css'
import EffectInput from '../components/EffectInput'
import axios from 'axios'
import { InputObject } from '../classes/InputObject'
import { Link } from 'react-router-dom'
import { config } from '../config/app-config'
import ConfirmRegistration from '../components/ConfirmRegistration'

const url = config.backendUrl
const registerUrl = url + '/register'
const usernameExistsUrl = registerUrl + '/username-exists'
const emailExistsUrl = registerUrl + '/email-exists'

export default function Register() {
  const [registered, setRegistered] = useState(false)
  const [token, setToken] = useState()
  const navigate = useNavigate()

  useEffect(() => {
    if (localStorage.jwt) navigate('/')
  }, [])

  const [username, setUsername] = useState('')
  const [usernameValid, setUsernameValid] = useState(true)
  const [usernameServerValid, setUsernameServerValid] = useState(true)
  const usernameObj = new InputObject(
    username,
    setUsername,
    usernameValid,
    setUsernameValid,
    (newValue) => newValue.length <= 30,
    () => username.length >= 6,
    'Username must be 6-30 chars long',
    usernameServerValid,
    setUsernameServerValid,
    () => checkIfUsernameIsNotTaken(username),
    'Username is taken'
  )
  const [email, setEmail] = useState('')
  const [emailValid, setEmailValid] = useState(true)
  const [emailServerValid, setEmailServerValid] = useState(true)
  const emailObj = new InputObject(
    email,
    setEmail,
    emailValid,
    setEmailValid,
    (newValue) => true,
    () =>
      email.match('\\w+@\\w+\\.\\w+') &&
      email.match('\\w+@\\w+\\.\\w+')[0] === email,
    'Email is invalid',
    emailServerValid,
    setEmailServerValid,
    () => checkIfEmailIsNotTaken(email),
    'This email is already registered'
  )
  const [password, setPassword] = useState('')
  const [passwordValid, setPasswordValid] = useState(true)
  const passwordObj = new InputObject(
    password,
    setPassword,
    passwordValid,
    setPasswordValid,
    (newValue) => newValue.length <= 30,
    () => password.length >= 8,
    'Password must be 8-30 chars long'
  )
  const [passwordRepeat, setPasswordRepeat] = useState('')
  const [passwordRepeatValid, setPasswordRepeatValid] = useState(true)
  const passwordRepeatObj = new InputObject(
    passwordRepeat,
    setPasswordRepeat,
    passwordRepeatValid,
    setPasswordRepeatValid,
    (newValue) => true,
    () => passwordRepeat === password,
    'Passwords are not the same'
  )

  const baseLoseFocusPasswordFunction = passwordObj.onLoseFocusPredicate
  passwordObj.onLoseFocusPredicate = function () {
    const repeatPasswordFunction = passwordRepeatObj.onLoseFocusPredicate
    if (!repeatPasswordFunction(passwordRepeatObj.value))
      passwordRepeatObj.setValid(false)
    else {
      passwordRepeatObj.setValid(true)
    }
    return baseLoseFocusPasswordFunction()
  }

  async function checkIfUsernameIsNotTaken(username) {
    return await axios
      .get(usernameExistsUrl, { params: { username } })
      // 200 - username is taken
      .then((response) => {
        if (response.status !== 200) throw new Exception('An error occured')
        return !response.data
      })
      // 404 - username is not taken
      .catch((error) => error.response.status === 404)
  }

  async function checkIfEmailIsNotTaken(email) {
    return await axios
      .get(emailExistsUrl, { params: { email } })
      .then((response) => {
        if (response.status !== 200) throw new Exception('An error occured')
        return !response.data
      })
      // 404 - username is not taken
      .catch((error) => error.response.status === 404)
  }

  function register() {
    if (!validateInputs(username, email, password, passwordRepeat)) {
      return
    }

    let registerRequestBody = {
      username: username,
      email: email,
      password: password,
    }

    axios.post(registerUrl, new URLSearchParams(registerRequestBody)).then((response) => {
      if (response.status === 200) {
        setToken(response.data)
        navigate('/login')
      }
    })
  }

  function validateInputs(username, email, password, passwordRepeat) {
    // validate username
    if (
      !usernameObj.onChangePredicate(username) ||
      !usernameObj.onLoseFocusPredicate() ||
      !usernameObj.onLoseApiCallPredicate()
    ) {
      return false
    }

    // validate email
    if (
      !emailObj.onChangePredicate(email) ||
      !emailObj.onLoseFocusPredicate() ||
      !emailObj.onLoseApiCallPredicate()
    ) {
      return false
    }

    // validate password
    if (
      !passwordObj.onChangePredicate(password) ||
      !passwordObj.onLoseFocusPredicate() ||
      !passwordRepeatObj.onLoseFocusPredicate(passwordRepeat)
    ) {
      return false
    }

    return true
  }

  return (
    <div className="register-box">
          <Link to="/login" className="register-login-link">
            <p>Login</p>
          </Link>
          <h1 className="register-title">Create an account</h1>
          <form className="register-form">
            <EffectInput
              name="username"
              type="text"
              inputObject={usernameObj}
            />
            <EffectInput name="email" type="email" inputObject={emailObj} />
            <EffectInput
              name="password"
              type="password"
              inputObject={passwordObj}
            />
            <EffectInput
              name="repeat password"
              type="password"
              inputObject={passwordRepeatObj}
            />
            <button className="register-btn" type="button" onClick={register}>
              Register
            </button>
          </form>
    </div>
  )
}
