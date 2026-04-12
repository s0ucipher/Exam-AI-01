import { useState } from 'react';

export default function StudyDashboard({ data }) {
  if (!data) return null;

  return (
    <div className="dashboard">
      <div className="left-column">
        {/* Summary & Top 5 */}
        <div className="glass-panel" style={{ marginBottom: '2rem' }}>
          <h2 className="section-title">Summary</h2>
          <p className="summary-text">{data.summary}</p>
          
          <h2 className="section-title" style={{ marginTop: '2rem' }}>Top Concepts</h2>
          <div className="concept-list">
            {data.top5?.map((item, idx) => (
              <div key={idx} className="concept-item">
                <h3>{item.concept}</h3>
                <p>{item.explanation}</p>
              </div>
            ))}
          </div>
        </div>

        {/* Quiz Section */}
        {data.quiz && data.quiz.length > 0 && (
          <div className="glass-panel quiz-section">
            <h2 className="section-title">Exam Time 📝</h2>
            {data.quiz.map((q, idx) => (
              <QuizQuestion key={idx} questionData={q} index={idx} />
            ))}
          </div>
        )}
      </div>

      <div className="right-column">
        {/* Meme Section */}
        <div className="glass-panel meme-panel">
          <h2 className="section-title">Meme Break 😂</h2>
          <div className="meme-container">
            {data.meme_url ? (
               <img src={data.meme_url} alt="Study Meme" className="meme-image" />
            ) : (
               <div style={{ padding: '2rem', textAlign: 'center', background: 'rgba(0,0,0,0.2)', borderRadius: '8px' }}>
                 <p>No meme generated.</p>
               </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

function QuizQuestion({ questionData, index }) {
  const [selectedOpt, setSelectedOpt] = useState(null);

  const handleSelect = (opt) => {
    if (selectedOpt) return; // Prevent changing answer
    setSelectedOpt(opt);
  }

  return (
    <div className="question-card">
      <h3 style={{ marginBottom: '1rem', color: '#f8fafc' }}>{index + 1}. {questionData.question}</h3>
      <div className="options-grid">
        {questionData.options.map((opt, i) => {
          let className = "option-btn";
          if (selectedOpt) {
             if (opt === questionData.answer) className += " correct";
             else if (opt === selectedOpt) className += " incorrect";
          }
          
          return (
            <button 
              key={i} 
              className={className}
              onClick={() => handleSelect(opt)}
            >
              {opt}
            </button>
          )
        })}
      </div>
    </div>
  );
}
