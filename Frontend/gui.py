"""
Fahis GUI - الواجهة الرسومية لأداة مكافحة التصيد الاحتيالي
واجهة رسومية جذابة وتفاعلية باستخدام Tkinter
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import sys
import os
from threading import Thread
import webbrowser

# إضافة مسار المحرك الخلفي
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))
from url_analyzer import URLAnalyzer

class FahisGUI:
    """فئة الواجهة الرسومية الرئيسية"""
    
    def __init__(self):
        """تهيئة الواجهة الرسومية"""
        self.root = tk.Tk()
        self.analyzer = URLAnalyzer()
        self.setup_window()
        self.create_widgets()
        
    def setup_window(self):
        """إعداد النافذة الرئيسية"""
        self.root.title("Fahis - أداة مكافحة التصيد الاحتيالي")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        
        # تعيين الأيقونة (إذا كانت متوفرة)
        try:
            self.root.iconbitmap("icon.ico")
        except:
            pass
        
        # تعيين الألوان والخطوط
        self.colors = {
            'primary': '#2E86AB',
            'secondary': '#A23B72',
            'success': '#28A745',
            'warning': '#FFC107',
            'danger': '#DC3545',
            'light': '#F8F9FA',
            'dark': '#343A40'
        }
        
        # تكوين الستايل
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
    def create_widgets(self):
        """إنشاء عناصر الواجهة"""
        # الإطار الرئيسي
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # تكوين الشبكة
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # العنوان الرئيسي
        title_label = tk.Label(
            main_frame,
            text="🛡️ Fahis - أداة مكافحة التصيد الاحتيالي",
            font=('Arial', 18, 'bold'),
            fg=self.colors['primary']
        )
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # وصف الأداة
        desc_label = tk.Label(
            main_frame,
            text="أداة احترافية لتحليل الروابط وكشف محاولات التصيد الاحتيالي باستخدام الذكاء الاصطناعي",
            font=('Arial', 10),
            fg=self.colors['dark'],
            wraplength=600
        )
        desc_label.grid(row=1, column=0, columnspan=2, pady=(0, 30))
        
        # قسم إدخال الرابط
        url_frame = ttk.LabelFrame(main_frame, text="إدخال الرابط للتحليل", padding="15")
        url_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 20))
        url_frame.columnconfigure(0, weight=1)
        
        # حقل إدخال الرابط
        self.url_var = tk.StringVar()
        self.url_entry = ttk.Entry(
            url_frame,
            textvariable=self.url_var,
            font=('Arial', 11),
            width=60
        )
        self.url_entry.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 10))
        self.url_entry.bind('<Return>', lambda e: self.analyze_url())
        
        # زر التحليل
        self.analyze_button = ttk.Button(
            url_frame,
            text="🔍 تحليل الرابط",
            command=self.analyze_url,
            style='Accent.TButton'
        )
        self.analyze_button.grid(row=0, column=1)
        
        # شريط التقدم
        self.progress = ttk.Progressbar(
            url_frame,
            mode='indeterminate',
            length=300
        )
        self.progress.grid(row=1, column=0, columnspan=2, pady=(10, 0), sticky=(tk.W, tk.E))
        self.progress.grid_remove()  # إخفاء في البداية
        
        # قسم النتائج
        results_frame = ttk.LabelFrame(main_frame, text="نتائج التحليل", padding="15")
        results_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 20))
        results_frame.columnconfigure(0, weight=1)
        results_frame.rowconfigure(1, weight=1)
        
        # إطار معلومات النتيجة
        info_frame = ttk.Frame(results_frame)
        info_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        info_frame.columnconfigure(1, weight=1)
        
        # حالة الأمان
        tk.Label(info_frame, text="حالة الأمان:", font=('Arial', 10, 'bold')).grid(row=0, column=0, sticky=tk.W)
        self.safety_label = tk.Label(info_frame, text="لم يتم التحليل بعد", font=('Arial', 10))
        self.safety_label.grid(row=0, column=1, sticky=tk.W, padx=(10, 0))
        
        # مستوى المخاطر
        tk.Label(info_frame, text="مستوى المخاطر:", font=('Arial', 10, 'bold')).grid(row=1, column=0, sticky=tk.W)
        self.risk_label = tk.Label(info_frame, text="غير محدد", font=('Arial', 10))
        self.risk_label.grid(row=1, column=1, sticky=tk.W, padx=(10, 0))
        
        # النقاط
        tk.Label(info_frame, text="نقاط المخاطر:", font=('Arial', 10, 'bold')).grid(row=2, column=0, sticky=tk.W)
        self.score_label = tk.Label(info_frame, text="0/100", font=('Arial', 10))
        self.score_label.grid(row=2, column=1, sticky=tk.W, padx=(10, 0))
        
        # منطقة النص للتفاصيل
        self.details_text = scrolledtext.ScrolledText(
            results_frame,
            height=15,
            width=70,
            font=('Consolas', 9),
            wrap=tk.WORD
        )
        self.details_text.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # قسم الأزرار السفلية
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.grid(row=4, column=0, columnspan=2, pady=(10, 0))
        
        # زر مسح النتائج
        ttk.Button(
            buttons_frame,
            text="🗑️ مسح النتائج",
            command=self.clear_results
        ).grid(row=0, column=0, padx=(0, 10))
        
        # زر حول البرنامج
        ttk.Button(
            buttons_frame,
            text="ℹ️ حول البرنامج",
            command=self.show_about
        ).grid(row=0, column=1, padx=(0, 10))
        
        # زر المساعدة
        ttk.Button(
            buttons_frame,
            text="❓ المساعدة",
            command=self.show_help
        ).grid(row=0, column=2)
        
        # تعيين التركيز على حقل الإدخال
        self.url_entry.focus()
        
    def analyze_url(self):
        """تحليل الرابط المدخل"""
        url = self.url_var.get().strip()
        
        if not url:
            messagebox.showwarning("تحذير", "يرجى إدخال رابط للتحليل")
            return
        
        # إضافة http:// إذا لم يكن موجوداً
        if not url.startswith(('http://', 'https://', 'ftp://')):
            url = 'http://' + url
            self.url_var.set(url)
        
        # تعطيل الزر وإظهار شريط التقدم
        self.analyze_button.config(state='disabled')
        self.progress.grid()
        self.progress.start()
        
        # تشغيل التحليل في خيط منفصل
        thread = Thread(target=self._analyze_thread, args=(url,))
        thread.daemon = True
        thread.start()
        
    def _analyze_thread(self, url):
        """تحليل الرابط في خيط منفصل"""
        try:
            result = self.analyzer.analyze_url(url)
            # تحديث الواجهة في الخيط الرئيسي
            self.root.after(0, self._update_results, result)
        except Exception as e:
            error_result = {
                'is_safe': False,
                'risk_level': 'high',
                'score': 100,
                'warnings': [f'خطأ في التحليل: {str(e)}'],
                'recommendations': ['لا يمكن تحليل الرابط'],
                'features': {}
            }
            self.root.after(0, self._update_results, error_result)
        
    def _update_results(self, result):
        """تحديث نتائج التحليل في الواجهة"""
        # إيقاف شريط التقدم وإعادة تفعيل الزر
        self.progress.stop()
        self.progress.grid_remove()
        self.analyze_button.config(state='normal')
        
        # تحديث معلومات النتيجة
        if result['is_safe']:
            self.safety_label.config(text="✅ آمن", fg=self.colors['success'])
        else:
            self.safety_label.config(text="⚠️ غير آمن", fg=self.colors['danger'])
        
        # تحديث مستوى المخاطر
        risk_colors = {
            'low': self.colors['success'],
            'medium': self.colors['warning'],
            'high': self.colors['danger']
        }
        
        risk_texts = {
            'low': '🟢 منخفض',
            'medium': '🟡 متوسط',
            'high': '🔴 عالي'
        }
        
        self.risk_label.config(
            text=risk_texts.get(result['risk_level'], 'غير محدد'),
            fg=risk_colors.get(result['risk_level'], self.colors['dark'])
        )
        
        # تحديث النقاط
        score_color = self.colors['success']
        if result['score'] >= 70:
            score_color = self.colors['danger']
        elif result['score'] >= 40:
            score_color = self.colors['warning']
        
        self.score_label.config(
            text=f"{result['score']}/100",
            fg=score_color
        )
        
        # تحديث التفاصيل
        self.details_text.delete(1.0, tk.END)
        
        details = f"تحليل مفصل للرابط: {result.get('url', 'غير محدد')}\n"
        details += "=" * 60 + "\n\n"
        
        # التحذيرات
        if result.get('warnings'):
            details += "⚠️ التحذيرات:\n"
            for warning in result['warnings']:
                details += f"  • {warning}\n"
            details += "\n"
        
        # التوصيات
        if result.get('recommendations'):
            details += "💡 التوصيات:\n"
            for rec in result['recommendations']:
                details += f"  • {rec}\n"
            details += "\n"
        
        # الميزات المستخلصة
        if result.get('features'):
            details += "🔍 الميزات المستخلصة:\n"
            features = result['features']
            details += f"  • طول الرابط: {features.get('url_length', 'غير محدد')}\n"
            details += f"  • يستخدم HTTPS: {'نعم' if features.get('has_https') else 'لا'}\n"
            details += f"  • يحتوي على IP: {'نعم' if features.get('has_ip') else 'لا'}\n"
            details += f"  • النطاق: {features.get('domain', 'غير محدد')}\n"
            details += f"  • النطاق الفرعي: {features.get('subdomain', 'لا يوجد')}\n"
            details += f"  • عدد النطاقات الفرعية: {features.get('subdomain_count', 0)}\n"
            details += f"  • عدد الكلمات المشبوهة: {features.get('suspicious_keywords_count', 0)}\n"
            details += f"  • عدد الأحرف الخاصة: {features.get('special_chars_count', 0)}\n"
        
        self.details_text.insert(1.0, details)
        
    def clear_results(self):
        """مسح النتائج والإدخال"""
        self.url_var.set("")
        self.safety_label.config(text="لم يتم التحليل بعد", fg=self.colors['dark'])
        self.risk_label.config(text="غير محدد", fg=self.colors['dark'])
        self.score_label.config(text="0/100", fg=self.colors['dark'])
        self.details_text.delete(1.0, tk.END)
        self.url_entry.focus()
        
    def show_about(self):
        """إظهار معلومات حول البرنامج"""
        about_text = """
