"""
Offshore wind energy information sources configuration.

Source categories:
1. Industry Organizations  - GWEC, WindEurope, AWEA/ACP
2. Government & Regulators - BOEM, ACER, Crown Estate, BEIS/DESNZ
3. News & Media            - Recharge News, Windpower Monthly, 4C Offshore
4. Company Announcements   - Vestas, Siemens Gamesa, Orsted, Equinor IR
5. Market Data             - 4C Offshore, BNEF (API), Wood Mackenzie
6. Project Databases       - 4C Offshore, WindEurope project tracker
"""

RSS_SOURCES = [
    # Industry Organizations
    {
        "name": "GWEC",
        "category": "industry_org",
        "url": "https://gwec.net/feed/",
        "language": "en",
    },
    {
        "name": "WindEurope",
        "category": "industry_org",
        "url": "https://windeurope.org/feed/",
        "language": "en",
    },
    {
        "name": "ACP (American Clean Power)",
        "category": "industry_org",
        "url": "https://cleanpower.org/feed/",
        "language": "en",
    },
    # News & Media
    {
        "name": "Recharge News",
        "category": "news_media",
        "url": "https://www.rechargenews.com/rss",
        "language": "en",
    },
    {
        "name": "Windpower Monthly",
        "category": "news_media",
        "url": "https://www.windpowermonthly.com/rss",
        "language": "en",
    },
    {
        "name": "Offshore Wind Biz",
        "category": "news_media",
        "url": "https://www.offshorewind.biz/feed/",
        "language": "en",
    },
    {
        "name": "4C Offshore News",
        "category": "news_media",
        "url": "https://www.4coffshore.com/rss/news.xml",
        "language": "en",
    },
    {
        "name": "NS Energy",
        "category": "news_media",
        "url": "https://www.nsenergybusiness.com/feed/",
        "language": "en",
    },
    {
        "name": "Wind Power Engineering",
        "category": "news_media",
        "url": "https://www.windpowerengineering.com/feed/",
        "language": "en",
    },
    # Chinese sources
    {
        "name": "北极星风力发电网",
        "category": "news_media_cn",
        "url": "https://news.bjx.com.cn/rss/wind.xml",
        "language": "zh",
    },
    {
        "name": "风能专委会",
        "category": "industry_org_cn",
        "url": "https://www.cwea.org.cn/rss/",
        "language": "zh",
    },
    # Company IR
    {
        "name": "Orsted News",
        "category": "company_ir",
        "url": "https://orsted.com/en/rss",
        "language": "en",
    },
    {
        "name": "Vestas News",
        "category": "company_ir",
        "url": "https://www.vestas.com/en/media/rss",
        "language": "en",
    },
    {
        "name": "Siemens Gamesa News",
        "category": "company_ir",
        "url": "https://www.siemensgamesa.com/en-int/newsroom/rss",
        "language": "en",
    },
]

# Web scraping targets (fallback when RSS unavailable)
SCRAPE_SOURCES = [
    {
        "name": "BOEM Offshore Wind",
        "category": "government",
        "url": "https://www.boem.gov/renewable-energy/offshore-wind",
        "selector": "article, .news-item, .press-release",
        "language": "en",
    },
    {
        "name": "Crown Estate News",
        "category": "government",
        "url": "https://www.thecrownestate.co.uk/news-and-media/news/",
        "selector": ".news-listing__item",
        "language": "en",
    },
    {
        "name": "DESNZ Offshore Wind",
        "category": "government",
        "url": "https://www.gov.uk/government/collections/offshore-wind-energy",
        "selector": ".gem-c-document-list__item",
        "language": "en",
    },
]

# Google News search queries for targeted collection
GOOGLE_NEWS_QUERIES = [
    "offshore wind farm contract award",
    "offshore wind auction results",
    "海上风电 中标 开标",
    "offshore wind CfD AR8 AR7",
    "offshore wind policy regulation 2025",
    "Orsted Equinor offshore wind project update",
    "Vestas Siemens Gamesa offshore wind order",
    "offshore wind installation vessel",
    "海上风电 装机容量 招标",
    "offshore wind financial investment decision FID",
]
