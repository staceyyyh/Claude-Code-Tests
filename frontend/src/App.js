import React, { useState } from 'react';
import axios from 'axios';
import SitemapForm from './components/SitemapForm';
import ContentDashboard from './components/ContentDashboard';

function App() {
  const [analysisData, setAnalysisData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleAnalyze = async (websiteUrl, includeBoth) => {
    setLoading(true);
    setError(null);
    setAnalysisData(null);

    try {
      const response = await axios.post('http://localhost:8000/analyze', {
        url: websiteUrl,
        include_both: includeBoth,
      });
      setAnalysisData(response.data);
    } catch (err) {
      setError(err.response?.data?.detail || err.message || 'Failed to analyze sitemap');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="App">
      <header className="app-header">
        <h1>🔍 Sitemap Analyzer</h1>
        <p>Discover all pages on a website and analyze their structure</p>
      </header>
      <main className="app-container">
        <SitemapForm onAnalyze={handleAnalyze} loading={loading} />
        {error && <div className="error-box"><p>⚠️ Error: {error}</p></div>}
        {loading && <div className="loading-box"><p>⏳ Analyzing sitemap...</p></div>}
        {analysisData && !loading && (
          <ContentDashboard 
            totalUrls={analysisData.total_urls}
            sitemaps={analysisData.sitemaps_found}
            urlList={analysisData.urls.map(u => u.url)}
          />
        )}
      </main>
    </div>
  );
}

export default App;