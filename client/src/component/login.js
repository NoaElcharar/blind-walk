import React from "react";
import { useState } from 'react';
import '../style/Login.css';
import {Link} from 'react-router-dom'

const Login = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  const handleUsernameChange = (event) => {
    setUsername(event.target.value);
  };

  const handlePasswordChange = (event) => {
    setPassword(event.target.value);
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    // Here you can add your authentication logic
    console.log('Username:', username);
    console.log('Password:', password);
    // For now, let's just clear the fields after submission
    setUsername('');
    setPassword('');
  };

  return (
    <div className="enterForm">
      <h2>Login</h2>
      <form onSubmit={handleSubmit}>
        <div>
          <label htmlFor="username">Username:</label>
          <input
            type="text"
            id="username"
            value={username}
            onChange={handleUsernameChange}
            required
          />
        </div>
        <div>
          <label htmlFor="password">Password:</label>
          <input
            type="password"
            id="password"
            value={password}
            onChange={handlePasswordChange}
            required
          />
        </div>
        
        <button type="submit"><Link to="/user-area">login</Link></button>
      </form>
      <Link to ="/sign-up">don't have account? create one!</Link>
    </div>
  );
};

export default Login;

