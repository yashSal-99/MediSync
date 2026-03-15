import React, { useState } from 'react';
import './index.css';

const App: React.FC = () => {
  const [loadingAction, setLoadingAction] = useState<string | null>(null);
  const [status, setStatus] = useState<{ type: 'idle' | 'loading' | 'success' | 'error', msg: string }>({
    type: 'idle',
    msg: 'System Ready 🚀'
  });
  const [resultData, setResultData] = useState<string | null>(null);

  const handleRecord = async () => {
    setLoadingAction('record');
    setStatus({ type: 'loading', msg: 'Recording Audio (Wait 30s) & Analyzing...' });
    setResultData(null);
    try {
      const res = await fetch('http://localhost:8000/record', { method: 'POST' });
      if (!res.ok) throw new Error("Server error during recording");
      const data = await res.json();
      setStatus({ type: 'success', msg: 'Analysis Complete! ✅' });
      setResultData(data.summary || data.log);
    } catch (err: any) {
      setStatus({ type: 'error', msg: `Recording failed: ${err.message}` });
    } finally {
      setLoadingAction(null);
    }
  };

  const handleUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    if (!e.target.files?.[0]) return;
    const file = e.target.files[0];
    
    setLoadingAction('upload');
    setStatus({ type: 'loading', msg: `Uploading ${file.name}...` });
    setResultData(null);

    const formData = new FormData();
    formData.append('file', file);

    try {
      const res = await fetch('http://localhost:8000/upload', { method: 'POST', body: formData });
      if (!res.ok) throw new Error("Upload failed");
      setStatus({ type: 'success', msg: `${file.name} saved to secure vault ✅` });
    } catch (err: any) {
      setStatus({ type: 'error', msg: `Upload failed: ${err.message}` });
    } finally {
      setLoadingAction(null);
      // Reset input
      e.target.value = '';
    }
  };

  const handleSync = async () => {
    setLoadingAction('sync');
    setStatus({ type: 'loading', msg: 'Syncing documents, running OCR & AI Analysis...' });
    setResultData(null);
    try {
      const res = await fetch('http://localhost:8000/sync', { method: 'POST' });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || "Sync failed");
      
      setStatus({ type: 'success', msg: 'WhatsApp Alert Sent Successfully! 📱' });
      
      // Attempt to clean the output to show just the relevant logs
      const rawLog = data.log || "";
      const cleanedLog = rawLog.includes('SAFETY REPORT:') 
        ? rawLog.substring(rawLog.indexOf('SAFETY REPORT:')) 
        : rawLog;

      setResultData(cleanedLog);
    } catch (err: any) {
      setStatus({ type: 'error', msg: `Sync failed: ${err.message}` });
    } finally {
      setLoadingAction(null);
    }
  };

  return (
    <div className="glass-container">
      <header className="app-header">
        <h1 className="title">MediSync AI</h1>
        <p className="subtitle">Clinical Pharmacist Intelligence System</p>
      </header>

      <div className={`status-banner ${status.type === 'loading' ? 'loading' : status.type === 'error' ? 'error' : ''}`}>
        {status.type === 'loading' && <div className="spinner"></div>}
        {status.msg}
      </div>

      <div className="action-grid">
        {/* Record Action */}
        <button 
          className="action-btn btn-record" 
          onClick={handleRecord} 
          disabled={loadingAction !== null}
        >
          <div className="icon">🎙️</div>
          1. Record Consultation
        </button>

        {/* Upload Action */}
        <label className={`action-btn btn-upload ${loadingAction !== null ? 'disabled' : ''}`}>
          <div className="icon">📑</div>
          2. Upload Documents
          <input 
            type="file" 
            onChange={handleUpload} 
            disabled={loadingAction !== null} 
            accept=".pdf,.png,.jpg,.jpeg,.txt" 
          />
        </label>

        {/* Sync Action */}
        <button 
          className="action-btn btn-sync" 
          onClick={handleSync} 
          disabled={loadingAction !== null}
        >
          <div className="icon">🔄</div>
          3. Process & Alert
        </button>
      </div>

      {resultData && (
        <div className="result-box">
          <h4><span style={{ fontSize: '1.2rem' }}>✨</span> AI Analysis Output</h4>
          {resultData}
        </div>
      )}
    </div>
  );
};

export default App;