import React, { useState } from 'react';
import CrimeMap from './CrimeMap';

function App() {
  const [mode, setMode] = useState("recent");

  return (
    <div className="App">
      <h1>Cornell Crime Map</h1>
      <button onClick={() => setMode("recent")}>Recent Crimes (Last 60 Days)</button>
      <button onClick={() => setMode("all")}>All Crimes (Legacy Mode)</button>
      <CrimeMap dataUrl={`/crimes/${mode}.json`} />
    </div>
  );
}

export default App;
