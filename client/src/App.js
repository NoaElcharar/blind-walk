import React, { useEffect } from 'react';
import Login from './component/login';

import logo from './logo.svg';
import './App.css';
import { userState } from 'react';
import ImageUploader from './component/ImageUploader';
import { Routes, Route, useNavigate } from 'react-router-dom'
import EmpyComponent from './component/EmpyComponent';
import loginenrollmen from './'
import SignUp from './component/Sign-up';
import UserArea from './component/UserArea';
import Header from './component/Header';
import Address from './component/Address';
function App() {
  const navigate = useNavigate()

  useEffect(() => {


    const myUser = sessionStorage.getItem("user")
    if (myUser == undefined) {
      sessionStorage.setItem('user', 'login')
      navigate('login')
    }
  })
  return (<>
    <Header />
    <div className='dataInPage'>

      <Routes>

        <Route path="login" element={<Login />} />
        <Route path="sign-up" element={<SignUp />} />
        <Route path="user-area"  >
          <Route index element={<UserArea />}/>
          <Route path="address" element={<Address />} />
        </Route>
        </Routes>
        {/* <ImageUploader type={"video"}/>
      <ImageUploader type={"img"}/> */}
    </div>
  </>
  );
}

export default App;
