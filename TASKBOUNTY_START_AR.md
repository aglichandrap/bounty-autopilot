# TaskBounty income lane

هذا المسار هو الاقرب للدخل الالي الحقيقي، لان TaskBounty مصمم اصلا لعملاء AI agents:

- يعلن عن bounties برمجية ممولة.
- يعطي API للعثور على task واخذ access.
- يقبل PR او unified diff patch.
- يدفع بعد التحقق والقبول، وليس فقط بعد "العثور على فرصة".

## ماذا يلزم مرة واحدة من صاحب الحساب

1. افتح حساب Agent:
   https://www.task-bounty.com/for-agents

2. من Dashboard -> API keys، انسخ API key.

3. من Agent settings، انسخ Agent ID اذا ظهر لك.

4. اضبط طريقة الدفع:
   - USDC on Base هو الاسهل غالبا اذا عندك wallet.
   - او USD bank transfer اذا مدعوم عندك.

5. ضع هذه القيم كاسرار في GitHub repo `asaadnashed/bounty-autopilot`:
   - `TASKBOUNTY_API_KEY`
   - `TASKBOUNTY_AGENT_ID`

## ماذا سيفعل النظام بعد ذلك

1. يراقب TaskBounty و GitHub bounty issues.
2. يترك اي فرصة مزدحمة او assigned او غير قابلة للدفع.
3. يحاول فقط على tasks صغيرة قابلة للفحص.
4. يجهز patch او PR مع regression test عندما يكون ذلك ممكنا.
5. يقدم النتيجة عبر TaskBounty API اذا توفر المفتاح.

## القاعدة المالية

هذا ليس دخل مضمون. الدخل يحصل فقط اذا:

- task ما زال مفتوحا.
- الحل صحيح.
- الاختبارات تمر.
- submission يفوز قبل غيره.
- المنصة تقبل وتدفع.

لكن هذا افضل من التسويق اليدوي، لان مصدر الطلب موجود اصلا والمنصة تطلب agents.
