import { useState } from 'react';
import axios from 'axios';
import './index.css';

function App() {
  const [file, setFile] = useState(null);
  const [feedback, setFeedback] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleUpload = async () => {
    if (!file) {
      alert('Please upload a resume first!');
      return;
    }

    setLoading(true);
    setError(null);
    const formData = new FormData();
    formData.append('file', file);
    console.log('Uploading file:', file.name, file.type);

    try {
      const backendurl = import.meta.env.VITE_BACKEND_URL
      const response = await axios.post(`${backendurl}/analyze`, formData);
      console.log('Response data:', response.data);
      setFeedback(response.data);
    } catch (error) {
      console.error('Error uploading resume:', error.response?.data || error.message);
      setError(error.response?.data?.detail || 'Something went wrong');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">
      <h1>Resume Coach</h1>
      <div className="upload-section">
        <input type="file" accept=".pdf,.docx" onChange={handleFileChange} />
        <button onClick={handleUpload} disabled={loading}>
          {loading ? 'Analyzing...' : 'Analyze Resume'}
        </button>
      </div>

      {error && (
        <div className="error-section" style={{ color: 'red', marginTop: '20px' }}>
          <h2>Error</h2>
          <p>{error}</p>
        </div>
      )}

      {feedback && !error && (
        <div className="feedback-section">
          {/* Feedback Section */}
          <h2>Personalized Feedback</h2>
          {feedback.feedback && (
            <>
              <h3>Strengths</h3>
              {Array.isArray(feedback.feedback.strengths) && feedback.feedback.strengths.length > 0 ? (
                <ul>
                  {feedback.feedback.strengths.map((strength, index) => (
                    <li key={index}>{strength}</li>
                  ))}
                </ul>
              ) : (
                <p>No strengths provided</p>
              )}

              <h3>Areas for Improvement</h3>
              {Array.isArray(feedback.feedback.areas_for_improvement) && feedback.feedback.areas_for_improvement.length > 0 ? (
                <ul>
                  {feedback.feedback.areas_for_improvement.map((area, index) => (
                    <li key={index}>{area}</li>
                  ))}
                </ul>
              ) : (
                <p>No areas for improvement provided</p>
              )}
            </>
          )}

          {/* Next Steps Section */}
          <h2>Next Steps</h2>
          {feedback.next_steps && (
            <>
              <h3>Certifications</h3>
              {Array.isArray(feedback.next_steps.certifications) && feedback.next_steps.certifications.length > 0 ? (
                <ul>
                  {feedback.next_steps.certifications.map((cert, index) => (
                    <li key={index}>{cert}</li>
                  ))}
                </ul>
              ) : (
                <p>No certifications suggested</p>
              )}

              <h3>Networking</h3>
              {Array.isArray(feedback.next_steps.networking) && feedback.next_steps.networking.length > 0 ? (
                <ul>
                  {feedback.next_steps.networking.map((net, index) => (
                    <li key={index}>{net}</li>
                  ))}
                </ul>
              ) : (
                <p>No networking steps suggested</p>
              )}

              <h3>Continuous Learning</h3>
              {Array.isArray(feedback.next_steps.continuous_learning) && feedback.next_steps.continuous_learning.length > 0 ? (
                <ul>
                  {feedback.next_steps.continuous_learning.map((learn, index) => (
                    <li key={index}>{learn}</li>
                  ))}
                </ul>
              ) : (
                <p>No learning steps suggested</p>
              )}
            </>
          )}

          {/* Career Advice Section */}
          <h2>Career Advice</h2>
          {feedback.advice && (
            <>
              <h3>Personal Branding</h3>
              {Array.isArray(feedback.advice.personal_branding) && feedback.advice.personal_branding.length > 0 ? (
                <ul>
                  {feedback.advice.personal_branding.map((brand, index) => (
                    <li key={index}>{brand}</li>
                  ))}
                </ul>
              ) : (
                <p>No personal branding advice provided</p>
              )}

              <h3>Career Growth</h3>
              {Array.isArray(feedback.advice.career_growth) && feedback.advice.career_growth.length > 0 ? (
                <ul>
                  {feedback.advice.career_growth.map((growth, index) => (
                    <li key={index}>{growth}</li>
                  ))}
                </ul>
              ) : (
                <p>No career growth advice provided</p>
              )}

              <h3>Interview Preparation</h3>
              {Array.isArray(feedback.advice.interview_preparation) && feedback.advice.interview_preparation.length > 0 ? (
                <ul>
                  {feedback.advice.interview_preparation.map((prep, index) => (
                    <li key={index}>{prep}</li>
                  ))}
                </ul>
              ) : (
                <p>No interview preparation advice provided</p>
              )}
            </>
          )}
        </div>
      )}
    </div>
  );
}

export default App;