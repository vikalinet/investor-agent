from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Конфигурация приложения"""
    
    # Database
    database_url: str = "postgresql://investor:investor@localhost:5432/investor_db"
    
    # Search
    search_api_url: str = ""
    search_api_key: str = ""
    
    # LLM
    llm_api_key: str = ""
    llm_model: str = "gpt-4o-mini"
    
    # MCP
    mcp_server_host: str = "localhost"
    mcp_server_port: int = 8001
    
    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    return Settings()
