from typing import Optional, Dict, Any
import requests
from app.core.logging import logger

class HTTPClient:
    def __init__(self):
        self.session = requests.Session()
        self._token: Optional[str] = None
        
    @property
    def headers(self) -> Dict[str, str]:
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        if self._token:
            headers['Authorization'] = f'Bearer {self._token}'
        return headers
    
    def request(
        self,
        method: str,
        url: str,
        **kwargs
    ) -> Dict[str, Any]:
        try:
            response = self.session.request(
                method=method,
                url=url,
                headers=self.headers,
                **kwargs
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"HTTP请求失败: {str(e)}")
            raise

http_client = HTTPClient() 