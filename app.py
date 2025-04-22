import os
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
# مطلوب لاستخدام رسائل flash.
app.secret_key = os.urandom(24) # أو استخدم سلسلة نصية ثابتة: app.secret_key = 'your secret key here'

# قائمة لتخزين البيانات المدخلة (مؤقتًا في الذاكرة)
entries = []

# الصفحة الرئيسية
@app.route('/')
def welcome():
    return render_template('welcome.html')

# صفحة النموذج (GET لعرضه, POST لإرساله)
@app.route('/form', methods=['GET', 'POST'])
def form():
    nid_value = ''
    ms_value = ''
    if request.method == 'POST':
        national_id = request.form.get('national_id', '').strip() # إزالة المسافات الزائدة
        marital_status = request.form.get('marital_status')
        is_valid = True # متغير لتتبع صحة البيانات

        # تخزين القيم لإعادة عرضها في حالة الخطأ
        nid_value = national_id
        ms_value = marital_status

        # --- تحقق أساسي من الصحة ---
        if not national_id:
            flash('حقل الرقم القومي مطلوب!', 'error')
            is_valid = False
        elif len(national_id) != 14 or not national_id.isdigit():
            flash('الرقم القومي يجب أن يتكون من 14 رقماً بالضبط.', 'error')
            is_valid = False

        if not marital_status:
            flash('يرجى اختيار الحالة الزوجية.', 'error')
            is_valid = False
        # --------------------------

        if is_valid:
            # إضافة البيانات إلى القائمة المؤقتة
            new_entry = {'national_id': national_id, 'marital_status': marital_status}
            entries.append(new_entry)

            # إظهار رسالة نجاح
            flash('تم إرسال بياناتك بنجاح!', 'success')
            # إعادة التوجيه إلى صفحة النجاح
            return redirect(url_for('success'))
        else:
            # إذا كانت البيانات غير صالحة، أعد عرض النموذج مع رسائل الخطأ والقيم المدخلة سابقًا
             return render_template('form.html', nid=nid_value, ms=ms_value)

    # إذا كان الطلب GET، اعرض النموذج (فارغًا أو بالقيم السابقة إذا كان هناك خطأ)
    return render_template('form.html', nid=nid_value, ms=ms_value)

# صفحة النجاح بعد الإرسال
@app.route('/success')
def success():
    return render_template('success.html')

# صفحة عرض كل البيانات المدخلة
@app.route('/data')
def data_display():
    # تمرير قائمة البيانات إلى القالب
    return render_template('data_display.html', all_entries=entries)

if __name__ == '__main__':
    app.run(debug=True)