🛡️ Fahis - أداة مكافحة التصيد الاحتيالي

الإصدار: 1.0.0

أداة احترافية ومتكاملة لتحليل الروابط وكشف محاولات التصيد الاحتيالي
باستخدام تقنيات الذكاء الاصطناعي والتحليل المتقدم.

الميزات:
• تحليل شامل للروابط
• كشف أساليب التمويه المختلفة
• واجهة رسومية جذابة وسهلة الاستخدام
• قاعدة بيانات محدثة للنطاقات المعروفة

المطور: Hassan Mohamed Hassan Ahmed
GitHub: kush-king249

© 2024 جميع الحقوق محفوظة
        """
        messagebox.showinfo("حول البرنامج", about_text)
        
    def show_help(self):
        """إظهار المساعدة"""
        help_text = """
📖 كيفية استخدام Fahis:

1. أدخل الرابط المراد فحصه في الحقل المخصص
2. اضغط على زر "تحليل الرابط" أو اضغط Enter
3. انتظر حتى يكتمل التحليل
4. راجع النتائج في القسم السفلي

نصائح:
• يمكنك إدخال الرابط مع أو بدون http://
• الأداة تدعم http, https, و ftp
• النتائج تشمل مستوى المخاطر والتوصيات
• استخدم زر "مسح النتائج" لبدء تحليل جديد

للمساعدة الإضافية، راجع ملف README.md
        """
        messagebox.showinfo("المساعدة", help_text)
        
    def run(self):
        """تشغيل الواجهة الرسومية"""
        self.root.mainloop()

def main():
    """الدالة الرئيسية لتشغيل الواجهة الرسومية"""
    try:
        app = FahisGUI()
        app.run()
    except Exception as e:
        messagebox.showerror("خطأ", f"حدث خطأ في تشغيل البرنامج:\n{str(e)}")

if __name__ == "__main__":
    main()
