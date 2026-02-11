# Portfolio Analysis - Quick Guide

## Overview

The portfolio analysis feature allows you to analyze multiple stocks together and get portfolio-level recommendations including allocation percentages, diversification assessment, and comparative rankings.

## Usage

### Option 1: Interactive CLI

```bash
python main_portfolio.py
```

Follow the prompts:
1. Choose mode (1 = Single Stock, 2 = Portfolio)
2. Enter stock tickers separated by commas
3. Enter portfolio size (default: $100,000)
4. Choose parallel processing (y/n)

### Option 2: Programmatic

```python
from stock_research_crew.portfolio_analyzer import PortfolioAnalyzer

# Create analyzer
analyzer = PortfolioAnalyzer(
    stocks=["AAPL", "GOOGL", "MSFT"],
    portfolio_size=100000
)

# Generate full report
report = analyzer.generate_full_report(parallel=True)

# Access results
for stock, analysis in report["individual_analyses"].items():
    print(f"\n{stock}:\n{analysis}")

print(f"\nPortfolio Analysis:\n{report['portfolio_analysis']}")
```

## Features

### 1. Individual Stock Analysis
- Each stock gets a complete analysis (research, fundamentals, risks, decision)
- Results are cached for faster subsequent runs
- Parallel processing option for faster batch analysis

### 2. Comparative Analysis
- Ranks stocks by overall score
- Compares business quality, growth, valuation, risk
- Identifies best stock for growth, stability, value
- Highlights sector concentration

### 3. Portfolio Allocation
- Recommends percentage allocation for each stock
- Calculates dollar amounts based on portfolio size
- Provides rationale for each allocation
- Identifies core vs satellite holdings

### 4. Diversification Assessment
- Sector diversification score (0-100)
- Risk diversification score (0-100)
- Overall portfolio balance rating
- Concentration risk warnings

## Example Output

```
============================================================
PORTFOLIO ANALYSIS & ALLOCATION
============================================================

COMPARATIVE RANKINGS:
1. AAPL - Score: 86/100 (BUY) - Strong fundamentals, ecosystem moat
2. MSFT - Score: 82/100 (BUY) - Cloud growth, enterprise strength
3. GOOGL - Score: 78/100 (BUY) - Ad dominance, AI potential

RECOMMENDED ALLOCATION ($100,000 portfolio):
┌────────┬────────┬───────────┬─────────────────────────────┐
│ Stock  │   %    │  Amount   │ Rationale                   │
├────────┼────────┼───────────┼─────────────────────────────┤
│ AAPL   │  35%   │ $35,000   │ Core holding, best score    │
│ MSFT   │  35%   │ $35,000   │ Core holding, cloud growth  │
│ GOOGL  │  30%   │ $30,000   │ Satellite, growth potential │
└────────┴────────┴───────────┴─────────────────────────────┘

DIVERSIFICATION SCORES:
- Sector Diversification: 65/100 (Tech-heavy, consider other sectors)
- Risk Diversification: 78/100 (Good balance)
- Overall Balance: Well-balanced with growth focus

PORTFOLIO RISK: Medium
- All three stocks are in technology sector
- High correlation during market downturns
- Consider adding non-tech stocks for better diversification

FINAL RECOMMENDATION: Yes, well-balanced portfolio
Strengths:
- All stocks have strong fundamentals and BUY ratings
- Good mix of established (AAPL, MSFT) and growth (GOOGL)
- Reasonable allocation spreads risk

Weaknesses:
- Heavy tech concentration (100%)
- Correlated performance during sector downturns
- No defensive or value stocks

Suggested Improvements:
- Add 1-2 stocks from different sectors (healthcare, consumer staples)
- Consider reducing tech exposure to 60-70% of portfolio
- Add a defensive stock for downside protection
============================================================
```

## Tips

1. **Start with 3-5 stocks** - More stocks = longer analysis time
2. **Use parallel processing** - Faster for 3+ stocks
3. **Check cache** - Cached stocks analyze instantly
4. **Diversify sectors** - Mix tech, healthcare, finance, etc.
5. **Review allocation** - Adjust based on your risk tolerance

## Performance

- **Single stock**: ~2-3 minutes (first run), instant (cached)
- **3 stocks (sequential)**: ~6-9 minutes (first run)
- **3 stocks (parallel)**: ~3-4 minutes (first run)
- **Portfolio analysis**: ~1-2 minutes additional

## Limitations

- Analysis is qualitative, not based on real-time data
- Recommendations are educational, not financial advice
- LLM quality depends on the model used (mistral, llama3.1, etc.)
- No real-time price data or technical indicators

## Next Steps

1. Run `python main_portfolio.py` to try it
2. Start with 2-3 stocks you're interested in
3. Review individual analyses first
4. Check portfolio allocation recommendations
5. Adjust your actual portfolio based on your research

---

**Remember**: This is educational software. Always do your own research and consult with financial advisors before making investment decisions.
