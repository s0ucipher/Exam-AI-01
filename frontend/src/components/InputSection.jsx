import { useState } from 'react';

export default function InputSection({ onSumbit, loading }) {
  const [notes, setNotes] = useState('');
  const [difficulty, setDifficulty] = useState('Medium');
  const [examMode, setExamMode] = useState(false);

  const handleSubmit = () => {
    onSumbit(notes, difficulty, examMode);
  };

  return (
    <div className="glass-panel">
      <h2 className="section-title">Paste your notes here</h2>
      <textarea
        value={notes}
        onChange={(e) => setNotes(e.target.value)}
        placeholder="e.g. Mitochondria is the powerhouse of the cell..."
        disabled={loading}
      />
      
      <div className="controls">
        <label className="checkbox-label">
          <input
            type="checkbox"
            checked={examMode}
            onChange={(e) => setExamMode(e.target.checked)}
            disabled={loading}
          />
          Exam Mode (Include Quiz)
        </label>

        <select 
          value={difficulty} 
          onChange={(e) => setDifficulty(e.target.value)}
          disabled={loading}
        >
          <option value="Easy">Easy (Explain like I'm 5)</option>
          <option value="Medium">Medium (Standard)</option>
          <option value="Hard">Hard (University Level)</option>
        </select>

        <button 
          className="btn-primary" 
          onClick={handleSubmit} 
          disabled={loading || !notes.trim()}
        >
          {loading ? (
            <span className="spinner"></span>
          ) : (
            'Generate Study Guide'
          )}
        </button>
      </div>
    </div>
  );
}
