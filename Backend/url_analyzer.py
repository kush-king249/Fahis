"""
Fahis URL Analyzer - المحرك الخلفي لتحليل الروابط
يحتوي على الخوارزميات والنماذج المطلوبة لتحليل الروابط وكشف التصيد الاحتيالي
"""

import re
import urllib.parse
import tldextract
import requests
from typing import Dict, List, Tuple
import json
import os

class URLAnalyzer:
    """
    فئة تحليل الروابط الرئيسية
    تحتوي على جميع الوظائف المطلوبة لتحليل الروابط وكشف التصيد
    """
    
    def __init__(self):
        """تهيئة محلل الروابط"""
        self.suspicious_keywords = [
            'login', 'secure', 'account', 'verify', 'update', 'confirm',
            'bank', 'paypal', 'amazon', 'google', 'microsoft', 'apple',
            'security', 'suspended', 'limited', 'urgent', 'immediate'
        ]
        
        self.safe_domains = [
            'google.com', 'facebook.com', 'twitter.com', 'linkedin.com',
            'github.com', 'stackoverflow.com', 'wikipedia.org'
        ]
        
        self.phishing_domains = [
            'googIe.com', 'faceb00k.com', 'twiter.com', 'linkedln.com',
            'githup.com', 'stackoverfl0w.com'
        ]
        
        # قاموس الأحرف المشبوهة لل homoglyphs
        # هذا القاموس يربط الحرف اللاتيني بالحروف المشابهة له في لغات أخرى (مثل السيريلية أو اليونانية)
        self.homoglyph_map = {
            'a': ['а'],  # Cyrillic 'a'
            'e': ['е'],  # Cyrillic 'e'
            'i': ['і', 'ı', 'l', '1'], # Cyrillic 'i', Turkish 'ı', Latin 'l', digit '1'
            'o': ['о', '0'], # Cyrillic 'o', digit '0'
            'p': ['р'],  # Cyrillic 'p'
            'c': ['с'],  # Cyrillic 'c'
            'y': ['у'],  # Cyrillic 'y'
            'x': ['х'],  # Cyrillic 'x'
            'v': ['ν'],  # Greek 'nu'
            'w': ['ѡ'],  # Old Cyrillic 'omega'
        }
        
        # تحميل قاعدة بيانات النطاقات إذا كانت موجودة
        self.load_domain_database()
    
    def load_domain_database(self):
        """تحميل قاعدة بيانات النطاقات من ملف JSON"""
        try:
            db_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'domains.json')
            if os.path.exists(db_path):
                with open(db_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.safe_domains.extend(data.get('safe', []))
                    self.phishing_domains.extend(data.get('phishing', []))
        except Exception as e:
            print(f"تحذير: لا يمكن تحميل قاعدة بيانات النطاقات: {e}")
    
    def extract_features(self, url: str) -> Dict:
        """
        استخلاص الميزات من الرابط للتحليل
        
        Args:
            url (str): الرابط المراد تحليله
            
        Returns:
            Dict: قاموس يحتوي على الميزات المستخلصة
        """
        features = {}
        
        # الميزات الأساسية
        features['url_length'] = len(url)
        features['has_https'] = url.startswith('https://')
        features['has_ip'] = bool(re.search(r'\d+\.\d+\.\d+\.\d+', url))
        
        # تحليل الرابط
        parsed = urllib.parse.urlparse(url)
        extracted = tldextract.extract(url)
        
        # ميزات النطاق
        features['domain'] = extracted.domain + '.' + extracted.suffix if extracted.suffix else extracted.domain
        features['subdomain'] = extracted.subdomain
        features['suffix'] = extracted.suffix
        features['subdomain_count'] = len(extracted.subdomain.split('.')) if extracted.subdomain else 0
        
        # الأحرف الخاصة
        features['special_chars_count'] = len(re.findall(r'[@\-_]', url))
        features['dots_count'] = url.count('.')
        features['slashes_count'] = url.count('/')
        
        # الكلمات المشبوهة (نبحث عنها في المسار والاستعلام فقط)
        path_query = parsed.path + parsed.query
        features['suspicious_keywords_count'] = sum(
            1 for keyword in self.suspicious_keywords 
            if keyword.lower() in path_query.lower()
        )
        
        # طول أجزاء مختلفة
        features['domain_length'] = len(features['domain']) if features['domain'] else 0
        features['path_length'] = len(parsed.path)
        features['query_length'] = len(parsed.query) if parsed.query else 0
        
        return features
    
    def check_homoglyphs(self, domain: str) -> bool:
        """
        فحص وجود homoglyphs في النطاق
        
        Args:
            domain (str): النطاق المراد فحصه
            
        Returns:
            bool: True إذا كان يحتوي على homoglyphs مشبوهة
        """
        # تحويل النطاق إلى lowercase لتوحيد الفحص
        lower_domain = domain.lower()
        
        for original_char, homoglyphs_list in self.homoglyph_map.items():
            # إذا كان الحرف الأصلي موجوداً في النطاق
            if original_char in lower_domain:
                for homoglyph_char in homoglyphs_list:
                    # إذا كان الحرف المشابه موجوداً في النطاق
                    # وتأكد أنه ليس نفس الحرف الأصلي (لتجنب false positives)
                    if homoglyph_char in lower_domain and homoglyph_char != original_char:
                        return True
            # تحقق أيضاً من وجود homoglyph_char بدون وجود original_char
            # مثلاً، إذا كان النطاق يستخدم '0' بدلاً من 'o' تماماً
            for homoglyph_char in homoglyphs_list:
                if homoglyph_char in lower_domain and original_char not in lower_domain:
                    return True
        return False
    
    def check_typosquatting(self, domain: str) -> Tuple[bool, str]:
        """
        فحص typosquatting مقارنة بالنطاقات المعروفة
        
        Args:
            domain (str): النطاق المراد فحصه
            
        Returns:
            Tuple[bool, str]: (هل يوجد typosquatting, النطاق الأصلي المحتمل)
        """
        for safe_domain in self.safe_domains:
            # حساب المسافة بين النطاقين (Levenshtein distance مبسطة)
            # يمكن استخدام مكتبة مثل python-Levenshtein للحصول على دقة أعلى
            if self._calculate_similarity(domain, safe_domain) > 0.8 and domain != safe_domain:
                return True, safe_domain
        
        return False, ""
    
    def _calculate_similarity(self, str1: str, str2: str) -> float:
        """
        حساب التشابه بين نصين باستخدام Jaccard similarity (مبسط)
        
        Args:
            str1 (str): النص الأول
            str2 (str): النص الثاني
            
        Returns:
            float: نسبة التشابه (0-1)
        """
        set1 = set(str1)
        set2 = set(str2)
        intersection = len(set1.intersection(set2))
        union = len(set1.union(set2))
        
        if union == 0:
            return 0.0
        return intersection / union
    
    def analyze_url(self, url: str) -> Dict:
        """
        تحليل شامل للرابط
        
        Args:
            url (str): الرابط المراد تحليله
            
        Returns:
            Dict: نتائج التحليل الشاملة
        """
        result = {
            'url': url,
            'is_safe': True,
            'risk_level': 'low',  # low, medium, high
            'score': 0,  # 0-100 (0 = آمن تماماً, 100 = خطير جداً)
            'warnings': [],
            'features': {},
            'recommendations': []
        }
        
        try:
            # استخلاص الميزات
            features = self.extract_features(url)
            result['features'] = features
            
            # فحص النطاق في القوائم المعروفة
            domain = features['domain']
            
            if domain in self.phishing_domains:
                result['is_safe'] = False
                result['risk_level'] = 'high'
                result['score'] = 95
                result['warnings'].append('النطاق موجود في قائمة النطاقات الاحتيالية المعروفة')
                result['recommendations'].append('تجنب هذا الرابط تماماً')
                return result
            
            if domain in self.safe_domains:
                result['score'] = 5
                result['recommendations'].append('النطاق آمن ومعروف')
                return result
            
            # تحليل المخاطر
            risk_score = 0
            
            # فحص طول الرابط
            if features['url_length'] > 100:
                risk_score += 10
                result['warnings'].append('الرابط طويل جداً (قد يكون مشبوهاً)')
            
            # فحص HTTPS
            if not features['has_https']:
                risk_score += 20
                result['warnings'].append('الرابط لا يستخدم HTTPS (غير آمن)')
            
            # فحص عنوان IP
            if features['has_ip']:
                risk_score += 25
                result['warnings'].append('الرابط يستخدم عنوان IP بدلاً من اسم النطاق')
            
            # فحص النطاقات الفرعية
            if features['subdomain_count'] > 2:
                risk_score += 10
                result['warnings'].append('عدد كبير من النطاقات الفرعية')
            
            # فحص الكلمات المشبوهة
            if features['suspicious_keywords_count'] > 0:
                risk_score += features['suspicious_keywords_count'] * 8 # وزن أقل للكلمات المشبوهة في المسار
                result['warnings'].append(f'يحتوي على {features["suspicious_keywords_count"]} كلمة مشبوهة في المسار/الاستعلام')
            
            # فحص homoglyphs
            if self.check_homoglyphs(domain):
                risk_score += 40 # وزن عالي جداً لـ homoglyphs
                result['warnings'].append('النطاق يحتوي على أحرف مشبوهة (homoglyphs)')
            
            # فحص typosquatting
            is_typo, original_domain = self.check_typosquatting(domain)
            if is_typo:
                risk_score += 35
                result['warnings'].append(f'النطاق مشابه لنطاق معروف: {original_domain}')
            
            # تحديد مستوى المخاطر
            result['score'] = min(risk_score, 100)
            
            if risk_score >= 70:
                result['is_safe'] = False
                result['risk_level'] = 'high'
                result['recommendations'].append('تجنب هذا الرابط - مخاطر عالية جداً')
            elif risk_score >= 40:
                result['is_safe'] = False
                result['risk_level'] = 'medium'
                result['recommendations'].append('كن حذراً مع هذا الرابط - مخاطر متوسطة')
            else:
                result['risk_level'] = 'low'
                result['recommendations'].append('الرابط يبدو آمناً نسبياً')
            
        except Exception as e:
            result['is_safe'] = False
            result['risk_level'] = 'high'
            result['score'] = 100
            result['warnings'].append(f'خطأ في تحليل الرابط: {str(e)}')
            result['recommendations'].append('لا يمكن تحليل الرابط - تجنبه')
        
        return result

# دالة مساعدة للاستخدام المباشر
def analyze_url(url: str) -> Dict:
    """
    دالة مساعدة لتحليل رابط واحد
    
    Args:
        url (str): الرابط المراد تحليله
        
    Returns:
        Dict: نتائج التحليل
    """
    analyzer = URLAnalyzer()
    return analyzer.analyze_url(url)

if __name__ == "__main__":
    # اختبار سريع
    test_urls = [
        "https://www.google.com", # آمن
        "http://googIe.com/login", # homoglyph + http + suspicious keyword
        "https://192.168.1.1/secure/account", # IP address + suspicious keyword
        "https://very-long-suspicious-domain-name-that-looks-like-phishing.com/login/verify/account", # long URL + suspicious keywords
        "https://www.faceb00k.com", # typosquatting
        "https://www.microsoft.com", # آمن
        "http://www.example.com/update-your-info", # http + suspicious keyword
        "https://docs.google.com.drive.evil.com/login", # multiple subdomains + suspicious keyword
        "https://www.paypal.com", # آمن
        "https://paypaI.com", # homoglyph
        "https://www.youtube.com", # آمن
        "https://www.youtube.com/watch?v=dQw4w9WgXcQ", # آمن
        "ftp://ftp.example.com/files/document.pdf" # FTP
    ]
    
    analyzer = URLAnalyzer()
    
    for url in test_urls:
        print(f"\nتحليل: {url}")
        result = analyzer.analyze_url(url)
        print(f"آمن: {result['is_safe']}")
        print(f"مستوى المخاطر: {result['risk_level']}")
        print(f"النقاط: {result['score']}")
        print(f"التحذيرات: {result['warnings']}")
        print(f"التوصيات: {result['recommendations']}")
        # print(f"الميزات: {result['features']}") # لطباعة الميزات المستخلصة
