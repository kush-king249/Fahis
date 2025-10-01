#!/usr/bin/env python3
"""
Fahis CLI - واجهة سطر الأوامر لأداة مكافحة التصيد الاحتيالي
واجهة بسيطة وفعالة للمستخدمين المتقدمين
"""

import argparse
import sys
import os
import json
from typing import List

# إضافة مسار المحرك الخلفي
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))
from url_analyzer import URLAnalyzer

class FahisCLI:
    """فئة واجهة سطر الأوامر"""
    
    def __init__(self):
        """تهيئة واجهة سطر الأوامر"""
        self.analyzer = URLAnalyzer()
        self.colors = {
            'red': '\033[91m',
            'green': '\033[92m',
            'yellow': '\033[93m',
            'blue': '\033[94m',
            'purple': '\033[95m',
            'cyan': '\033[96m',
            'white': '\033[97m',
            'bold': '\033[1m',
            'end': '\033[0m'
        }
    
    def colorize(self, text: str, color: str) -> str:
        """تلوين النص في الطرفية"""
        if color in self.colors:
            return f"{self.colors[color]}{text}{self.colors['end']}"
        return text
    
    def print_banner(self):
        """طباعة شعار البرنامج"""
        banner = f"""
{self.colorize('🛡️  Fahis - أداة مكافحة التصيد الاحتيالي', 'cyan')}
{self.colorize('=' * 50, 'blue')}
{self.colorize('أداة احترافية لتحليل الروابط وكشف التصيد الاحتيالي', 'white')}
{self.colorize('المطور: Hassan Mohamed Hassan Ahmed', 'purple')}
{self.colorize('=' * 50, 'blue')}
        """
        print(banner)
    
    def analyze_single_url(self, url: str, verbose: bool = False, json_output: bool = False) -> dict:
        """
        تحليل رابط واحد
        
        Args:
            url (str): الرابط المراد تحليله
            verbose (bool): إظهار تفاصيل إضافية
            json_output (bool): إخراج النتائج بصيغة JSON
            
        Returns:
            dict: نتائج التحليل
        """
        # إضافة http:// إذا لم يكن موجوداً
        if not url.startswith(('http://', 'https://', 'ftp://')):
            url = 'http://' + url
        
        print(f"\n{self.colorize('🔍 تحليل الرابط:', 'yellow')} {url}")
        print(f"{self.colorize('⏳ جاري التحليل...', 'blue')}")
        
        try:
            result = self.analyzer.analyze_url(url)
            
            if json_output:
                print(json.dumps(result, ensure_ascii=False, indent=2))
                return result
            
            # طباعة النتائج
            self.print_results(result, verbose)
            return result
            
        except Exception as e:
            error_msg = f"❌ خطأ في تحليل الرابط: {str(e)}"
            print(self.colorize(error_msg, 'red'))
            return {'error': str(e)}
    
    def analyze_multiple_urls(self, urls: List[str], verbose: bool = False, json_output: bool = False) -> List[dict]:
        """
        تحليل عدة روابط
        
        Args:
            urls (List[str]): قائمة الروابط المراد تحليلها
            verbose (bool): إظهار تفاصيل إضافية
            json_output (bool): إخراج النتائج بصيغة JSON
            
        Returns:
            List[dict]: نتائج التحليل لجميع الروابط
        """
        results = []
        
        print(f"\n{self.colorize(f'🔍 تحليل {len(urls)} رابط...', 'yellow')}")
        
        for i, url in enumerate(urls, 1):
            print(f"\n{self.colorize(f'[{i}/{len(urls)}]', 'cyan')} {url}")
            
            # إضافة http:// إذا لم يكن موجوداً
            if not url.startswith(('http://', 'https://', 'ftp://')):
                url = 'http://' + url
            
            try:
                result = self.analyzer.analyze_url(url)
                results.append(result)
                
                if not json_output:
                    self.print_results(result, verbose, compact=True)
                    
            except Exception as e:
                error_result = {'url': url, 'error': str(e)}
                results.append(error_result)
                if not json_output:
                    print(self.colorize(f"❌ خطأ: {str(e)}", 'red'))
        
        if json_output:
            print(json.dumps(results, ensure_ascii=False, indent=2))
        
        return results
    
    def analyze_from_file(self, file_path: str, verbose: bool = False, json_output: bool = False) -> List[dict]:
        """
        تحليل روابط من ملف
        
        Args:
            file_path (str): مسار الملف الذي يحتوي على الروابط
            verbose (bool): إظهار تفاصيل إضافية
            json_output (bool): إخراج النتائج بصيغة JSON
            
        Returns:
            List[dict]: نتائج التحليل
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                urls = [line.strip() for line in f if line.strip()]
            
            print(f"{self.colorize(f'📁 تم تحميل {len(urls)} رابط من الملف: {file_path}', 'green')}")
            return self.analyze_multiple_urls(urls, verbose, json_output)
            
        except FileNotFoundError:
            error_msg = f"❌ الملف غير موجود: {file_path}"
            print(self.colorize(error_msg, 'red'))
            return []
        except Exception as e:
            error_msg = f"❌ خطأ في قراءة الملف: {str(e)}"
            print(self.colorize(error_msg, 'red'))
            return []
    
    def print_results(self, result: dict, verbose: bool = False, compact: bool = False):
        """
        طباعة نتائج التحليل
        
        Args:
            result (dict): نتائج التحليل
            verbose (bool): إظهار تفاصيل إضافية
            compact (bool): عرض مضغوط للنتائج
        """
        if 'error' in result:
            print(self.colorize(f"❌ خطأ: {result['error']}", 'red'))
            return
        
        # حالة الأمان
        if result.get('is_safe', False):
            safety_text = self.colorize("✅ آمن", 'green')
        else:
            safety_text = self.colorize("⚠️ غير آمن", 'red')
        
        # مستوى المخاطر
        risk_level = result.get('risk_level', 'غير محدد')
        risk_colors = {'low': 'green', 'medium': 'yellow', 'high': 'red'}
        risk_icons = {'low': '🟢', 'medium': '🟡', 'high': '🔴'}
        
        risk_text = f"{risk_icons.get(risk_level, '⚪')} {risk_level}"
        risk_colored = self.colorize(risk_text, risk_colors.get(risk_level, 'white'))
        
        # النقاط
        score = result.get('score', 0)
        score_color = 'green' if score < 40 else 'yellow' if score < 70 else 'red'
        score_text = self.colorize(f"{score}/100", score_color)
        
        if compact:
            # عرض مضغوط
            print(f"  {safety_text} | {risk_colored} | {score_text}")
        else:
            # عرض مفصل
            print(f"\n{self.colorize('📊 النتائج:', 'bold')}")
            print(f"  حالة الأمان: {safety_text}")
            print(f"  مستوى المخاطر: {risk_colored}")
            print(f"  نقاط المخاطر: {score_text}")
            
            # التحذيرات
            warnings = result.get('warnings', [])
            if warnings:
                print(f"\n{self.colorize('⚠️ التحذيرات:', 'yellow')}")
                for warning in warnings:
                    print(f"  • {warning}")
            
            # التوصيات
            recommendations = result.get('recommendations', [])
            if recommendations:
                print(f"\n{self.colorize('💡 التوصيات:', 'cyan')}")
                for rec in recommendations:
                    print(f"  • {rec}")
            
            # الميزات (في الوضع المفصل فقط)
            if verbose and result.get('features'):
                print(f"\n{self.colorize('🔍 الميزات المستخلصة:', 'purple')}")
                features = result['features']
                for key, value in features.items():
                    print(f"  • {key}: {value}")
    
    def interactive_mode(self):
        """الوضع التفاعلي"""
        self.print_banner()
        print(self.colorize('🔄 الوضع التفاعلي - اكتب "exit" للخروج', 'cyan'))
        
        while True:
            try:
                url = input(f"\n{self.colorize('🔗 أدخل الرابط:', 'yellow')} ").strip()
                
                if url.lower() in ['exit', 'quit', 'خروج']:
                    print(self.colorize('👋 شكراً لاستخدام Fahis!', 'green'))
                    break
                
                if not url:
                    continue
                
                self.analyze_single_url(url, verbose=False)
                
            except KeyboardInterrupt:
                print(self.colorize('👋 تم إيقاف البرنامج بواسطة المستخدم', 'yellow'))
                break
            except EOFError:
                break

def main():
    """الدالة الرئيسية لواجهة سطر الأوامر"""
    parser = argparse.ArgumentParser(
        description='Fahis - أداة مكافحة التصيد الاحتيالي',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=r"""
