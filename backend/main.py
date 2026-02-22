from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
import xml.etree.ElementTree as ET
from typing import List, Optional

app = FastAPI(title="Sitemap Analyzer API", description="Analyzes website sitemaps to identify and group content")

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"],)

class AnalyzeRequest(BaseModel):
    url: str
    include_both: bool = False

class URLItem(BaseModel):
    url: str
    priority: Optional[float] = None

class AnalysisResponse(BaseModel):
    status: str
    total_urls: int
    sitemaps_found: List[str]
    urls: List[URLItem]

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.post("/analyze")
def analyze(request: AnalyzeRequest):
    try:
        sitemap_urls = find_sitemaps(request.url)
        if not sitemap_urls:
            raise HTTPException(status_code=404, detail="No sitemaps found")
        all_urls = []
        for sitemap_url in sitemap_urls:
            urls = parse_sitemap(sitemap_url)
            all_urls.extend(urls)
        url_items = [URLItem(url=url) for url in all_urls]
        return {"status": "success", "total_urls": len(url_items), "sitemaps_found": sitemap_urls, "urls": url_items[:200]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def find_sitemaps(base_url: str) -> List[str]:
    base_url = base_url.rstrip('/')
    sitemaps = []
    try:
        response = requests.get(f"{base_url}/robots.txt", timeout=5)
        for line in response.text.split('\n'):
            if line.lower().startswith('sitemap:'):
                sitemap = line.split(':', 1)[1].strip()
                if sitemap:
                    sitemaps.append(sitemap)
    except:
        pass
    common_paths = ['/sitemap.xml', '/sitemap_index.xml', '/sitemap.html']
    for path in common_paths:
        try:
            url = f"{base_url}{path}"
            response = requests.head(url, timeout=5, allow_redirects=True)
            if response.status_code == 200 and url not in sitemaps:
                sitemaps.append(url)
        except:
            pass
    return list(set(sitemaps))


def parse_sitemap(sitemap_url: str) -> List[str]:
    urls = []
    try:
        response = requests.get(sitemap_url, timeout=10)
        if response.status_code != 200:
            return urls
        root = ET.fromstring(response.content)
        namespace = {'sitemap': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
        for url_element in root.findall('sitemap:url', namespace):
            loc = url_element.find('sitemap:loc', namespace)
            if loc is not None and loc.text:
                urls.append(loc.text)
    except Exception as e:
        print(f"Error parsing sitemap {sitemap_url}: {e}")
    return urls

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)