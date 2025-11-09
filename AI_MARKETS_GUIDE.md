# AI Companies & Multi-Market Guide 🤖🌍

Complete guide to screening AI companies and markets from India, Canada, and USA.

## 📊 Market Coverage

The Investment Agent now includes comprehensive coverage of:

### 🇺🇸 USA Markets
- **NASDAQ**: Technology-focused exchange
- **NYSE**: New York Stock Exchange
- **AI Companies**: 30+ companies (NVIDIA, Palantir, C3.ai, CrowdStrike, etc.)
- **Sectors**: Cloud Computing, Cybersecurity, Fintech, EV, Biotech, E-commerce

### 🇨🇦 Canada Markets
- **TSX**: Toronto Stock Exchange
- **TSXV**: TSX Venture Exchange
- **AI Companies**: 12+ companies (Shopify, Lightspeed, WELL Health, etc.)
- **Sectors**: Technology, Healthcare, Fintech, Clean Energy, Cannabis

### 🇮🇳 India Markets
- **NSE**: National Stock Exchange (Primary)
- **BSE**: Bombay Stock Exchange
- **AI Companies**: 16+ companies (TCS, Infosys, Wipro, Tech Mahindra, etc.)
- **Sectors**: IT Services, Fintech & Payments, E-commerce, Pharma, EV & Auto

## 🤖 AI Companies Database

### USA AI Companies (30+)

**Large Cap AI Leaders:**
- NVDA - NVIDIA Corporation (AI Chips)
- MSFT - Microsoft Corporation (AI Platform)
- GOOGL - Alphabet Inc. (AI Platform)
- META - Meta Platforms (AI Platform)
- AMZN - Amazon.com Inc. (AI Cloud)
- ORCL - Oracle Corporation (AI Cloud)
- AMD - Advanced Micro Devices (AI Chips)

**Mid/Small Cap AI Pure Plays:**
- PLTR - Palantir Technologies (AI Analytics)
- SNOW - Snowflake Inc. (AI Data)
- DDOG - Datadog Inc. (AI Monitoring)
- PATH - UiPath Inc. (AI Automation)
- AI - C3.ai Inc. (AI Platform)
- SOUN - SoundHound AI (Voice AI)
- BBAI - BigBear.ai Holdings (AI Analytics)

**AI Chip & Infrastructure:**
- MRVL - Marvell Technology (AI Chips)
- ARM - Arm Holdings (AI Chips)
- SMCI - Super Micro Computer (AI Infrastructure)
- DELL - Dell Technologies (AI Infrastructure)

**AI Cybersecurity:**
- CRWD - CrowdStrike Holdings (AI Security)
- PANW - Palo Alto Networks (AI Security)
- ZS - Zscaler Inc. (AI Security)
- S - SentinelOne Inc. (AI Security)

**Emerging AI:**
- IONQ - IonQ Inc. (Quantum AI)
- RGTI - Rigetti Computing (Quantum AI)

### Canada AI Companies (12+)

**AI-Focused:**
- SHOP.TO - Shopify Inc. (E-commerce AI)
- LSPD.TO - Lightspeed Commerce (Retail AI)
- DCBO.TO - Docebo Inc. (Learning AI)
- WELL.TO - WELL Health Technologies (Healthcare AI)
- DOC.TO - CloudMD Software (Healthcare AI)
- TOI.TO - Topicus.com Inc. (Software AI)

**Emerging:**
- NTAR.V - NexTech AR Solutions (AR/AI)
- DM.V - Datametrex AI (AI Analytics)

### India AI Companies (16+)

**Large Cap IT Services with AI:**
- TCS.NS - Tata Consultancy Services (AI Services)
- INFY.NS - Infosys Limited (AI Services)
- WIPRO.NS - Wipro Limited (AI Services)
- TECHM.NS - Tech Mahindra (AI Services)
- HCLTECH.NS - HCL Technologies (AI Services)
- LTI.NS - LTIMindtree (AI Services)

**Mid/Small Cap AI-Focused:**
- PERSISTENT.NS - Persistent Systems (AI Software)
- COFORGE.NS - Coforge Limited (AI Services)
- SONATSOFTW.NS - Sonata Software (AI Software)
- LTTS.NS - L&T Technology Services (Engineering AI)
- HAPPSTMNDS.NS - Happiest Minds (AI Products)
- TATAELXSI.NS - Tata Elxsi (AI Design)
- CYIENT.NS - Cyient Limited (AI Engineering)

## 📋 New CLI Commands

### Scan All AI Companies

```bash
# Scan all AI companies from all markets
python main.py ai

# Scan AI companies from specific market
python main.py ai --market USA
python main.py ai --market CANADA
python main.py ai --market INDIA

# Scan AI companies with minimum score
python main.py ai --market USA --min-score 70
```

### Scan by Sector

```bash
# Scan Fintech companies
python main.py sector Fintech

# Scan Cloud Computing companies
python main.py sector "Cloud Computing"

# Scan EV & Clean Energy companies
python main.py sector "EV & Clean Energy" --market USA

# Scan IT Services in India
python main.py sector "IT Services" --market INDIA
```