أمثلة الاستخدام:
  %(prog)s -u https://example.com                    # تحليل رابط واحد
  %(prog)s -u https://example.com -v                 # تحليل مفصل
  %(prog)s -u https://example.com --json             # إخراج JSON
  %(prog)s -f urls.txt                               # تحليل من ملف
  %(prog)s -m https://site1.com https://site2.com    # تحليل عدة روابط
  %(prog)s -i                                        # الوضع التفاعلي
        """
    )
    
    parser.add_argument('-u', '--url', help='رابط واحد للتحليل')
    parser.add_argument('-f', '--file', help='ملف يحتوي على روابط للتحليل')
    parser.add_argument('-m', '--multiple', nargs='+', help='عدة روابط للتحليل')
    parser.add_argument('-i', '--interactive', action='store_true', help='الوضع التفاعلي')
    parser.add_argument('-v', '--verbose', action='store_true', help='إظهار تفاصيل إضافية')
    parser.add_argument('--json', action='store_true', help='إخراج النتائج بصيغة JSON')
    parser.add_argument('--version', action='version', version='Fahis 1.0.0')
    
    args = parser.parse_args()
    
    cli = FahisCLI()
    
    # إذا لم يتم تمرير أي معاملات، تشغيل الوضع التفاعلي
    if len(sys.argv) == 1:
        cli.interactive_mode()
        return
    
    # الوضع التفاعلي
    if args.interactive:
        cli.interactive_mode()
    
    # تحليل رابط واحد
    elif args.url:
        cli.analyze_single_url(args.url, args.verbose, args.json)
    
    # تحليل من ملف
    elif args.file:
        cli.analyze_from_file(args.file, args.verbose, args.json)
    
    # تحليل عدة روابط
    elif args.multiple:
        cli.analyze_multiple_urls(args.multiple, args.verbose, args.json)
    
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
