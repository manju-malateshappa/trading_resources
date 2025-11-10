"""Configuration loader for the investment agent."""

import os
import yaml
from pathlib import Path
from typing import Any, Dict
from dotenv import load_dotenv

class ConfigLoader:
    """Load and manage configuration settings."""

    def __init__(self, config_path: str = None):
        """Initialize configuration loader.

        Args:
            config_path: Path to YAML configuration file
        """
        # Load environment variables
        load_dotenv()

        # Load YAML configuration
        if config_path is None:
            config_path = Path(__file__).parent.parent / "config" / "settings.yaml"

        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)

    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value by dot-notation key.

        Args:
            key: Configuration key in dot notation (e.g., 'strategy.entry.min_revenue_growth')
            default: Default value if key not found

        Returns:
            Configuration value
        """
        keys = key.split('.')
        value = self.config

        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
                if value is None:
                    return default
            else:
                return default

        return value

    def get_env(self, key: str, default: Any = None) -> Any:
        """Get environment variable.

        Args:
            key: Environment variable name
            default: Default value if not found

        Returns:
            Environment variable value
        """
        return os.getenv(key, default)

    def get_api_keys(self) -> Dict[str, str]:
        """Get all API keys from environment variables.

        Returns:
            Dictionary of API keys
        """
        return {
            'alpha_vantage': self.get_env('ALPHA_VANTAGE_API_KEY'),
            'finnhub': self.get_env('FINNHUB_API_KEY'),
            'news_api': self.get_env('NEWS_API_KEY'),
            'fred': self.get_env('FRED_API_KEY'),
        }

    def get_risk_params(self) -> Dict[str, Any]:
        """Get risk management parameters.

        Returns:
            Dictionary of risk parameters
        """
        return {
            'max_position_size': float(self.get_env('MAX_POSITION_SIZE', 0.15)),
            'stop_loss': self.get('risk.max_drawdown', 0.20),
            'max_portfolio_volatility': self.get('risk.max_portfolio_volatility', 0.25),
            'min_cash_reserve': float(self.get_env('MIN_CASH_RESERVE', 0.10)),
        }

# Global configuration instance
config = ConfigLoader()

__all__ = ['config', 'ConfigLoader']
