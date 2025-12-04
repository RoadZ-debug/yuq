# 数据抓取核心逻辑
# 用于从百度新闻接口爬取数据

import requests
from bs4 import BeautifulSoup
from urllib.parse import quote
from datetime import datetime
from app import db
from app.models import News

class BaiduNewsScraper:
    """百度新闻抓取器"""
    
    def __init__(self):
        self.base_url = "https://www.baidu.com/s"
        self.headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "accept-encoding": "gzip, deflate, br, zstd",
            "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
            "cache-control": "max-age=0",
            "connection": "keep-alive",
            "host": "www.baidu.com",
            "referer": "https://news.baidu.com/",
            "sec-ch-ua": '"Chromium";v="142", "Microsoft Edge";v="142", "Not_A Brand";v="99"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "same-site",
            "sec-fetch-user": "?1",
            "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36 Edg/142.0.0.0"
        }
    
    def fetch_news(self, keyword, page=1):
        """
        根据关键字抓取百度新闻
        :param keyword: 搜索关键字
        :param page: 页码
        :return: 新闻列表
        """
        # 构建请求参数 - 不要手动编码关键字，让requests自动处理
        params = {
            "rtt": "1",  # 实时排序
            "bsst": "1",
            "cl": "2",  # 新闻类型
            "tn": "news",
            "rsv_dl": "ns_pc",
            "word": keyword,  # 直接使用关键字，让requests自动处理URL编码
            "pn": (page - 1) * 10  # 分页参数
        }
        
        try:
            # 发送请求
            response = requests.get(
                self.base_url,
                params=params,
                headers=self.headers,
                timeout=10
            )
            response.raise_for_status()  # 检查请求是否成功
            
            # 解析HTML
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 提取新闻列表
            news_list = self._parse_news(soup)
            
            # 保存到数据库
            self._save_to_database(news_list, keyword)
            
            return news_list
            
        except requests.RequestException as e:
            print(f"抓取失败: {e}")
            return []
    
    def _parse_news(self, soup):
        """解析百度新闻页面，提取新闻信息"""
        try:
            news_list = []
            
            # 百度新闻页面结构：新闻结果保存在id为'content_left'的容器中
            content_left = soup.find("div", id="content_left")
            if not content_left:
                print("未找到新闻结果容器")
                return []
            
            # 每个新闻条目是class为'result-op.c-container'的div
            news_items = content_left.select(".result-op.c-container")
            print(f"找到 {len(news_items)} 个.result-op.c-container新闻条目")
            
            # 去重处理
            seen_titles = set()
            seen_urls = set()
            
            for item in news_items:
                try:
                    # 提取标题和链接
                    title_elem = item.find("h3")
                    if not title_elem:
                        continue
                    
                    a_tag = title_elem.find("a")
                    if not a_tag:
                        continue
                    
                    title = a_tag.text.strip()
                    url = a_tag.get("href", "")
                    
                    # 验证标题和URL
                    if not title or not url or "javascript:" in url or "#" in url:
                        continue
                    
                    # 去重检查
                    if title in seen_titles or url in seen_urls:
                        continue
                    
                    seen_titles.add(title)
                    seen_urls.add(url)
                    
                    # 提取来源和时间
                    source_elem = item.find("span", class_="c-gray")
                    if not source_elem:
                        # 尝试其他可能的来源选择器
                        source_elem = item.find("span", class_="c-color-gray")
                        if not source_elem:
                            # 查找所有span标签，尝试提取来源
                            spans = item.find_all("span")
                            for span in spans:
                                if span.text.strip() and len(span.text.strip()) < 20:
                                    source_elem = span
                                    break
                    
                    source = source_elem.text.strip() if source_elem else "未知来源"
                    
                    # 提取摘要
                    summary_elem = item.find("div", class_="c-font-normal")
                    if not summary_elem:
                        # 尝试其他可能的摘要选择器
                        summary_elem = item.find("div", class_="c-summary")
                        if not summary_elem:
                            # 查找所有div标签，尝试提取摘要
                            divs = item.find_all("div")
                            for div in divs:
                                if div.text.strip() and len(div.text.strip()) > 50:
                                    summary_elem = div
                                    break
                    
                    summary = summary_elem.text.strip() if summary_elem else ""
                    
                    # 提取封面图片
                    cover = ""
                    img_elem = item.find("img")
                    if img_elem:
                        cover = img_elem.get("src", "")
                        # 处理相对路径
                        if cover and not cover.startswith("http"):
                            cover = "https://www.baidu.com" + cover
                    
                    # 数据清洗：检查是否为脏数据
                    # 定义无效字段的条件
                    is_url_valid = bool(url and not url.startswith("javascript:") and "#" not in url)
                    is_cover_valid = bool(cover)
                    is_source_valid = bool(source and source != "未知来源")
                    is_title_valid = bool(title and title != "无标题")
                    is_summary_valid = bool(summary)
                    
                    # 计算无效字段数量
                    invalid_count = 0
                    if not is_url_valid: invalid_count += 1
                    if not is_cover_valid: invalid_count += 1
                    if not is_source_valid: invalid_count += 1
                    if not is_title_valid: invalid_count += 1
                    if not is_summary_valid: invalid_count += 1
                    
                    # 如果无效字段数量≥3，则视为脏数据，跳过
                    if invalid_count >= 3:
                        print(f"过滤脏数据: 标题='{title[:20]}...', 无效字段数={invalid_count}")
                        continue
                    
                    # 添加到新闻列表
                    news_list.append({
                        "title": title,
                        "url": url,
                        "source": source,
                        "summary": summary,
                        "cover": cover
                    })
                    
                except Exception as e:
                    # 如果单个新闻解析失败，记录日志并继续处理下一个
                    print(f"解析单个新闻失败: {e}")
                    continue
            
            print(f"成功解析 {len(news_list)} 条新闻")
            return news_list
        except Exception as e:
            print(f"解析新闻页面失败: {e}")
            return []
    
    def _save_to_database(self, news_list, keyword):
        """
        将抓取的新闻保存到数据库
        :param news_list: 新闻列表
        :param keyword: 搜索关键字
        """
        try:
            for news_item in news_list:
                # 检查是否已存在相同URL的新闻
                existing_news = News.query.filter_by(url=news_item['url']).first()
                if not existing_news:
                    # 创建新的新闻记录
                    news = News(
                        keyword=keyword,
                        title=news_item['title'],
                        summary=news_item['summary'],
                        cover=news_item['cover'],
                        url=news_item['url'],
                        source=news_item['source']
                    )
                    db.session.add(news)
            
            # 提交到数据库
            db.session.commit()
            print(f"成功保存 {len(news_list)} 条新闻到数据库")
            
        except Exception as e:
            print(f"保存到数据库失败: {e}")
            db.session.rollback()

# 创建全局抓取器实例
scraper = BaiduNewsScraper()
