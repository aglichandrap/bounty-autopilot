# خطة إطلاق Bounty Autopilot

## الهدف

تشغيل نظام أونلاين يبحث كل ساعتين عن فرص برمجية مدفوعة، يحول أفضلها إلى queue عمل، ثم نستخدم Codex لحل الفرص القابلة فعلا عبر PRs حقيقية.

هذا ليس دخل مضمون. لكنه أقرب مسار عملي بدون تسويق، بدون تصوير، بدون نشر يومي، وبدون بيع مباشر.

## قاعدة صفر تدخل بعد الإعداد

القاعدة الأساسية للمشروع: المستخدم يساعد مرة واحدة فقط في الحسابات والصلاحيات والدفع. بعد ذلك يجب أن يعمل النظام بدون قرارات يومية من المستخدم.

أي خطوة يمكن تنفيذها آليا يجب تنفيذها آليا. لا يطلب النظام تدخل المستخدم إلا عند حدود لا يمكن تجاوزها قانونيا أو تقنيا، مثل KYC، ربط payout، أو صلاحية GitHub غير ممنوحة.

## ما صار جاهزا

- GitHub Actions workflow يعمل كل ساعتين.
- سكربت `scripts/bounty_scout.py` يبحث عن issues فيها bounty/reward/paid.
- سكربت `scripts/bounty_worker_queue.py` يحول أفضل النتائج إلى قائمة عمل.
- ملف `bounty_extra_queries.txt` لتوسيع البحث بدون تعديل الكود.
- ملف الحسابات `BOUNTY_AUTOPILOT_ACCOUNTS_AR.md`.
- ملف التشغيل `BOUNTY_AUTOPILOT_RUNBOOK_AR.md`.
- ملف الحالة `BOUNTY_AUTOPILOT_STATUS.md`.
- ملفات النتائج:
  - `bounty_report.md`
  - `bounty_candidates.json`
  - `bounty_worker_queue.md`

## ما سيحدث كل ساعتين

1. GitHub Actions يشغل scout.
2. السكربت يبحث في GitHub عن bounties.
3. يفلتر النتائج الخطرة أو غير الجدية.
4. يكتب تقرير candidates.
5. يبني worker queue بأفضل 3 فرص.
6. يفتح أو يحدث GitHub issue باسم `Bounty scout candidates`.

## كيف يتحول هذا إلى دخل

1. نجد bounty حقيقية.
2. أفتح repository وأفهم المطلوب.
3. أصلح المشكلة وأشغل الاختبارات.
4. أجهز PR نظيف.
5. صاحب المشروع يدمج PR.
6. منصة bounty تدفع عبر حساب payout/محفظة.

الدفع لا يحصل قبل قبول الطرف الآخر. لذلك أول يومين هدفنا هو إيجاد فرص صالحة وتنفيذ أول PR حقيقي، لا الوعد بدخل فوري.

## المطلوب منك مرة واحدة بكرا

### GitHub

1. افتح حساب GitHub أو استخدم حسابك الحالي.
2. أنشئ repository جديد باسم:
   `bounty-autopilot`
3. اجعله Private أو Public. الأفضل Private في البداية.
4. ارسل لي رابط الـ repository.
5. فعّل GitHub Actions إذا ظهر لك تنبيه تعطيل workflows.

اقرأ أيضا:

- `BOUNTY_AUTOPILOT_ACCOUNTS_AR.md`
- `ZERO_INTERVENTION_RULE_AR.md`

### حسابات Bounty / Payout

افتح هذه الحسابات فقط عندما نحتاج أول payout أو أول submission:

1. Lightning Bounties:
   - يحتاج غالبا GitHub login ومحفظة Bitcoin/Lightning أو طريقة payout يدعمها الموقع.
2. Opire:
   - يحتاج GitHub login وربط payout حسب المنصة.
3. BountyHub / Collaborators:
   - نستخدمها فقط إذا وجدنا bounty واضحة وقابلة للحل.

لا تضع بطاقة أو محفظة في أي منصة قبل أن نتحقق من bounty حقيقية.

### صلاحيات مريحة

إذا تريدني أرفع كل شيء:

1. أعطني repo link.
2. اسمح للـ GitHub connector بالوصول إلى هذا repo إذا طلب منك Codex ذلك.
3. بعدها أرفع الملفات وأشغل workflow.

## قواعد السلامة

- لا PR عشوائي.
- لا security spam.
- لا contests أو referral أو fake accounts.
- لا شيء يحتاج خداع أو scraping خاص.
- لا نشتغل إلا على issue مفتوح وواضح وله bounty أو reward قابل للتحقق.

## مؤشرات نجاح أول 72 ساعة

- workflow يعمل كل ساعتين بدون فشل.
- يوجد 5-20 candidates في التقرير.
- يوجد 1-3 queue items قابلة للفحص.
- نختار أول issue قابلة للحل.
- نجهز أول PR حقيقي.

## متى يصبح "شغال 100%"

يصبح شغال 100% تقنيا عندما:

1. الملفات مرفوعة على repo.
2. GitHub Actions تعمل كل ساعتين.
3. issue التقرير يتحدث تلقائيا.
4. Codex automation يراجع queue دوريا.
5. يوجد حساب payout جاهز عند أول bounty مقبولة.

يصبح شغال 100% ماليا فقط بعد أول PR مقبول ومدفوع.

الهدف التشغيلي بعد الإعداد: البحث، الاختيار، التنفيذ، الاختبار، وفتح PR تتم بدون تدخل المستخدم عندما تسمح الصلاحيات بذلك.
