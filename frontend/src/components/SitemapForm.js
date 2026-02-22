import React, { useState } from 'react';

const SitemapForm = () => {
    const [url, setUrl] = useState('');
    const [includeXml, setIncludeXml] = useState(false);
    const [includeHtml, setIncludeHtml] = useState(false);

    const handleSubmit = (e) => {
        e.preventDefault();
        // Handle form submission logic here
        console.log({ url, includeXml, includeHtml });
    };

    return (
        <form onSubmit={handleSubmit}>
            <div>
                <label htmlFor="url">Website URL:</label>
                <input 
                    type="url" 
                    id="url" 
                    value={url} 
                    onChange={(e) => setUrl(e.target.value)} 
                    required 
                />
            </div>
            <div>
                <label>
                    <input 
                        type="checkbox" 
                        checked={includeXml} 
                        onChange={(e) => setIncludeXml(e.target.checked)} 
                    />
                    Include XML Sitemap
                </label>
            </div>
            <div>
                <label>
                    <input 
                        type="checkbox" 
                        checked={includeHtml} 
                        onChange={(e) => setIncludeHtml(e.target.checked)} 
                    />
                    Include HTML Sitemap
                </label>
            </div>
            <button type="submit">Generate Sitemap</button>
        </form>
    );
};

export default SitemapForm;