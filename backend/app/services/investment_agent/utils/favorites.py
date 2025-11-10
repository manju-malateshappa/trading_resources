"""Favorites management system for tracking preferred stocks."""

import json
import sqlite3
from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime

from .logger import logger


class FavoritesManager:
    """Manage favorite stocks with categories."""

    def __init__(self, db_path: str = None):
        """Initialize favorites manager.

        Args:
            db_path: Path to SQLite database
        """
        if db_path is None:
            db_dir = Path(__file__).parent.parent / "data"
            db_dir.mkdir(exist_ok=True)
            db_path = str(db_dir / "favorites.db")

        self.db_path = db_path
        self._init_database()

    def _init_database(self) -> None:
        """Initialize database tables."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS favorites (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                symbol TEXT NOT NULL UNIQUE,
                name TEXT,
                category TEXT DEFAULT 'general',
                added_date TEXT NOT NULL,
                notes TEXT
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                description TEXT,
                created_date TEXT NOT NULL
            )
        """)

        # Add default categories
        default_categories = [
            ('general', 'General favorites'),
            ('usa', 'US market stocks'),
            ('canada', 'Canadian market stocks'),
            ('india', 'Indian market stocks'),
            ('ai', 'AI companies'),
            ('tech', 'Technology stocks'),
            ('healthcare', 'Healthcare stocks'),
            ('fintech', 'Fintech companies'),
            ('watchlist', 'Active watchlist'),
        ]

        for cat_name, cat_desc in default_categories:
            cursor.execute(
                "INSERT OR IGNORE INTO categories (name, description, created_date) VALUES (?, ?, ?)",
                (cat_name, cat_desc, datetime.now().isoformat())
            )

        conn.commit()
        conn.close()

    def add(self, symbol: str, category: str = 'general', name: str = None, notes: str = None) -> bool:
        """Add a stock to favorites.

        Args:
            symbol: Stock ticker symbol
            category: Category name
            name: Company name (optional)
            notes: Additional notes (optional)

        Returns:
            True if added successfully, False if already exists
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        try:
            cursor.execute(
                """INSERT INTO favorites (symbol, name, category, added_date, notes)
                   VALUES (?, ?, ?, ?, ?)""",
                (symbol.upper(), name, category.lower(), datetime.now().isoformat(), notes)
            )
            conn.commit()
            logger.info(f"Added {symbol} to favorites (category: {category})")
            return True

        except sqlite3.IntegrityError:
            logger.warning(f"{symbol} already in favorites")
            return False

        finally:
            conn.close()

    def remove(self, symbol: str) -> bool:
        """Remove a stock from favorites.

        Args:
            symbol: Stock ticker symbol

        Returns:
            True if removed, False if not found
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("DELETE FROM favorites WHERE symbol = ?", (symbol.upper(),))
        rows_affected = cursor.rowcount

        conn.commit()
        conn.close()

        if rows_affected > 0:
            logger.info(f"Removed {symbol} from favorites")
            return True
        else:
            logger.warning(f"{symbol} not found in favorites")
            return False

    def get_all(self, category: str = None) -> List[Dict]:
        """Get all favorites, optionally filtered by category.

        Args:
            category: Category filter (optional)

        Returns:
            List of favorite stocks
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        if category:
            cursor.execute(
                "SELECT symbol, name, category, added_date, notes FROM favorites WHERE category = ? ORDER BY added_date DESC",
                (category.lower(),)
            )
        else:
            cursor.execute("SELECT symbol, name, category, added_date, notes FROM favorites ORDER BY added_date DESC")

        favorites = []
        for row in cursor.fetchall():
            favorites.append({
                'symbol': row[0],
                'name': row[1],
                'category': row[2],
                'added_date': row[3],
                'notes': row[4],
            })

        conn.close()

        return favorites

    def get_symbols(self, category: str = None) -> List[str]:
        """Get list of favorite symbols.

        Args:
            category: Category filter (optional)

        Returns:
            List of ticker symbols
        """
        favorites = self.get_all(category=category)
        return [fav['symbol'] for fav in favorites]

    def get_categories(self) -> List[Dict]:
        """Get all categories.

        Returns:
            List of categories with descriptions
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("SELECT name, description, created_date FROM categories ORDER BY name")

        categories = []
        for row in cursor.fetchall():
            # Count stocks in category
            cursor.execute("SELECT COUNT(*) FROM favorites WHERE category = ?", (row[0],))
            count = cursor.fetchone()[0]

            categories.append({
                'name': row[0],
                'description': row[1],
                'created_date': row[2],
                'count': count,
            })

        conn.close()

        return categories

    def create_category(self, name: str, description: str = None) -> bool:
        """Create a new category.

        Args:
            name: Category name
            description: Category description (optional)

        Returns:
            True if created, False if already exists
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        try:
            cursor.execute(
                "INSERT INTO categories (name, description, created_date) VALUES (?, ?, ?)",
                (name.lower(), description, datetime.now().isoformat())
            )
            conn.commit()
            logger.info(f"Created category: {name}")
            return True

        except sqlite3.IntegrityError:
            logger.warning(f"Category '{name}' already exists")
            return False

        finally:
            conn.close()

    def update_category(self, symbol: str, new_category: str) -> bool:
        """Update the category of a favorite stock.

        Args:
            symbol: Stock ticker symbol
            new_category: New category name

        Returns:
            True if updated, False if not found
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute(
            "UPDATE favorites SET category = ? WHERE symbol = ?",
            (new_category.lower(), symbol.upper())
        )
        rows_affected = cursor.rowcount

        conn.commit()
        conn.close()

        if rows_affected > 0:
            logger.info(f"Updated {symbol} category to {new_category}")
            return True
        else:
            logger.warning(f"{symbol} not found in favorites")
            return False

    def export_to_json(self, filepath: str) -> None:
        """Export favorites to JSON file.

        Args:
            filepath: Output file path
        """
        favorites = self.get_all()

        with open(filepath, 'w') as f:
            json.dump({
                'exported_date': datetime.now().isoformat(),
                'favorites': favorites
            }, f, indent=2)

        logger.info(f"Exported {len(favorites)} favorites to {filepath}")

    def import_from_json(self, filepath: str) -> int:
        """Import favorites from JSON file.

        Args:
            filepath: Input file path

        Returns:
            Number of favorites imported
        """
        with open(filepath, 'r') as f:
            data = json.load(f)

        favorites = data.get('favorites', [])
        imported_count = 0

        for fav in favorites:
            if self.add(
                symbol=fav.get('symbol'),
                category=fav.get('category', 'general'),
                name=fav.get('name'),
                notes=fav.get('notes')
            ):
                imported_count += 1

        logger.info(f"Imported {imported_count} favorites from {filepath}")
        return imported_count

    def export_to_csv(self, filepath: str) -> None:
        """Export favorites to CSV file.

        Args:
            filepath: Output file path
        """
        import csv

        favorites = self.get_all()

        with open(filepath, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=['symbol', 'name', 'category', 'added_date', 'notes'])
            writer.writeheader()
            writer.writerows(favorites)

        logger.info(f"Exported {len(favorites)} favorites to {filepath}")


# Global instance
favorites_manager = FavoritesManager()

__all__ = ['FavoritesManager', 'favorites_manager']
