import React, { useState } from 'react';
import '../style/Sign-up.css'; // Import your CSS file for styling
import { Link } from 'react-router-dom';


function SignUp() {
  // הגדרת הסטייט לכל שדה בטופס
  const [firstName, setFirstName] = useState('');
  const [lastName, setLastName] = useState('');
  const [phone, setPhone] = useState('');
  const [email, setEmail] = useState('');

  // פונקציות לעדכון הסטייט עבור כל שדה בהתאם למשתנה input שנשלח
  const handleFirstNameChange = (e) => {
    setFirstName(e.target.value);
  };

  const handleLastNameChange = (e) => {
    setLastName(e.target.value);
  };

  const handlePhoneChange = (e) => {
    setPhone(e.target.value);
  };

  const handleEmailChange = (e) => {
    setEmail(e.target.value);
  };

  // פונקציה לשליחת הטופס
  const handleSubmit = (e) => {
    e.preventDefault();
    // כאן תוכל להוסיף כל מיני פעולות לשליחת הנתונים לשרת או לעיבודם
    console.log('Form submitted:', { firstName, lastName, phone, email });
  };

  return (
    <form className="registration" onSubmit={handleSubmit}>

      <label>
        First Name:
        <input type="text" value={firstName} onChange={handleFirstNameChange} />
      </label>
      <label>
        Last Name:
        <input type="text" value={lastName} onChange={handleLastNameChange} />
      </label>
      <label>
        Phone:
        <input type="tel" value={phone} onChange={handlePhoneChange} />
      </label>
      <label>
        Email:
        <input type="email" value={email} onChange={handleEmailChange} />
      </label>
     <button><Link to="/user-area">send</Link></button> 
      {/* <input type="submit" value="send"/>  */}
    </form>
  );
}

export default SignUp;
// export default function SignUp() {
//     return <div>
//         <h1>Sign up</h1>
        
//     </div>
// }