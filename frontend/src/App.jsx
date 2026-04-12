import { useState } from 'react'
import axios from 'axios'
import './index.css'
import InputSection from './components/InputSection'
import StudyDashboard from './components/StudyDashboard'

function App() {
  const [loading, setLoading] = useState(false)
  const [results, setResults] = useState(null)
  const [error, setError] = useState(null)

  const handleProcessNotes = async (notes, difficulty, examMode) => {
    if (!notes.trim()) return;
    
    setLoading(true);
    setError(null);
    setResults(null);
    
    try {
      const response = await axios.post('http://127.0.0.1:5000/api/process-notes', {
        notes,
        difficulty,
        examMode
      });
      
      setResults(response.data);
    } catch (err) {
      console.error(err);
      setError(err.response?.data?.error || "Failed to connect to the backend server. Make sure it's running.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app-container">
      <header className="header">
        <h1>AI Study Assistant</h1>
        <p>Convert your brain dumps into interactive knowledge & memes</p>
      </header>

      <InputSection onSumbit={handleProcessNotes} loading={loading} />

      {error && (
        <div className="glass-panel" style={{ marginTop: '2rem', borderLeft: '4px solid #ef4444' }}>
          <h3 style={{ color: '#ef4444' }}>Error processing request</h3>
          <p>{error}</p>
        </div>
      )}

      {results && <StudyDashboard data={results} />}
    </div>
  )
}

export default App
