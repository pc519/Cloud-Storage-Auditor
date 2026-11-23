import requests
from datetime import datetime
import webbrowser
import os

def audit_cloud_assets(keyword):
    print(f"\n[*] جاري تدقيق الأصول السحابية المفتوحة المرتبطة بالاسم: {keyword} ...")
    targets = [
("Firebase Realtime DB", "https" + "://" + keyword + ".firebaseio" + ".com/.json"),
        ("Firebase Default DB", "https" + "://" + keyword + "-default-rtdb.firebaseio" + ".com/.json"),
        ("AWS S3 Storage Bucket", "https" + "://" + keyword + ".s3.amazonaws" + ".com"),
        ("AWS S3 Assets Bucket", "https" + "://" + keyword + "-assets.s3.amazonaws" + ".com"),
        ("AWS S3 Backup Bucket", "https" + "://" + keyword + "-backup.s3.amazonaws" + ".com")
    ]

    results = []
    for service, url in targets:
        try:
            res = requests.get(url, timeout=6)
            if res.status_code == 200 and "Permission denied" not in res.text and "AccessDenied" not in res.text:
                status = "🚨 مكشوف للعامة (Publicly Accessible - خطر حرج)"
                color = "#ef4444"
            elif res.status_code in [401, 403] or "Permission denied" in res.text or "AccessDenied" in res.text:
                status = "✅ محمي ومغلق بشكل صحيح (Protected)"
                color = "#10b981"
            else:
                status = "⚪ غير موجود / غير مستخدم (Not Found)"
                color = "#94a3b8"
        except Exception:
            status = "⚪ تعذر الاتصال / غير موجود"
            color = "#94a3b8"
        
        print(f"[{service}] -> {status}")
        results.append((service, url, status, color))

    rows = "".join([f"<tr><td>{srv}</td><td dir='ltr'>{u}</td><td style='color:{c};font-weight:bold'>{st}</td></tr>" for srv, u, st, c in results])

    html = f"""<!DOCTYPE html>
<html lang="ar" dir="rtl"><head><meta charset="UTF-8"><title>Cloud Storage Audit - {keyword}</title>
<style>body{{font-family:Tahoma,sans-serif;background:#0f172a;color:#f8fafc;padding:30px}}
.box{{max-width:950px;margin:auto;background:#1e293b;padding:25px;border-radius:10px}}
table{{width:100%;border-collapse:collapse;margin-top:20px}}
th,td{{padding:12px;border-bottom:1px solid #334155;text-align:right}}
th{{background:#0f172a;color:#38bdf8}}</style></head>
<body><div class="box"><h2>☁️ تقرير تدقيق أمان التخزين السحابي (Firebase & AWS S3)</h2>
<p><strong>اسم المشروع / الشركة المفحوصة:</strong> <span dir="ltr">{keyword}</span> | <strong>التاريخ:</strong> {datetime.now().strftime("%Y-%m-%d %H:%M")}</p>
<table><tr><th>الخدمة السحابية</th><th>الرابط المفحوص</th><th>حالة الأمان</th></tr>{rows}</table></div></body></html>"""

    fname = f"cloud_audit_{keyword}.html"
    with open(fname, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"[+] تم حفظ التقرير: {fname}")
    webbrowser.open('file://' + os.path.realpath(fname))

if __name__ == "__main__":
    name = input("Enter company or project keyword (e.g. shopify): ").strip().lower()
    if name:
        audit_cloud_assets(name)