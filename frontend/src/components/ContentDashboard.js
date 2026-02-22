import React from 'react';

const ContentDashboard = ({ totalUrls, sitemaps, urlList }) => {
    return (
        <div>
            <h1>Analysis Results</h1>
            <p>Total URLs: {totalUrls}</p>
            <p>Sitemaps Found: {sitemaps.length}</p>
            <h2>List of URLs:</h2>
            <ul>
                {urlList.map((url, index) => (
                    <li key={index}>
                        <a href={url} target="_blank" rel="noopener noreferrer">{url}</a>
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default ContentDashboard;