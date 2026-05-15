# Runbook التشغيل

## التشغيل الطبيعي

كل ساعتين:

1. `bounty_scout.py` يبحث عن bounties.
2. `bounty_worker_queue.py` يختار أفضل 3 فرص.
3. GitHub Actions يحفظ النتائج.
4. GitHub issue باسم `Bounty scout candidates` يتحدث تلقائيا.
5. Codex automation `Bounty Worker Autopilot` يحاول تحويل queue إلى عمل برمجي حقيقي.

## قرار العمل التلقائي

الـ worker يشتغل فقط إذا:

- issue مفتوح.
- bounty أو reward واضح.
- repository عام.
- التغيير قانوني وأخلاقي.
- يوجد طريق اختبار أو تحقق.
- لا يحتاج بيانات خاصة أو حسابات مزيفة أو spam.

## متى يتوقف

يتوقف إذا:

- bounty غير واضحة.
- issue محلولة مسبقا.
- المشروع يحتاج credentials خاصة.
- المطلوب security spam أو report مصطنع.
- لا يوجد اختبار أو طريقة تحقق معقولة.
- الدفع يحتاج KYC/payout غير معد.

## ماذا يعتبر نجاحا

نجاح تقني:

- workflow يعمل.
- report يتحدث.
- queue تظهر فرص قابلة للفحص.
- worker يجهز patch أو PR.

نجاح مالي:

- PR مقبول.
- bounty status يتحول إلى payable/paid.
- الرصيد يصل إلى المنصة أو wallet.

## تصعيد بدون تدخل يومي

إذا تعذر PR بسبب صلاحية ناقصة:

- يسجل السبب في التقرير.
- ينتقل للفرصة التالية في التشغيل التالي.

إذا تعذر payout:

- يسجل المنصة والحساب المطلوب.
- لا يحاول تجاوز KYC أو إنشاء wallet باسم المستخدم.
