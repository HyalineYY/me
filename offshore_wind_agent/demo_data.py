"""Sample data with pre-written analysis for demo mode (no API key needed)."""

DEMO_ITEMS = [
    {
        "source_name": "Offshore Wind Biz",
        "source_category": "news_media",
        "language": "en",
        "title": "UK AR8 CfD Auction Brought Forward to July 2025, DESNZ Confirms",
        "url": "https://www.offshorewind.biz/2025/06/09/uk-ar8-cfd-auction-brought-forward/",
        "summary": (
            "The UK Department for Energy Security and Net Zero (DESNZ) has confirmed "
            "the Allocation Round 8 (AR8) Contracts for Difference auction will open in "
            "July 2025, two months ahead of the previously indicated September timeline. "
            "The administrative strike price for offshore wind remains under discussion, "
            "but industry sources suggest it will be set above £80/MWh to attract sufficient bids."
        ),
        "raw_content": "",
        "published_at": "2025-06-09T10:00:00+00:00",
        "analysis": {
            "title_cn": "英国AR8海上风电CfD拍卖提前至2025年7月开标",
            "core_content": (
                "英国能源安全与净零部（DESNZ）确认，第8轮差价合约（AR8）拍卖将于2025年7月开标，"
                "较此前预告的9月时间表提前约2个月。"
                "行政执行价格预计将设定在£80/MWh以上，以吸引足够的投标方参与。"
            ),
            "impact_analysis": (
                "【动态对比】此前市场预期AR8于9月开标，此次确认提前至7月，进度超预期。\n"
                "影响维度：政策/市场情绪｜影响方向：利好｜影响程度：重大\n"
                "开标提前意味着英国政府加快海上风电扩容节奏，有助于改善行业订单能见度；"
                "对Orsted、SSE Renewables等开发商及Vestas、Siemens Gamesa等整机商短期情绪提振显著。"
            ),
            "value_note": "AR8是欧洲近期最大单次海上风电拍卖，结果直接影响全球海上风电订单格局。",
            "tags": ["英国CfD", "AR8", "政策", "拍卖时间表", "利好"],
            "value_score": 5,
        },
    },
    {
        "source_name": "GWEC",
        "source_category": "industry_org",
        "language": "en",
        "title": "GWEC Report: Fast-Track Offshore Wind To Help Prevent Future Energy Crises",
        "url": "https://gwec.net/gwec-report-fast-track-offshore-wind/",
        "summary": (
            "The Global Wind Energy Council (GWEC) has released a new report urging governments "
            "to accelerate offshore wind deployment as a key measure to prevent future energy supply "
            "crises. The report calls for streamlined permitting, stronger CfD frameworks, and "
            "long-term capacity auctions. GWEC estimates that doubling the current global offshore "
            "wind pipeline could reduce household energy costs by 15-20% by 2035."
        ),
        "raw_content": "",
        "published_at": "2025-06-08T08:00:00+00:00",
        "analysis": {
            "title_cn": "GWEC报告：加速海上风电部署可防范未来能源危机",
            "core_content": (
                "全球风能理事会（GWEC）发布报告，呼吁各国政府加快海上风电审批和部署，"
                "以增强能源安全韧性。"
                "报告测算，若全球海上风电管道规模翻倍，至2035年可将家庭能源成本降低15-20%。"
            ),
            "impact_analysis": (
                "影响维度：行业长期增长动力/市场情绪｜影响方向：利好｜影响程度：一般\n"
                "GWEC报告代表行业组织对政策加速的集体诉求，具有舆论引导价值，"
                "但短期内对估值影响有限；长期来看有助于强化各国政策制定者的支持意愿。"
            ),
            "value_note": "反映行业组织对政策加速的预期，有助于判断行业长期增长动力。",
            "tags": ["GWEC", "行业报告", "政策倡导", "能源安全"],
            "value_score": 3,
        },
    },
    {
        "source_name": "Recharge News",
        "source_category": "news_media",
        "language": "en",
        "title": "Orsted Takes FID on 1.3GW Hornsea 4 After Revised Government Support Agreement",
        "url": "https://www.rechargenews.com/wind/orsted-fid-hornsea-4/",
        "summary": (
            "Orsted has reached Final Investment Decision (FID) on the 1.3GW Hornsea 4 offshore "
            "wind project off the Yorkshire coast after securing a revised contract agreement with "
            "the UK government. The project had previously been shelved in 2023 due to supply chain "
            "inflation. The revised strike price of £87/MWh (2012 prices) represents a 22% uplift "
            "from the original AR4 contract. Total capex is estimated at £4.8bn."
        ),
        "raw_content": "",
        "published_at": "2025-06-07T14:30:00+00:00",
        "analysis": {
            "title_cn": "Orsted宣布Hornsea 4（1.3GW）最终投资决定，修订后电价上调22%",
            "core_content": (
                "Orsted对1.3GW的Hornsea 4项目作出最终投资决定（FID），"
                "修订后差价合约执行价格为£87/MWh（2012年价格），较原AR4合同上调22%，总资本支出约£48亿。"
                "该项目此前因供应链通胀于2023年被搁置。"
            ),
            "impact_analysis": (
                "【动态对比】Hornsea 4于2023年被搁置，此次FID标志项目重启，且电价谈判结果超出原有合同水平。\n"
                "影响维度：业绩/估值｜影响方向：利好｜影响程度：重大\n"
                "对Orsted：直接增厚业绩管线，缓解市场对其项目取消率过高的担忧，估值修复逻辑强化；"
                "对供应链：1.3GW规模项目落地，带动整机、基础、海缆订单，对Vestas/Siemens Gamesa订单展望积极。"
            ),
            "value_note": "标志性大型项目重启，是欧洲海上风电景气度回升的关键信号。",
            "tags": ["Orsted", "Hornsea 4", "FID", "英国", "项目重启", "利好"],
            "value_score": 5,
        },
    },
    {
        "source_name": "北极星风力发电网",
        "source_category": "news_media_cn",
        "language": "zh",
        "title": "广东省2025年海上风电竞配结果公示：总规模达500万千瓦",
        "url": "https://news.bjx.com.cn/html/20250608/offshore-wind-guangdong.shtml",
        "summary": (
            "广东省能源局公示2025年海上风电项目竞争性配置结果，共核准8个项目，"
            "总装机规模500万千瓦（5GW）。其中明阳智能获批2个项目共120万千瓦，"
            "金风科技获批1个项目60万千瓦，三峡能源获批2个项目140万千瓦。"
            "项目要求在2027年底前完成全容量并网，补贴采用省级财政专项补贴机制。"
        ),
        "raw_content": "",
        "published_at": "2025-06-08T09:00:00+00:00",
        "analysis": {
            "title_cn": "广东省2025年海上风电5GW竞配结果出炉，明阳/金风/三峡中标",
            "core_content": (
                "广东省2025年海上风电竞配完成，共核准8个项目5GW，"
                "明阳智能（1.2GW）、三峡能源（1.4GW）、金风科技（0.6GW）等头部企业中标。"
                "省补机制确定，要求2027年底前全容量并网。"
            ),
            "impact_analysis": (
                "影响维度：行业数据/业绩/订单｜影响方向：利好｜影响程度：重大\n"
                "广东作为全国海上风电第一大省，5GW单次竞配规模创近年新高，"
                "直接利好明阳智能（整机+开发双受益）、三峡能源（开发）；"
                "省补机制落地消除政策不确定性，加速行业开工节奏，"
                "带动海缆（东方电缆、中天科技）、桩基（海力风电）等供应链订单释放。"
            ),
            "value_note": "广东5GW落地是2025年国内海上风电装机目标实现的关键支撑。",
            "tags": ["广东", "竞配", "5GW", "明阳智能", "三峡能源", "金风科技", "省补", "国内政策"],
            "value_score": 5,
        },
    },
    {
        "source_name": "Windpower Monthly",
        "source_category": "news_media",
        "language": "en",
        "title": "Vestas Secures 820MW Offshore Wind Turbine Order for German North Sea Project",
        "url": "https://www.windpowermonthly.com/vestas-820mw-germany-offshore/",
        "summary": (
            "Vestas has secured a firm order for 820MW of V236-15MW offshore wind turbines "
            "for an unnamed German North Sea project. The order includes a 30-year service agreement. "
            "Delivery is scheduled for 2027-2028. The deal brings Vestas year-to-date offshore "
            "order intake to 3.2GW, ahead of analyst consensus of 2.8GW for H1 2025."
        ),
        "raw_content": "",
        "published_at": "2025-06-06T11:00:00+00:00",
        "analysis": {
            "title_cn": "Vestas获得德国北海820MW海上风机订单，H1订单量超分析师预期",
            "core_content": (
                "Vestas获得德国北海820MW V236-15MW海上风机订单（含30年服务合同），"
                "预计2027-2028年交付。"
                "至此Vestas年初至今海上订单量达3.2GW，超出分析师H1共识预期2.8GW。"
            ),
            "impact_analysis": (
                "影响维度：业绩/估值｜影响方向：利好｜影响程度：重大\n"
                "订单量超预期直接支撑Vestas业绩展望，且服务合同提供长期稳定现金流；"
                "V236-15MW机型放量验证大兆瓦机组商业化进程，对行业降本预期有积极信号；"
                "对竞争对手Siemens Gamesa（SGRE）构成间接压力。"
            ),
            "value_note": "Vestas订单超预期是海上风电景气度的核心量化指标之一。",
            "tags": ["Vestas", "订单", "德国", "V236-15MW", "超预期", "利好"],
            "value_score": 4,
        },
    },
    {
        "source_name": "4C Offshore News",
        "source_category": "news_media",
        "language": "en",
        "title": "Taiwan Offshore Wind Round 3 Results: 3GW Awarded Across Six Projects",
        "url": "https://www.4coffshore.com/news/taiwan-round3-results/",
        "summary": (
            "Taiwan's Bureau of Energy has announced Round 3 offshore wind capacity allocation "
            "results, awarding 3GW across six projects. Ørsted (600MW), Swancor Renewable (500MW), "
            "and Corio Generation (500MW) were among the winners. Local content requirements "
            "have been raised to 60% for turbine nacelles and 80% for foundations."
        ),
        "raw_content": "",
        "published_at": "2025-06-05T06:00:00+00:00",
        "analysis": {
            "title_cn": "台湾第三轮海上风电3GW竞配结果公布，本土化要求大幅提升",
            "core_content": (
                "台湾能源局公布第三轮海上风电竞配结果，共授予6个项目3GW；"
                "Orsted（600MW）、Swancor（500MW）等获批。"
                "机舱本土化率要求提升至60%，基础本土化率提升至80%。"
            ),
            "impact_analysis": (
                "影响维度：行业数据/供应链/市场情绪｜影响方向：中性偏积极｜影响程度：一般\n"
                "台湾市场3GW落地总量符合预期，但本土化率大幅提升对外资整机商（Vestas/SGRE）进入门槛构成约束；"
                "对台湾本土风电设备商（上纬新能源、台船重工）是明显利好；"
                "对中国出海整机商竞争台湾市场形成额外壁垒。"
            ),
            "value_note": "亚太区海上风电重要市场，本土化政策走向值得持续追踪。",
            "tags": ["台湾", "第三轮竞配", "3GW", "本土化", "Orsted", "供应链"],
            "value_score": 4,
        },
    },
    {
        "source_name": "Google News: offshore wind CfD AR7",
        "source_category": "search",
        "language": "en",
        "title": "UK AR7 Strike Price Confirmed at £131/MWh, 31% Above Original Budget Estimate",
        "url": "https://www.rechargenews.com/wind/ar7-strike-price-confirmed/",
        "summary": (
            "The UK government has confirmed the AR7 Contracts for Difference strike price at "
            "£131/MWh (2012 prices), which is 31% above the original £100/MWh budget estimate "
            "published in January 2025. The uplift reflects persistent supply chain inflation "
            "and higher financing costs. Total AR7 offshore wind capacity awarded stands at 4.9GW."
        ),
        "raw_content": "",
        "published_at": "2025-06-04T16:00:00+00:00",
        "analysis": {
            "title_cn": "英国AR7执行电价确认£131/MWh，较年初预算估算超出31%",
            "core_content": (
                "英国政府确认AR7差价合约执行价格为£131/MWh（2012年价格），"
                "较2025年1月公布的£100/MWh预算估算高出31%，反映供应链通胀和融资成本压力；"
                "AR7共授权4.9GW海上风电容量。"
            ),
            "impact_analysis": (
                "【动态对比】2025年1月预期补贴£100/MWh，最终确认£131/MWh，超预期幅度达31%——对行业是重大利好。\n"
                "影响维度：政策/估值/业绩｜影响方向：利好｜影响程度：重大\n"
                "更高的执行价格直接改善项目IRR，增强开发商和整机商盈利预期；"
                "同时向市场发出信号：英国政府愿意为海上风电提供足够经济激励，"
                "有助于提振AR8及后续轮次的投资信心和出价积极性。"
            ),
            "value_note": "典型的'超预期利好'案例，须与1月原始预算对比方能体现其价值。",
            "tags": ["英国CfD", "AR7", "执行电价", "超预期", "利好", "政策"],
            "value_score": 5,
        },
    },
    {
        "source_name": "NS Energy",
        "source_category": "news_media",
        "language": "en",
        "title": "Siemens Gamesa Secures Monopile Supply Deal With Steelwind Nordenham for 2026-2028",
        "url": "https://www.nsenergybusiness.com/siemens-gamesa-monopile-steelwind/",
        "summary": (
            "Siemens Gamesa has signed a multi-year monopile supply agreement with German "
            "manufacturer Steelwind Nordenham for projects scheduled for installation in 2026-2028. "
            "The deal is valued at approximately €600m and covers around 120 monopiles. "
            "This alleviates previous concerns about foundation bottlenecks in the European offshore supply chain."
        ),
        "raw_content": "",
        "published_at": "2025-06-03T13:00:00+00:00",
        "analysis": {
            "title_cn": "西门子歌美飒与Steelwind签订€6亿单桩供货协议，缓解基础设施供应链瓶颈",
            "core_content": (
                "西门子歌美飒（SGRE）与德国Steelwind Nordenham签署多年期单桩供货协议，"
                "涵盖约120根单桩，合同金额约€6亿，供货周期2026-2028年。"
                "此举有效缓解市场对欧洲近海基础设施供应瓶颈的担忧。"
            ),
            "impact_analysis": (
                "影响维度：供应链/业绩｜影响方向：利好｜影响程度：一般\n"
                "供应链确定性提升，有助于SGRE锁定项目交付时间表，降低工程延期风险；"
                "单桩供应瓶颈是欧洲海上风电装机节奏的核心制约之一，"
                "本协议落地是行业供应链修复的积极信号，对行业整体进度预期有正面影响。"
            ),
            "value_note": "供应链瓶颈缓解是欧洲海上风电加速装机的必要条件。",
            "tags": ["西门子歌美飒", "单桩", "供应链", "德国", "欧洲"],
            "value_score": 3,
        },
    },
]