### Scan by Market

```bash
# Scan Indian market (NSE)
python main.py india
python main.py india --min-score 70

# Scan Canadian market (TSX)
python main.py canada
python main.py canada --min-score 65

# Scan US market (NASDAQ, NYSE)
python main.py us
python main.py us --min-score 75
```

### Analyze Indian Stocks

```bash
# Analyze Indian stocks (use .NS suffix for NSE)
python main.py analyze TCS.NS
python main.py analyze INFY.NS
python main.py analyze PERSISTENT.NS

# Evaluate buying Indian stocks
python main.py buy TCS.NS
python main.py buy HAPPSTMNDS.NS
```

## 💻 Python API Examples

### Screen AI Companies

```python
from investment_agent.agent import InvestmentAgent

agent = InvestmentAgent()

# Scan all AI companies
all_ai = agent.stock_screener.screen_ai_companies()

# Scan USA AI companies
us_ai = agent.stock_screener.screen_ai_companies(market='USA', min_score=70)

# Scan India AI companies
india_ai = agent.stock_screener.screen_ai_companies(market='INDIA', min_score=65)

# Scan Canada AI companies
canada_ai = agent.stock_screener.screen_ai_companies(market='CANADA', min_score=65)
```

### Screen by Sector

```python
# Screen Fintech companies
fintech = agent.stock_screener.screen_sector('Fintech')

# Screen Cloud Computing companies in USA
cloud = agent.stock_screener.screen_sector('Cloud Computing', market='USA')

# Screen IT Services in India
it_services = agent.stock_screener.screen_sector('IT Services', market='INDIA')

# Screen Clean Energy companies
clean_energy = agent.stock_screener.screen_sector('Clean Energy', min_score=70)
```

### Screen by Market

```python
# Screen Indian market
indian_stocks = agent.stock_screener.screen_indian_market(min_score=65)

# Screen Canadian market
canadian_stocks = agent.stock_screener.screen_canadian_market(min_score=70)

# Screen US market
us_stocks = agent.stock_screener.screen_us_market(min_score=75)
```

### Analyze Specific Stocks

```python
# Analyze USA AI stock
nvidia_analysis = agent.analyze_stock('NVDA')

# Analyze Canadian AI stock
shopify_analysis = agent.analyze_stock('SHOP.TO')

# Analyze Indian AI stock
tcs_analysis = agent.analyze_stock('TCS.NS')
infosys_analysis = agent.analyze_stock('INFY.NS')
```

## 🎯 Available Sectors

### USA Sectors
- **Cloud Computing**: NET, DDOG, MDB, DOCN, CFLT
- **Cybersecurity**: CRWD, ZS, OKTA, FTNT
- **Fintech**: AFRM, UPST, SOFI, COIN, SQ
- **EV & Clean Energy**: TSLA, RIVN, LCID, ENPH, SEDG
- **Biotech**: MRNA, BNTX, CRSP, BEAM, NTLA
- **E-commerce**: SHOP, ETSY, W, CHWY
- **Gaming**: RBLX, U, TTWO

### Canada Sectors
- **Technology**: SHOP.TO, LSPD.TO, TOI.TO, DCBO.TO, NVEI.TO
- **Healthcare**: WELL.TO, DOC.TO
- **Fintech**: GSY.TO, NVEI.TO
- **Clean Energy**: NOU.V, HPQ.V, SOLR.V
- **Cannabis**: TLRY, CGC

### India Sectors
- **IT Services**: TCS.NS, INFY.NS, WIPRO.NS, TECHM.NS, HCLTECH.NS
- **Fintech & Payments**: PAYTM.NS, POLICYBZR.NS, NYKAA.NS, 5PAISA.NS
- **E-commerce**: ZOMATO.NS, NYKAA.NS
- **Pharma & Healthcare**: SUNPHARMA.NS, DRREDDY.NS, CIPLA.NS, LAURUSLABS.NS
- **EV & Auto**: TATAMOTORS.NS, M&M.NS, MOTHERSON.NS
- **Renewable Energy**: ADANIGREEN.NS, TATAPOWER.NS, SUZLON.NS
- **Infrastructure**: LT.NS, ADANIPORTS.NS

## 🌟 Special Features

### 1. AI-Specific Analysis

The agent understands AI company categories:
- **AI Chips**: NVIDIA, AMD, ARM
- **AI Platform**: Palantir, C3.ai, Microsoft, Google
- **AI Software**: ServiceNow, Salesforce, Adobe
- **AI Services**: TCS, Infosys, Wipro, Accenture
- **AI Security**: CrowdStrike, SentinelOne, Zscaler
- **AI Healthcare**: Veeva, Doximity, Teladoc

### 2. Market-Specific Understanding

**Indian Market Support:**
- Automatic .NS suffix handling for NSE stocks
- Support for .BO suffix for BSE stocks
- Indian IT services focus
- Fintech and digital payment companies

**Canadian Market Support:**
- .TO suffix for TSX stocks
- .V suffix for TSXV stocks
- Focus on tech and healthcare growth

