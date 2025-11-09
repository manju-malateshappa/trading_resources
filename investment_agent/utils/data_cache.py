"""Data cache and refresh management for stock data."""

import json
import sqlite3
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime, timedelta

from .logger import logger


class DataCache:
    """Manage cached stock data with refresh capabilities."""

    def __init__(self, db_path: str = None):
        """Initialize data cache.

        Args:
            db_path: Path to SQLite database
        """
        if db_path is None:
            db_dir = Path(__file__).parent.parent / "data"
            db_dir.mkdir(exist_ok=True)
            db_path = str(db_dir / "data_cache.db")

        self.db_path = db_path
        self._init_database()

    def _init_database(self) -> None:
        """Initialize database tables."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Table for cached stock data
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS stock_cache (
                symbol TEXT PRIMARY KEY,
                name TEXT,
                market TEXT,
                last_updated TEXT NOT NULL,
                data TEXT NOT NULL,
                error_count INTEGER DEFAULT 0
            )
        """)

        # Table for refresh history
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS refresh_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                refresh_date TEXT NOT NULL,
                symbols_count INTEGER NOT NULL,
                successful_count INTEGER NOT NULL,
                failed_count INTEGER NOT NULL,
                duration_seconds REAL NOT NULL
            )
        """)

        conn.commit()
        conn.close()

    def is_stale(self, symbol: str, max_age_hours: int = 24) -> bool:
        """Check if cached data is stale.

        Args:
            symbol: Stock ticker symbol
            max_age_hours: Maximum age in hours before considered stale

        Returns:
            True if stale or not cached, False otherwise
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute(
            "SELECT last_updated FROM stock_cache WHERE symbol = ?",
            (symbol.upper(),)
        )
        result = cursor.fetchone()
        conn.close()

        if not result:
            return True  # Not cached

        last_updated = datetime.fromisoformat(result[0])
        age = datetime.now() - last_updated

        return age > timedelta(hours=max_age_hours)

    def get_cached_data(self, symbol: str) -> Optional[Dict]:
        """Get cached data for a symbol.

        Args:
            symbol: Stock ticker symbol

        Returns:
            Cached data dict or None
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute(
            "SELECT data, last_updated FROM stock_cache WHERE symbol = ?",
            (symbol.upper(),)
        )
        result = cursor.fetchone()
        conn.close()

        if result:
            data = json.loads(result[0])
            data['cache_updated'] = result[1]
            return data

        return None

    def cache_data(self, symbol: str, data: Dict, name: str = None, market: str = None) -> None:
        """Cache stock data.

        Args:
            symbol: Stock ticker symbol
            data: Data to cache
            name: Company name (optional)
            market: Market (optional)
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute(
            """INSERT OR REPLACE INTO stock_cache
               (symbol, name, market, last_updated, data, error_count)
               VALUES (?, ?, ?, ?, ?, 0)""",
            (symbol.upper(), name, market, datetime.now().isoformat(), json.dumps(data))
        )

        conn.commit()
        conn.close()

        logger.debug(f"Cached data for {symbol}")

    def get_all_cached_symbols(self, market: str = None) -> List[Dict]:
        """Get all cached symbols.

        Args:
            market: Filter by market (optional)

        Returns:
            List of cached symbols with metadata
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        if market:
            cursor.execute(
                """SELECT symbol, name, market, last_updated
                   FROM stock_cache
                   WHERE market = ?
                   ORDER BY symbol""",
                (market.upper(),)
            )
        else:
            cursor.execute(
                """SELECT symbol, name, market, last_updated
                   FROM stock_cache
                   ORDER BY market, symbol"""
            )

        results = []
        for row in cursor.fetchall():
            last_updated = datetime.fromisoformat(row[3])
            age_hours = (datetime.now() - last_updated).total_seconds() / 3600

            results.append({
                'symbol': row[0],
                'name': row[1],
                'market': row[2],
                'last_updated': row[3],
                'age_hours': age_hours,
                'is_stale': age_hours > 24
            })

        conn.close()

        return results

    def get_stale_symbols(self, max_age_hours: int = 24) -> List[str]:
        """Get symbols with stale data.

        Args:
            max_age_hours: Maximum age in hours

        Returns:
            List of stale symbols
        """
        cached = self.get_all_cached_symbols()
        return [item['symbol'] for item in cached if item['age_hours'] > max_age_hours]

    def record_refresh(self, symbols_count: int, successful: int, failed: int, duration: float) -> None:
        """Record a refresh operation.

        Args:
            symbols_count: Total symbols attempted
            successful: Number of successful refreshes
            failed: Number of failed refreshes
            duration: Duration in seconds
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute(
            """INSERT INTO refresh_history
               (refresh_date, symbols_count, successful_count, failed_count, duration_seconds)
               VALUES (?, ?, ?, ?, ?)""",
            (datetime.now().isoformat(), symbols_count, successful, failed, duration)
        )

        conn.commit()
        conn.close()

    def get_refresh_history(self, limit: int = 10) -> List[Dict]:
        """Get refresh history.

        Args:
            limit: Number of records to return

        Returns:
            List of refresh records
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute(
            """SELECT refresh_date, symbols_count, successful_count, failed_count, duration_seconds
               FROM refresh_history
               ORDER BY refresh_date DESC
               LIMIT ?""",
            (limit,)
        )

        history = []
        for row in cursor.fetchall():
            history.append({
                'date': row[0],
                'total': row[1],
                'successful': row[2],
                'failed': row[3],
                'duration': row[4]
            })

        conn.close()

        return history

    def clear_cache(self, symbol: str = None) -> int:
        """Clear cache.

        Args:
            symbol: Specific symbol to clear (or None for all)

        Returns:
            Number of records deleted
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        if symbol:
            cursor.execute("DELETE FROM stock_cache WHERE symbol = ?", (symbol.upper(),))
        else:
            cursor.execute("DELETE FROM stock_cache")

        rows_deleted = cursor.rowcount

        conn.commit()
        conn.close()

        logger.info(f"Cleared cache: {rows_deleted} records deleted")

        return rows_deleted

    def get_cache_stats(self) -> Dict:
        """Get cache statistics.

        Returns:
            Dictionary with cache stats
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Total cached symbols
        cursor.execute("SELECT COUNT(*) FROM stock_cache")
        total = cursor.fetchone()[0]

        # By market
        cursor.execute("""
            SELECT market, COUNT(*) FROM stock_cache
            GROUP BY market
            ORDER BY COUNT(*) DESC
        """)
        by_market = {row[0] or 'Unknown': row[1] for row in cursor.fetchall()}

        # Stale count (>24 hours)
        cursor.execute("""
            SELECT COUNT(*) FROM stock_cache
            WHERE datetime(last_updated) < datetime('now', '-24 hours')
        """)
        stale_count = cursor.fetchone()[0]

        # Fresh count (<1 hour)
        cursor.execute("""
            SELECT COUNT(*) FROM stock_cache
            WHERE datetime(last_updated) > datetime('now', '-1 hour')
        """)
        fresh_count = cursor.fetchone()[0]

        conn.close()

        return {
            'total': total,
            'by_market': by_market,
            'stale': stale_count,
            'fresh': fresh_count,
            'aged': total - stale_count - fresh_count
        }


# Global instance
data_cache = DataCache()

__all__ = ['DataCache', 'data_cache']
