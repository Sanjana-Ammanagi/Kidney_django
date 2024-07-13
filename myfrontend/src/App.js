

import React, { useState } from 'react';
import axios from 'axios';
import './App.css'; 
import logo from './kc.png';

function App() {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
  };

  const handleUpload = async () => {
    if (!file) {
      alert('Please select a file to upload');
      return;
    }

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await axios.post('http://localhost:8000/api/upload/', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      if (response.data && response.data.prediction) {
        setResult(response.data.prediction);
        setError(null); 
      } else {
        setError('Result not found in response');
        setResult(null);
      }
    } catch (error) {
      console.error('Error uploading file:', error);
      setError('Error uploading file');
      setResult(null);
    }
  };

  return (
    <div className="App">
      <nav className="App-navbar">
        <img src={logo} className="App-logo" alt="logo" /> 
        <h1 className='hospital'>Kidney Care</h1>
      </nav>
      <div className="upload-container">
        <header className="App-header">
          <h1>Upload an Image</h1>
        </header>
        <div className="card">
          <div className="upload-template">
            <label>    
            Select an image to upload:
              <input type="file" onChange={handleFileChange}/>
            </label>
            <br />
            <button onClick={handleUpload}>Upload</button>
          </div>
        </div>
        {error && <p className="error-message">{error}</p>}
        {result !== null && (
          <div className="result-card">
            <h2>Result</h2>
            <p>{result}</p>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