**USA Market Support:**
- NASDAQ and NYSE coverage
- Comprehensive AI and tech coverage
- Sector diversification

### 3. Currency Handling

The agent automatically handles different currencies:
- **USA**: USD
- **Canada**: CAD
- **India**: INR

Note: All analyses are done in local currency. Compare valuations carefully across markets.

## 📈 Example Workflows

### Daily AI Stock Scan

```bash
# Morning routine
python main.py ai --market USA --min-score 70
python main.py ai --market CANADA --min-score 65
python main.py ai --market INDIA --min-score 65

# Or using Python
agent = InvestmentAgent()
us_ai = agent.stock_screener.screen_ai_companies(market='USA')
canada_ai = agent.stock_screener.screen_ai_companies(market='CANADA')
india_ai = agent.stock_screener.screen_ai_companies(market='INDIA')
```

### Sector Deep Dive

```bash
# Analyze Fintech across all markets
python main.py sector Fintech

# Focus on specific market
python main.py sector "IT Services" --market INDIA
python main.py sector "Cloud Computing" --market USA
```

### Market Comparison

```python
# Compare markets
indian_stocks = agent.stock_screener.screen_indian_market()
canadian_stocks = agent.stock_screener.screen_canadian_market()
us_stocks = agent.stock_screener.screen_us_market()

# Compare AI companies across markets
us_ai = agent.stock_screener.screen_ai_companies(market='USA')
india_ai = agent.stock_screener.screen_ai_companies(market='INDIA')
canada_ai = agent.stock_screener.screen_ai_companies(market='CANADA')
```

## 🔍 Finding Specific Companies

```python
from investment_agent.data import company_db

# Search for companies
results = company_db.search_companies('shopify')
results = company_db.search_companies('tata')
results = company_db.search_companies('nvidia')

# Get company info
nvidia_info = company_db.get_company_info('NVDA')
tcs_info = company_db.get_company_info('TCS.NS')
shopify_info = company_db.get_company_info('SHOP.TO')

# Get all symbols from a market
usa_symbols = company_db.get_all_symbols(market='USA')
india_symbols = company_db.get_all_symbols(market='INDIA')
canada_symbols = company_db.get_all_symbols(market='CANADA')
```

## 🎯 Best Practices

### For AI Stocks
1. Focus on revenue growth and AI adoption metrics
2. Monitor competitive advantages (moat)
3. Track R&D spending as % of revenue
4. Watch for regulatory risks
5. Consider market positioning

### For Indian Stocks
1. Check ADR availability for liquidity
2. Monitor rupee exchange rates
3. Consider tax implications
4. Watch for quarterly results
5. Track FII/DII data

### For Canadian Stocks
1. Monitor commodity prices (materials sector)
2. Consider USD/CAD exchange rates
3. Watch for cross-listings
4. Track resource-related stocks carefully

### For US Stocks
1. Monitor Fed policy and interest rates
2. Watch sector rotation
3. Track institutional ownership
4. Consider market cap categories
5. Monitor earnings seasons

## ⚠️ Important Notes

1. **Exchange Suffixes**:
   - Indian NSE: Add `.NS` (e.g., TCS.NS)
   - Indian BSE: Add `.BO` (e.g., TCS.BO)
   - Canadian TSX: Add `.TO` (e.g., SHOP.TO)
   - Canadian TSXV: Add `.V` (e.g., NOU.V)
   - US stocks: No suffix needed

2. **Market Hours**:
   - NSE: 9:15 AM - 3:30 PM IST
   - TSX: 9:30 AM - 4:00 PM EST
   - NASDAQ/NYSE: 9:30 AM - 4:00 PM EST

3. **Data Availability**:
   - Indian stocks may have less analyst coverage
   - Canadian small-caps may have lower liquidity
   - Use .NS for better data availability than .BO

4. **Tax Considerations**:
   - Different tax rules apply for each country
   - Capital gains tax varies by country
   - Consult tax professional for cross-border investing

## 📊 Quick Reference

```bash
# AI Companies
python main.py ai                           # All AI companies
python main.py ai --market USA             # US AI companies
python main.py ai --market INDIA           # Indian AI companies
python main.py ai --market CANADA          # Canadian AI companies

# Sectors
python main.py sector Fintech              # All Fintech
python main.py sector "IT Services" --market INDIA

# Markets
python main.py india                       # Indian market
python main.py canada                      # Canadian market
python main.py us                          # US market

# Analysis
python main.py analyze TCS.NS              # Indian stock
python main.py analyze SHOP.TO             # Canadian stock
python main.py analyze NVDA                # US stock
```

## 🚀 What's New

✅ 200+ companies added across India, Canada, USA
✅ AI-specific company database with 50+ AI companies
✅ Sector-based screening (10+ sectors)
✅ Market-specific screening (NSE, BSE, TSX, NASDAQ, NYSE)
✅ Indian market support with .NS/.BO handling
✅ Enhanced CLI with new commands
✅ Updated configuration for multi-market support

---

**Ready to explore AI companies and global markets! 🌍🤖📈**
