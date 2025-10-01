#!/usr/bin/env python3
"""
Fahis - أداة مكافحة التصيد الاحتيالي
الملف الرئيسي لتشغيل الأداة

يمكن تشغيل الأداة بطرق مختلفة:
1. الواجهة الرسومية (GUI) - الافتراضي
2. واجهة سطر الأوامر (CLI)
3. الوضع التفاعلي
"""

import sys
import os
import argparse

def main():
    """الدالة الرئيسية لتشغيل Fahis"""
    
    parser = argparse.ArgumentParser(
        description="Fahis - أداة مكافحة التصيد الاحتيالي",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
أوضاع التشغيل:
  بدون معاملات          تشغيل الواجهة الرسومية (GUI)
  --cli                  تشغيل واجهة سطر الأوامر
  --gui                  تشغيل الواجهة الرسومية (صريح)

أمثلة:
  python fahis.py                    # الواجهة الرسومية
  python fahis.py --cli              # واجهة سطر الأوامر
  python fahis.py --cli -u site.com  # تحليل رابط مباشر
        """
    )
    
    parser.add_argument("--cli", action="store_true", 
                       help="تشغيل واجهة سطر الأوامر")
    parser.add_argument("--gui", action="store_true", 
                       help="تشغيل الواجهة الرسومية (الافتراضي)")
    
    # تمرير باقي المعاملات لواجهة سطر الأوامر
    args, unknown = parser.parse_known_args()
    
    # إضافة مسار المشروع إلى sys.path لتمكين الاستيراد النسبي
    project_root = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, project_root)
    
    try:
        if args.cli:
            # تشغيل واجهة سطر الأوامر
            print("🚀 تشغيل Fahis - واجهة سطر الأوامر")
            
            # إعادة بناء sys.argv لواجهة سطر الأوامر
            sys.argv = ["fahis-cli"] + unknown
            
            from cli.cli import main as cli_main
            cli_main()
            
        else:
            # تشغيل الواجهة الرسومية (الافتراضي)
            print("🚀 تشغيل Fahis - الواجهة الرسومية")
            
            try:
                from frontend.gui import main as gui_main
                gui_main()
            except ImportError as e:
                print(f"❌ خطأ في تحميل الواجهة الرسومية: {e}")
                print("💡 تأكد من تثبيت tkinter أو استخدم --cli للواجهة النصية")
                sys.exit(1)
            except Exception as e:
                print(f"❌ خطأ في تشغيل الواجهة الرسومية: {e}")
                print("💡 جرب استخدام --cli للواجهة النصية")
                sys.exit(1)
                
    except KeyboardInterrupt:
        print("\n👋 تم إيقاف البرنامج بواسطة المستخدم")
    except Exception as e:
        print(f"❌ خطأ غير متوقع: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

