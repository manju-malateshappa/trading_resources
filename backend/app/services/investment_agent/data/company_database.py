"""
Company database with curated lists of AI and high-growth companies
from India, Canada, and USA.

Last Updated: November 2024
"""

from typing import Dict, List
from datetime import datetime


class CompanyDatabase:
    """Database of AI and high-growth companies across markets."""

    def __init__(self):
        """Initialize company database."""
        self.last_updated = "2024-11-09"

        # AI Companies by market
        self.ai_companies = {
            'USA': self._get_usa_ai_companies(),
            'CANADA': self._get_canada_ai_companies(),
            'INDIA': self._get_india_ai_companies(),
        }

        # Other high-growth sectors
        self.sector_companies = {
            'USA': self._get_usa_sector_companies(),
            'CANADA': self._get_canada_sector_companies(),
            'INDIA': self._get_india_sector_companies(),
        }

    def _get_usa_ai_companies(self) -> List[Dict]:
        """Get USA AI companies (2024 updated list)."""
        return [
            # Large Cap AI Leaders
            {'symbol': 'NVDA', 'name': 'NVIDIA Corporation', 'category': 'AI Chips', 'market_cap': 'Large'},
            {'symbol': 'MSFT', 'name': 'Microsoft Corporation', 'category': 'AI Platform', 'market_cap': 'Large'},
            {'symbol': 'GOOGL', 'name': 'Alphabet Inc.', 'category': 'AI Platform', 'market_cap': 'Large'},
            {'symbol': 'META', 'name': 'Meta Platforms', 'category': 'AI Platform', 'market_cap': 'Large'},
            {'symbol': 'AMZN', 'name': 'Amazon.com Inc.', 'category': 'AI Cloud', 'market_cap': 'Large'},
            {'symbol': 'ORCL', 'name': 'Oracle Corporation', 'category': 'AI Cloud', 'market_cap': 'Large'},
            {'symbol': 'AMD', 'name': 'Advanced Micro Devices', 'category': 'AI Chips', 'market_cap': 'Large'},

            # Mid Cap AI Pure Plays
            {'symbol': 'PLTR', 'name': 'Palantir Technologies', 'category': 'AI Analytics', 'market_cap': 'Mid'},
            {'symbol': 'SNOW', 'name': 'Snowflake Inc.', 'category': 'AI Data', 'market_cap': 'Mid'},
            {'symbol': 'DDOG', 'name': 'Datadog Inc.', 'category': 'AI Monitoring', 'market_cap': 'Mid'},
            {'symbol': 'PATH', 'name': 'UiPath Inc.', 'category': 'AI Automation', 'market_cap': 'Mid'},
            {'symbol': 'AI', 'name': 'C3.ai Inc.', 'category': 'AI Platform', 'market_cap': 'Mid'},
            {'symbol': 'SOUN', 'name': 'SoundHound AI', 'category': 'Voice AI', 'market_cap': 'Small'},
            {'symbol': 'BBAI', 'name': 'BigBear.ai Holdings', 'category': 'AI Analytics', 'market_cap': 'Small'},

            # AI Chip & Infrastructure
            {'symbol': 'MRVL', 'name': 'Marvell Technology', 'category': 'AI Chips', 'market_cap': 'Mid'},
            {'symbol': 'ARM', 'name': 'Arm Holdings', 'category': 'AI Chips', 'market_cap': 'Large'},
            {'symbol': 'SMCI', 'name': 'Super Micro Computer', 'category': 'AI Infrastructure', 'market_cap': 'Mid'},
            {'symbol': 'DELL', 'name': 'Dell Technologies', 'category': 'AI Infrastructure', 'market_cap': 'Large'},

            # AI Software & Applications
            {'symbol': 'NOW', 'name': 'ServiceNow Inc.', 'category': 'AI Software', 'market_cap': 'Large'},
            {'symbol': 'CRM', 'name': 'Salesforce Inc.', 'category': 'AI CRM', 'market_cap': 'Large'},
            {'symbol': 'ADBE', 'name': 'Adobe Inc.', 'category': 'AI Creative', 'market_cap': 'Large'},
            {'symbol': 'WDAY', 'name': 'Workday Inc.', 'category': 'AI HR', 'market_cap': 'Mid'},
            {'symbol': 'PEGA', 'name': 'Pegasystems Inc.', 'category': 'AI Automation', 'market_cap': 'Small'},

            # AI Cybersecurity
            {'symbol': 'CRWD', 'name': 'CrowdStrike Holdings', 'category': 'AI Security', 'market_cap': 'Mid'},
            {'symbol': 'PANW', 'name': 'Palo Alto Networks', 'category': 'AI Security', 'market_cap': 'Large'},
            {'symbol': 'ZS', 'name': 'Zscaler Inc.', 'category': 'AI Security', 'market_cap': 'Mid'},
            {'symbol': 'S', 'name': 'SentinelOne Inc.', 'category': 'AI Security', 'market_cap': 'Small'},

            # AI Healthcare
            {'symbol': 'VEEV', 'name': 'Veeva Systems', 'category': 'AI Healthcare', 'market_cap': 'Mid'},
            {'symbol': 'TDOC', 'name': 'Teladoc Health', 'category': 'AI Telehealth', 'market_cap': 'Small'},
            {'symbol': 'DOCS', 'name': 'Doximity Inc.', 'category': 'AI Healthcare', 'market_cap': 'Small'},

            # AI Startups/Emerging (Recently Public)
            {'symbol': 'IONQ', 'name': 'IonQ Inc.', 'category': 'Quantum AI', 'market_cap': 'Small'},
            {'symbol': 'RGTI', 'name': 'Rigetti Computing', 'category': 'Quantum AI', 'market_cap': 'Small'},
            {'symbol': 'GFAI', 'name': 'Guardforce AI', 'category': 'AI Robotics', 'market_cap': 'Small'},
        ]

    def _get_canada_ai_companies(self) -> List[Dict]:
        """Get Canadian AI companies (2024 updated list)."""
        return [
            # Pure AI Companies
            {'symbol': 'DND.TO', 'name': 'DarkVision Technologies', 'category': 'AI Vision', 'market_cap': 'Small'},
            {'symbol': 'NTAR.V', 'name': 'NexTech AR Solutions', 'category': 'AR/AI', 'market_cap': 'Small'},
            {'symbol': 'AIML.CN', 'name': 'AI/ML Innovations', 'category': 'AI Platform', 'market_cap': 'Small'},

            # Tech Companies with Strong AI Focus
            {'symbol': 'SHOP.TO', 'name': 'Shopify Inc.', 'category': 'E-commerce AI', 'market_cap': 'Large'},
            {'symbol': 'LSPD.TO', 'name': 'Lightspeed Commerce', 'category': 'Retail AI', 'market_cap': 'Mid'},
            {'symbol': 'DCBO.TO', 'name': 'Docebo Inc.', 'category': 'Learning AI', 'market_cap': 'Small'},
            {'symbol': 'WELL.TO', 'name': 'WELL Health Technologies', 'category': 'Healthcare AI', 'market_cap': 'Mid'},
            {'symbol': 'DOC.TO', 'name': 'CloudMD Software', 'category': 'Healthcare AI', 'market_cap': 'Small'},

            # AI/Data Analytics
            {'symbol': 'GDNP.TO', 'name': 'Goodfood Market', 'category': 'Food Tech AI', 'market_cap': 'Small'},
            {'symbol': 'TOI.TO', 'name': 'Topicus.com Inc.', 'category': 'Software AI', 'market_cap': 'Mid'},
            {'symbol': 'GSY.TO', 'name': 'goeasy Ltd.', 'category': 'Fintech AI', 'market_cap': 'Mid'},

            # Emerging AI
            {'symbol': 'DM.V', 'name': 'Datametrex AI', 'category': 'AI Analytics', 'market_cap': 'Small'},
            {'symbol': 'EVAN.V', 'name': 'Else Nutrition', 'category': 'Food AI', 'market_cap': 'Small'},
        ]

    def _get_india_ai_companies(self) -> List[Dict]:
        """Get Indian AI companies (2024 updated list)."""
        return [
            # Large Cap Tech with AI
            {'symbol': 'TCS.NS', 'name': 'Tata Consultancy Services', 'category': 'AI Services', 'market_cap': 'Large'},
            {'symbol': 'INFY.NS', 'name': 'Infosys Limited', 'category': 'AI Services', 'market_cap': 'Large'},
            {'symbol': 'WIPRO.NS', 'name': 'Wipro Limited', 'category': 'AI Services', 'market_cap': 'Large'},
            {'symbol': 'TECHM.NS', 'name': 'Tech Mahindra', 'category': 'AI Services', 'market_cap': 'Large'},
            {'symbol': 'HCLTECH.NS', 'name': 'HCL Technologies', 'category': 'AI Services', 'market_cap': 'Large'},
            {'symbol': 'LTI.NS', 'name': 'LTIMindtree', 'category': 'AI Services', 'market_cap': 'Mid'},

            # Mid/Small Cap AI-Focused
            {'symbol': 'PERSISTENT.NS', 'name': 'Persistent Systems', 'category': 'AI Software', 'market_cap': 'Mid'},
            {'symbol': 'COFORGE.NS', 'name': 'Coforge Limited', 'category': 'AI Services', 'market_cap': 'Mid'},
            {'symbol': 'SONATSOFTW.NS', 'name': 'Sonata Software', 'category': 'AI Software', 'market_cap': 'Small'},
            {'symbol': 'LTTS.NS', 'name': 'L&T Technology Services', 'category': 'Engineering AI', 'market_cap': 'Mid'},

            # AI Product Companies
            {'symbol': 'HAPPSTMNDS.NS', 'name': 'Happiest Minds', 'category': 'AI Products', 'market_cap': 'Small'},
            {'symbol': 'ROUTE.NS', 'name': 'Route Mobile', 'category': 'AI Communication', 'market_cap': 'Small'},

            # AI Healthcare/Pharma
            {'symbol': 'METROPOLIS.NS', 'name': 'Metropolis Healthcare', 'category': 'AI Diagnostics', 'market_cap': 'Small'},
            {'symbol': '5PAISA.NS', 'name': '5Paisa Capital', 'category': 'Fintech AI', 'market_cap': 'Small'},

            # Emerging AI (also on BSE)
            {'symbol': 'TATAELXSI.NS', 'name': 'Tata Elxsi', 'category': 'AI Design', 'market_cap': 'Mid'},
            {'symbol': 'CYIENT.NS', 'name': 'Cyient Limited', 'category': 'AI Engineering', 'market_cap': 'Mid'},
        ]

    def _get_usa_sector_companies(self) -> Dict[str, List[Dict]]:
        """Get USA companies by sector (2024 updated)."""
        return {
            'Cloud Computing': [
                {'symbol': 'NET', 'name': 'Cloudflare Inc.', 'market_cap': 'Mid'},
                {'symbol': 'DDOG', 'name': 'Datadog Inc.', 'market_cap': 'Mid'},
                {'symbol': 'MDB', 'name': 'MongoDB Inc.', 'market_cap': 'Mid'},
                {'symbol': 'DOCN', 'name': 'DigitalOcean', 'market_cap': 'Small'},
                {'symbol': 'CFLT', 'name': 'Confluent Inc.', 'market_cap': 'Mid'},
            ],

            'Cybersecurity': [
                {'symbol': 'CRWD', 'name': 'CrowdStrike', 'market_cap': 'Mid'},
                {'symbol': 'ZS', 'name': 'Zscaler', 'market_cap': 'Mid'},
                {'symbol': 'OKTA', 'name': 'Okta Inc.', 'market_cap': 'Mid'},
                {'symbol': 'FTNT', 'name': 'Fortinet', 'market_cap': 'Large'},
            ],

            'Fintech': [
                {'symbol': 'AFRM', 'name': 'Affirm Holdings', 'market_cap': 'Small'},
                {'symbol': 'UPST', 'name': 'Upstart Holdings', 'market_cap': 'Small'},
                {'symbol': 'SOFI', 'name': 'SoFi Technologies', 'market_cap': 'Small'},
                {'symbol': 'COIN', 'name': 'Coinbase Global', 'market_cap': 'Mid'},
                {'symbol': 'SQ', 'name': 'Block Inc.', 'market_cap': 'Mid'},
            ],

            'EV & Clean Energy': [
                {'symbol': 'TSLA', 'name': 'Tesla Inc.', 'market_cap': 'Large'},
                {'symbol': 'RIVN', 'name': 'Rivian Automotive', 'market_cap': 'Mid'},
                {'symbol': 'LCID', 'name': 'Lucid Group', 'market_cap': 'Small'},
                {'symbol': 'ENPH', 'name': 'Enphase Energy', 'market_cap': 'Mid'},
                {'symbol': 'SEDG', 'name': 'SolarEdge Technologies', 'market_cap': 'Small'},
            ],

            'Biotech': [
                {'symbol': 'MRNA', 'name': 'Moderna Inc.', 'market_cap': 'Mid'},
                {'symbol': 'BNTX', 'name': 'BioNTech SE', 'market_cap': 'Mid'},
                {'symbol': 'CRSP', 'name': 'CRISPR Therapeutics', 'market_cap': 'Small'},
                {'symbol': 'BEAM', 'name': 'Beam Therapeutics', 'market_cap': 'Small'},
                {'symbol': 'NTLA', 'name': 'Intellia Therapeutics', 'market_cap': 'Small'},
            ],

            'E-commerce': [
                {'symbol': 'SHOP', 'name': 'Shopify Inc.', 'market_cap': 'Large'},
                {'symbol': 'ETSY', 'name': 'Etsy Inc.', 'market_cap': 'Mid'},
                {'symbol': 'W', 'name': 'Wayfair Inc.', 'market_cap': 'Small'},
                {'symbol': 'CHWY', 'name': 'Chewy Inc.', 'market_cap': 'Mid'},
            ],

            'Gaming': [
                {'symbol': 'RBLX', 'name': 'Roblox Corporation', 'market_cap': 'Mid'},
                {'symbol': 'U', 'name': 'Unity Software', 'market_cap': 'Small'},
                {'symbol': 'TTWO', 'name': 'Take-Two Interactive', 'market_cap': 'Mid'},
            ],
        }

    def _get_canada_sector_companies(self) -> Dict[str, List[Dict]]:
        """Get Canadian companies by sector (2024 updated)."""
        return {
            'Technology': [
                {'symbol': 'SHOP.TO', 'name': 'Shopify Inc.', 'market_cap': 'Large'},
                {'symbol': 'LSPD.TO', 'name': 'Lightspeed Commerce', 'market_cap': 'Mid'},
                {'symbol': 'TOI.TO', 'name': 'Topicus.com', 'market_cap': 'Mid'},
                {'symbol': 'DCBO.TO', 'name': 'Docebo Inc.', 'market_cap': 'Small'},
                {'symbol': 'NVEI.TO', 'name': 'Nuvei Corporation', 'market_cap': 'Mid'},
            ],

            'Healthcare': [
                {'symbol': 'WELL.TO', 'name': 'WELL Health', 'market_cap': 'Mid'},
                {'symbol': 'DOC.TO', 'name': 'CloudMD', 'market_cap': 'Small'},
                {'symbol': 'TDOC', 'name': 'Teladoc Health', 'market_cap': 'Mid'},
            ],

            'Fintech': [
                {'symbol': 'GSY.TO', 'name': 'goeasy Ltd.', 'market_cap': 'Mid'},
                {'symbol': 'NVEI.TO', 'name': 'Nuvei Corp.', 'market_cap': 'Mid'},
            ],

            'Clean Energy': [
                {'symbol': 'NOU.V', 'name': 'Nouveau Monde Graphite', 'market_cap': 'Small'},
                {'symbol': 'HPQ.V', 'name': 'HPQ Silicon', 'market_cap': 'Small'},
                {'symbol': 'SOLR.V', 'name': 'Solarvest BioEnergy', 'market_cap': 'Small'},
            ],

            'Mining & Resources': [
                {'symbol': 'FOOD.V', 'name': 'Good Flour', 'market_cap': 'Small'},
                {'symbol': 'GRSL.V', 'name': 'Grain Discovery', 'market_cap': 'Small'},
            ],

            'Cannabis': [
                {'symbol': 'TLRY', 'name': 'Tilray Brands', 'market_cap': 'Small'},
                {'symbol': 'CGC', 'name': 'Canopy Growth', 'market_cap': 'Small'},
            ],
        }

    def _get_india_sector_companies(self) -> Dict[str, List[Dict]]:
        """Get Indian companies by sector (2024 updated)."""
        return {
            'IT Services': [
                {'symbol': 'TCS.NS', 'name': 'Tata Consultancy Services', 'market_cap': 'Large'},
                {'symbol': 'INFY.NS', 'name': 'Infosys', 'market_cap': 'Large'},
                {'symbol': 'WIPRO.NS', 'name': 'Wipro', 'market_cap': 'Large'},
                {'symbol': 'TECHM.NS', 'name': 'Tech Mahindra', 'market_cap': 'Large'},
                {'symbol': 'HCLTECH.NS', 'name': 'HCL Technologies', 'market_cap': 'Large'},
                {'symbol': 'PERSISTENT.NS', 'name': 'Persistent Systems', 'market_cap': 'Mid'},
                {'symbol': 'COFORGE.NS', 'name': 'Coforge', 'market_cap': 'Mid'},
                {'symbol': 'LTTS.NS', 'name': 'L&T Technology', 'market_cap': 'Mid'},
            ],

            'Fintech & Payments': [
                {'symbol': 'PAYTM.NS', 'name': 'Paytm', 'market_cap': 'Mid'},
                {'symbol': 'POLICYBZR.NS', 'name': 'PB Fintech', 'market_cap': 'Mid'},
                {'symbol': 'NYKAA.NS', 'name': 'Nykaa', 'market_cap': 'Mid'},
                {'symbol': '5PAISA.NS', 'name': '5Paisa Capital', 'market_cap': 'Small'},
            ],

            'E-commerce': [
                {'symbol': 'ZOMATO.NS', 'name': 'Zomato', 'market_cap': 'Mid'},
                {'symbol': 'NYKAA.NS', 'name': 'Nykaa', 'market_cap': 'Mid'},
            ],

            'Pharma & Healthcare': [
                {'symbol': 'SUNPHARMA.NS', 'name': 'Sun Pharmaceutical', 'market_cap': 'Large'},
                {'symbol': 'DRREDDY.NS', 'name': 'Dr. Reddy\'s', 'market_cap': 'Large'},
                {'symbol': 'CIPLA.NS', 'name': 'Cipla', 'market_cap': 'Large'},
                {'symbol': 'LAURUSLABS.NS', 'name': 'Laurus Labs', 'market_cap': 'Mid'},
                {'symbol': 'METROPOLIS.NS', 'name': 'Metropolis Healthcare', 'market_cap': 'Small'},
            ],

            'EV & Auto': [
                {'symbol': 'TATAMOTORS.NS', 'name': 'Tata Motors', 'market_cap': 'Large'},
                {'symbol': 'M&M.NS', 'name': 'Mahindra & Mahindra', 'market_cap': 'Large'},
                {'symbol': 'MOTHERSON.NS', 'name': 'Motherson Sumi', 'market_cap': 'Mid'},
            ],

            'Renewable Energy': [
                {'symbol': 'ADANIGREEN.NS', 'name': 'Adani Green Energy', 'market_cap': 'Large'},
                {'symbol': 'TATAPOWER.NS', 'name': 'Tata Power', 'market_cap': 'Mid'},
                {'symbol': 'SUZLON.NS', 'name': 'Suzlon Energy', 'market_cap': 'Small'},
            ],

            'Infrastructure': [
                {'symbol': 'LT.NS', 'name': 'Larsen & Toubro', 'market_cap': 'Large'},
                {'symbol': 'ADANIPORTS.NS', 'name': 'Adani Ports', 'market_cap': 'Large'},
            ],
        }

    def get_all_ai_companies(self, market: str = None) -> List[Dict]:
        """Get all AI companies, optionally filtered by market.

        Args:
            market: Market filter ('USA', 'CANADA', 'INDIA', or None for all)

        Returns:
            List of AI companies
        """
        if market:
            return self.ai_companies.get(market.upper(), [])

        # Return all AI companies
        all_companies = []
        for market_companies in self.ai_companies.values():
            all_companies.extend(market_companies)
        return all_companies

    def get_companies_by_sector(self, sector: str, market: str = None) -> List[Dict]:
        """Get companies by sector.

        Args:
            sector: Sector name
            market: Market filter ('USA', 'CANADA', 'INDIA', or None for all)

        Returns:
            List of companies in sector
        """
        companies = []

        if market:
            market_sectors = self.sector_companies.get(market.upper(), {})
            return market_sectors.get(sector, [])

        # Search all markets
        for market_sectors in self.sector_companies.values():
            if sector in market_sectors:
                companies.extend(market_sectors[sector])

        return companies

    def get_all_symbols(self, market: str = None) -> List[str]:
        """Get all symbols in database.

        Args:
            market: Market filter ('USA', 'CANADA', 'INDIA', or None for all)

        Returns:
            List of symbols
        """
        symbols = set()

        # Add AI companies
        ai_companies = self.get_all_ai_companies(market)
        symbols.update(c['symbol'] for c in ai_companies)

        # Add sector companies
        if market:
            market_sectors = self.sector_companies.get(market.upper(), {})
            for sector_companies in market_sectors.values():
                symbols.update(c['symbol'] for c in sector_companies)
        else:
            for market_sectors in self.sector_companies.values():
                for sector_companies in market_sectors.values():
                    symbols.update(c['symbol'] for c in sector_companies)

        return sorted(list(symbols))

    def get_company_info(self, symbol: str) -> Dict:
        """Get company info by symbol.

        Args:
            symbol: Stock symbol

        Returns:
            Company information dictionary
        """
        # Search AI companies
        for market, companies in self.ai_companies.items():
            for company in companies:
                if company['symbol'] == symbol:
                    return {**company, 'market': market, 'type': 'AI'}

        # Search sector companies
        for market, sectors in self.sector_companies.items():
            for sector, companies in sectors.items():
                for company in companies:
                    if company['symbol'] == symbol:
                        return {**company, 'market': market, 'sector': sector, 'type': 'Sector'}

        return {}

    def search_companies(self, query: str) -> List[Dict]:
        """Search companies by name or symbol.

        Args:
            query: Search query

        Returns:
            List of matching companies
        """
        query = query.lower()
        matches = []

        # Search all companies
        all_companies = self.get_all_ai_companies()

        for market_sectors in self.sector_companies.values():
            for sector_companies in market_sectors.values():
                all_companies.extend(sector_companies)

        for company in all_companies:
            if (query in company['symbol'].lower() or
                query in company['name'].lower() or
                query in company.get('category', '').lower()):
                matches.append(company)

        return matches


# Global instance
company_db = CompanyDatabase()

__all__ = ['CompanyDatabase', 'company_db']
