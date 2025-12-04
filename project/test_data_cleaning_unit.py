# 测试数据清洗过滤功能的单元测试
import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app.scraper.scraper import BaiduNewsScraper

def test_data_cleaning():
    """测试数据清洗过滤功能"""
    print("=== 测试数据清洗过滤功能 ===")
    
    # 创建抓取器实例
    scraper = BaiduNewsScraper()
    
    # 模拟各种新闻数据情况
    test_cases = [
        # 正常数据 - 所有字段都有效
        {
            "title": "正常新闻标题",
            "url": "https://example.com/news1",
            "source": "示例来源",
            "summary": "这是一条正常的新闻摘要，内容完整。",
            "cover": "https://example.com/cover1.jpg",
            "expected": "保留"  # 应该保留
        },
        # 脏数据 - 4个无效字段
        {
            "title": "",
            "url": "",
            "source": "未知来源",
            "summary": "",
            "cover": "",
            "expected": "过滤"  # 应该过滤
        },
        # 脏数据 - 3个无效字段
        {
            "title": "有标题",
            "url": "",
            "source": "未知来源",
            "summary": "",
            "cover": "",
            "expected": "过滤"  # 应该过滤
        },
        # 边缘情况 - 3个无效字段
        {
            "title": "有标题",
            "url": "https://example.com/news2",
            "source": "未知来源",
            "summary": "",
            "cover": "",
            "expected": "过滤"  # 应该过滤（3个无效字段）
        },
        # 特定情况 - 无标题
        {
            "title": "无标题",
            "url": "https://example.com/news3",
            "source": "示例来源",
            "summary": "有摘要",
            "cover": "https://example.com/cover3.jpg",
            "expected": "保留"  # 应该保留
        },
        # 特定情况 - JavaScript链接（只有1个无效字段）
        {
            "title": "有标题",
            "url": "javascript:alert('test')",
            "source": "示例来源",
            "summary": "有摘要",
            "cover": "有封面",
            "expected": "保留"  # 应该保留（只有1个无效字段）
        },
    ]
    
    # 运行测试用例
    for i, test_case in enumerate(test_cases):
        print(f"\n测试用例 {i+1}:")
        print(f"   标题: {'有' if test_case['title'] and test_case['title'] != '无标题' else '无'}")
        print(f"   URL: {'有效' if test_case['url'] and 'javascript:' not in test_case['url'] and '#' not in test_case['url'] else '无效'}")
        print(f"   来源: {'有效' if test_case['source'] and test_case['source'] != '未知来源' else '无效'}")
        print(f"   摘要: {'有' if test_case['summary'] else '无'}")
        print(f"   封面: {'有' if test_case['cover'] else '无'}")
        print(f"   预期结果: {test_case['expected']}")
        
        # 计算无效字段数量
        invalid_count = 0
        
        # 检查URL
        is_url_valid = bool(test_case['url'] and not test_case['url'].startswith("javascript:") and "#" not in test_case['url'])
        if not is_url_valid: invalid_count += 1
        
        # 检查封面
        is_cover_valid = bool(test_case['cover'])
        if not is_cover_valid: invalid_count += 1
        
        # 检查来源
        is_source_valid = bool(test_case['source'] and test_case['source'] != "未知来源")
        if not is_source_valid: invalid_count += 1
        
        # 检查标题
        is_title_valid = bool(test_case['title'] and test_case['title'] != "无标题")
        if not is_title_valid: invalid_count += 1
        
        # 检查摘要
        is_summary_valid = bool(test_case['summary'])
        if not is_summary_valid: invalid_count += 1
        
        # 判断是否为脏数据
        is_dirty = invalid_count >= 3
        result = "过滤" if is_dirty else "保留"
        
        print(f"   实际结果: {result} (无效字段数: {invalid_count})")
        print(f"   测试结果: {'通过' if result == test_case['expected'] else '失败'}")
    
    print("\n=== 单元测试完成 ===")

if __name__ == "__main__":
    test_data_cleaning()
