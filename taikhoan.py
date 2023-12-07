from types import NoneType
from flask import Flask, request, render_template, redirect, url_for,g,  session
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import os
from datetime import timedelta

import sqlite3
import threading
app = Flask(__name__)
app.secret_key = "123456abcd"
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=60)
app.permanent_session_lifetime = timedelta(minutes=60)

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect('school.db')
        g.db.row_factory = sqlite3.Row
    return g.db

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['tendangnhap']
        password = request.form['password']
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM taikhoan WHERE username=? AND password=?", (password, username))
        user = cursor.fetchone()
        if user:
            user_id = username  # Thay thế giá trị này bằng giá trị thực tế của 'user_id'
            session['user_id'] = user_id
            role = user[2]
            if role == 'GV':
                return redirect(url_for('a'))
            elif role == 'QL':
                return redirect(url_for('b'))
            else:
                return render_template('login.html', error=error)
        else:
            error = "Tên đăng nhập hoặc mật khẩu không chính xác. Vui lòng thử lại."
            return render_template('login.html', error=error)
    return render_template('login.html')

@app.route('/giaovien')
def a():
    return render_template('giaovien.html')

@app.route('/quanly')
def b():
    return render_template('quanly.html')

@app.route('/logout')
def logout():
    return redirect(url_for('login'))
import random
import time



from flask import Flask, request, jsonify
import logging

@app.route('/quanly/capnhatkhoahoc', methods=['GET', 'POST', 'DELETE'])
def update_course():
    conn = get_db()
    cursor = conn.cursor()
    
    if request.method == 'POST' :
        course_name = request.form['class_name']
        level = request.form['class_level']
        start_date = request.form['start_date']
        end_date = request.form['end_date']
        #lessons_per_week =  request.form.getlist('days_per_week')
        course_fee = request.form['course_fee']
        description = request.form['description']
        status = request.form['status']
        so_gio_hoc = request.form['so_gio_hoc']
        dayweek = ["Thứ hai", "Thứ ba", "Thứ tư", "Thứ năm", "Thứ sáu", "Thứ bảy", "Chủ nhật"]
        lessons_per_week = [request.form['hour_hai'],  request.form['hour_ba'],request.form['hour_tu'], request.form['hour_nam'] , request.form['hour_sau'], request.form['hour_bay'], request.form['hour_cn']]

        if status == "update":
            course_name = request.form['class_name']
            level = request.form['class_level']
            start_date = request.form['start_date']
            end_date = request.form['end_date']
            #lessons_per_week =  request.form.getlist('days_per_week')
            course_fee = request.form['course_fee']
            description = request.form['description']
            course_id = request.form['course_id']
            so_gio_hoc = request.form['so_gio_hoc']
            dayweek = ["Thứ hai", "Thứ ba", "Thứ tư", "Thứ năm", "Thứ sáu", "Thứ bảy", "Chủ nhật"]
            lessons_per_week = [request.form['hour_hai'],  request.form['hour_ba'],request.form['hour_tu'], request.form['hour_nam'] , request.form['hour_sau'], request.form['hour_bay'], request.form['hour_cn']]
            if level == "IELTS":
                band = request.form['band_score_ielts_update']
            elif level =="TOEIC":
                band = request.form['band_score_toeic_update']
            else:
                band = request.form['band_score_pet_update']

            cursor.execute("UPDATE course SET course_name =?, level =?, start_date=?, end_date=?, course_fee=?, description =?, band = ?, so_gio_hoc =? WHERE id = ?",
                            (course_name , level, start_date, end_date,course_fee, description,  band, so_gio_hoc,course_id))
            conn.commit()
            cursor.execute("delete from course_days where course_id=?", (course_id,) )
            i = 0
            for time in lessons_per_week:
                if len(time) > 0:
                    day = dayweek[i]
                    cursor.execute('INSERT INTO course_days (course_id, day, time) VALUES (?, ?, ?)', (course_id, day, time))
                    conn.commit()
                i = i + 1
            cursor.execute("SELECT * FROM course")
            courses = cursor.fetchall()
            cursor.execute("SELECT * FROM course_days")
            course_days = cursor.fetchall()
            conn.close()
            return render_template('capnhatkhoahoc.html', courses=courses, course_days=course_days)

        if level == "IELTS":
            band = request.form['band_score_ielts']
        elif level =="TOEIC":
            band = request.form['band_score_toeic']
        else:
            band = request.form['band_score_pet']
        #course_id = generate_unique_id()
        cursor.execute('INSERT INTO course (course_name, level, start_date, end_date, course_fee, description, band, so_gio_hoc) VALUES ( ?, ?, ?, ?, ?, ?, ?, ?)',
                    (course_name, level, start_date, end_date, course_fee, description, band, so_gio_hoc))
        conn.commit()
        i = 0
        course_id = cursor.lastrowid
        lessons_per_week = [request.form['hour_hai'],  request.form['hour_ba'],request.form['hour_tu'], request.form['hour_nam'] , request.form['hour_sau'], request.form['hour_bay'], request.form['hour_cn']]
        dayweek = ["Thứ hai", "Thứ ba", "Thứ tư", "Thứ năm", "Thứ sáu", "Thứ bảy", "Chủ nhật"]
        for time in lessons_per_week:
            if len(time) > 0:
                day = dayweek[i]
                cursor.execute('INSERT INTO course_days (course_id, day, time) VALUES (?, ?, ?)', (course_id, day, time))
                conn.commit()
            i = i + 1
        cursor.execute("SELECT * FROM course")
        courses = cursor.fetchall()
        cursor.execute("SELECT * FROM course_days")
        course_days = cursor.fetchall()
        conn.close()
        return render_template('capnhatkhoahoc.html', courses=courses, course_days=course_days)
           
    if request.method == "DELETE":
        data = request.get_json()
        courseId = data.get("courseId")
        cursor.execute("delete from course_days where course_id=?", (courseId,) )
        cursor.execute("delete from course where id=?", (courseId,) )
        conn.commit()
        cursor.execute("SELECT * FROM course")
        courses = cursor.fetchall()
        cursor.execute("SELECT * FROM course_days")
        course_days = cursor.fetchall()
        conn.close()
        return render_template('capnhatkhoahoc.html', courses=courses, course_days=course_days)
    
    cursor.execute("SELECT * FROM course")
    courses = cursor.fetchall()
    cursor.execute("SELECT * FROM course_days")
    course_days = cursor.fetchall()
    conn.close()
    return render_template('capnhatkhoahoc.html', courses=courses, course_days=course_days)
import os
upload_folder = os.path.join('static', 'images')
app.config['UPLOAD'] = upload_folder

@app.route('/quanly/capnhatgiaovien', methods=['GET', 'POST', 'DELETE'])
def update_teacher():
    conn = get_db()
    cursor = conn.cursor()
    if request.method == 'POST':
        full_name = request.form['teacher_name']
        address =   request.form['address']
        phone = request.form['phone']
        birthdate = request.form['birthdate']
        date_hire = request.form['date_hire']
        # Lấy thông tin từ trường dữ liệu bằng cấp
        certificates = request.form.getlist('certificates[]')
        ielts =  request.form.getlist('ielts')
        toeic = request.form.getlist('toeic')
        cam = request.form.getlist('cam')
        cursor.execute('INSERT INTO teachers ( teacher_name, teacher_birthdate, phone, address, Date_Of_Hire) VALUES ( ?, ?, ?, ?, ?)',
                    (full_name, birthdate, phone, address, date_hire))
        conn.commit()
        teacher_id = cursor.lastrowid
        f = request.files.get('teacher_image', '')
        if f:
            upload_folder = 'static/images'
            if not os.path.exists(upload_folder):
                os.makedirs(upload_folder)
            custom_filename = f'{teacher_id}.png'
            f.save(os.path.join(upload_folder, secure_filename(custom_filename)))
        cursor.execute("UPDATE teachers SET avatar =? WHERE teacher_id = ?",(custom_filename ,teacher_id))
        conn.commit()
        if len(ielts) > 0:
            for course in ielts:
                type = 'IELTS'
                cursor.execute('INSERT INTO Teachable_courses (teacher_id, name_of_course, type) VALUES (?, ?, ?)', (teacher_id, course, type))
                conn.commit()
        if len(toeic) > 0:
            for course in toeic:
                type = 'TOEIC'
                cursor.execute('INSERT INTO Teachable_courses (teacher_id, name_of_course, type) VALUES (?, ?, ?)', (teacher_id, course, type))
                conn.commit()
        if len(cam) > 0:
            for course in cam:
                type = 'Tiếng Anh Cambridge'
                cursor.execute('INSERT INTO Teachable_courses (teacher_id, name_of_course, type) VALUES (?, ?, ?)', (teacher_id, course, type))
                conn.commit()
        if len(certificates) > 0:
            for cer in certificates:
                cursor.execute('INSERT INTO certificate (teacher_id, name_cer) VALUES (?, ?)', (teacher_id, cer))
                conn.commit()
        username = f'GV{teacher_id}'
        role = 'GV'
        cursor.execute('INSERT INTO Taikhoan (password, username, role) VALUES (?, ?, ?)', (teacher_id,username ,role))
        conn.commit()
    if request.method == "DELETE":
        data = request.get_json()
        teacherId = data.get("teacherId")
        cursor.execute("delete from teachers where teacher_id=?", (teacherId,) )
        cursor.execute("delete from certificate where teacher_id=?", (teacherId,) )
        cursor.execute("delete from taikhoan where password=?", (teacherId,))
        cursor.execute("delete from Teachable_courses where teacher_id=?", (teacherId,))
        conn.commit()
        image_to_delete = f'static/images/{teacherId}.png'
        if os.path.exists(image_to_delete):
            os.remove(image_to_delete)
        cursor.execute("SELECT * FROM teachers")
        teacher_list = cursor.fetchall()
        cursor.execute("SELECT * FROM certificate")
        certificate_list = cursor.fetchall()
        cursor.execute("SELECT * FROM Teachable_courses")
        teachable_courses_list = cursor.fetchall()
        conn.close()
        return render_template('capnhatgiaovien.html', teacher_list = teacher_list, certificate_list = certificate_list, teachable_courses_list = teachable_courses_list)
    cursor.execute("SELECT * FROM teachers")
    teacher_list = cursor.fetchall()
    cursor.execute("SELECT * FROM certificate")
    certificate_list = cursor.fetchall()
    cursor.execute("SELECT * FROM Teachable_courses")
    teachable_courses_list = cursor.fetchall()
    conn.close()
    #return render_template('capnhatgiaovien.html')

    return render_template('capnhatgiaovien.html', teacher_list = teacher_list, certificate_list = certificate_list, teachable_courses_list = teachable_courses_list)
def convert_time_to_decimal(time_str):
    hours, minutes = map(int, time_str.split(':'))
    decimal_hours = hours + minutes / 60
    return round(decimal_hours, 2)
import pandas as pd

def taolich(course, teacher):
    sorted_teacher = sorted(teacher, key=lambda x: len(x))
    # Khởi tạo dictionary để lưu thông tin giáo viên theo yêu cầu
    teacher_dict = {}
    # Xử lý thông tin từ danh sách course và teacher
    for c in course:
        subject, day, start_time, end_time = c[0], c[1], c[2], c[3]
        for t in teacher:
            teacher_name, *subjects = t
            if subject in subjects and day in teacher_dict:
                # Nếu ngày đã tồn tại trong dictionary
                if teacher_name in teacher_dict[day]:
                    if (start_time, end_time) in teacher_dict[day][teacher_name]:
                        teacher_dict[day][teacher_name][(start_time, end_time)].append(subject)
                    else:
                        teacher_dict[day][teacher_name][(start_time, end_time)] = [subject]
                else:
                    teacher_dict[day][teacher_name] = {(start_time, end_time): [subject]}
            elif subject in subjects:
                # Nếu ngày chưa tồn tại trong dictionary
                teacher_dict[day] = {teacher_name: {(start_time, end_time): [subject]}}
        # Chuyển đổi dữ liệu thành DataFrame
    rows = []
    for day, teachers in teacher_dict.items():
        for teacher, schedule in teachers.items():
            for time_slot, courses in schedule.items():
                start_time, end_time = time_slot
                for course in courses:
                    rows.append([day, start_time, end_time, teacher, course])
    df = pd.DataFrame(rows, columns=['Day', 'Start_time', 'End_time', 'Teacher', 'Course'])
    unique_courses = df['Course'].value_counts()
    courses_appear_once = unique_courses[unique_courses == 1].index.tolist()
    df_new = df[df['Course'].isin(courses_appear_once)]
    # Nhóm theo cột "Course" và "Teacher" và kiểm tra số lượng dòng trong mỗi nhóm
    course_teacher_counts = df.groupby(['Course', 'Teacher']).size().reset_index(name='Count')
    # Lọc ra những khóa học xuất hiện nhiều lần và đều chung giáo viên
    duplicate_courses_same_teacher = course_teacher_counts[course_teacher_counts['Count'] > 1]
    unique_course_teacher_counts = duplicate_courses_same_teacher.drop_duplicates(subset=['Course'], keep=False)
    # Tìm những cột có tên 'Course' và 'Teacher' giống với unique_course_teacher_counts trong df
    for j in range(unique_course_teacher_counts.shape[0]):
        for i in range(df.shape[0]):
            if df['Course'].values[i] == unique_course_teacher_counts['Course'].values[j]:
                row_to_add = pd.DataFrame([df.iloc[i].values], columns=df.columns)
                df_new = pd.concat([df_new, row_to_add],ignore_index=True)
    have_course =  df_new['Teacher'].unique().tolist()
    have_teacher =  df_new['Course'].unique().tolist()

    for t in sorted_teacher:
        if t[0] not in have_course:
            fla = False
            for k in range(1, len(t)):
                if t[k] not in have_course:
                    for i in range(df.shape[0]):
                        if df['Course'].values[i] == t[k] and  df['Teacher'].values[i] == t[0]:
                            row_to_add = pd.DataFrame([df.iloc[i].values], columns=df.columns)
                            df_new = pd.concat([df_new, row_to_add],ignore_index=True)
                            fla = True
                    if fla == True:
                        have_course.append(t[k])
                        have_teacher.append(t[0])
                        break

    if set(have_course) == set(df['Teacher'].unique().tolist()):
        if set(have_teacher) != set(df['Course'].unique().tolist()):
            # Đếm số lần xuất hiện của mỗi giáo viên
            different_elements = set(have_teacher).symmetric_difference(set(df['Course'].unique().tolist()))
            for f in different_elements:
                teachers_for_course = df[df['Course'] == f]['Teacher'].unique().tolist()
                # Lọc các dòng trong df có giáo viên thuộc danh sách teachers_for_course
                filtered_df = df_new[df_new['Teacher'].isin(teachers_for_course)]
                # Đếm số lần xuất hiện của mỗi giáo viên trong danh sách filtered_df
                teacher_counts = filtered_df['Teacher'].value_counts(ascending=True)
                # Lấy danh sách giáo viên theo số lần xuất hiện và sắp xếp
                sorted_teachers = teacher_counts.index.tolist()
                filtered_df = df[(df['Teacher'] == sorted_teachers[0]) & (df['Course'] == f)]
                df_new = pd.concat([df_new, filtered_df],ignore_index=True)
                have_teacher.append(f)
    return df_new
df_all = pd.DataFrame()
@app.route('/quanly/capnhatlichday', methods=['GET', 'POST', 'DELETE'])
def capnhatlichday():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT status FROM need_schfree ORDER BY stt_id DESC LIMIT 1')
    result = cursor.fetchone()
    if result:
        if result['status'] == '0':
            current_status = False
        else: 
            current_status = True
    else:
        current_status = False     
    if request.method == "POST":
        isChecked = request.form.get('isChecked')
        if isChecked == 'false':
            cursor.execute('INSERT INTO need_schfree (status) VALUES (?)', ('0'))
        else:
            cursor.execute('INSERT INTO need_schfree (status) VALUES (?)', ('1'))

    cursor.execute('SELECT * FROM lichday')
    result = cursor.fetchall()
    cursor.execute('SELECT * FROM lichday')
    cursor.execute('SELECT * FROM register_course_teacher')
    regis = cursor.fetchall()
    course = []
    teacher = []
    index = 0
    so_gio_hoc = 0
    khoahocDK = []
    cursor.execute('SELECT * FROM course')
    cacKH = []
    a = cursor.fetchall()
    for f in a:
        cacKH.append(f['id'])
    tea = []
    cursor.execute('SELECT * FROM teachers')
    cacGV = []
    a = cursor.fetchall()
    for f in a:
            cacGV.append(f['teacher_id'])
    for i in regis:
            cursor.execute('SELECT * FROM course_days where course_id = ?', (i['course_id'],))
            lich_KH = cursor.fetchall()
            maKH = i['course_id']
            khoahocDK.append(maKH)
            cursor.execute('SELECT so_gio_hoc FROM course where id = ?', (i['course_id'],))
            so_gio_hoc = cursor.fetchone()
            for j in lich_KH:
                thu = j['day']
                gio_bat_dau = j['time']
                gio_ket_thuc = convert_time_to_decimal(gio_bat_dau) + int(so_gio_hoc['so_gio_hoc'])
                course.append([maKH, thu, convert_time_to_decimal(gio_bat_dau), gio_ket_thuc])
            teacher.append([i['teacher_id'], i['course_id']])
            tea.append(i['teacher_id'])

        
    if len(cacKH) != len(khoahocDK):
            mess = "Những khóa học chưa có giáo viên đăng ký:"
            for i in cacKH:
                if i not in khoahocDK:
                    mess = mess + " mã "+str(i) + " "
    else:
            mess = "Tất cả các khóa học đã được đăng ký"
        
    if len(cacGV) != len(tea):
            mess1 = "Những giáo viên chưa đăng ký:"
            for i in cacGV:
                if i not in tea:
                    mess1 = mess1 + " mã " + str(i) + " "
    else:
            mess1 = "Tất cả các giáo viên đã được đăng ký"

    df = taolich(course, teacher)
    df_sorted = df.sort_values(by='Day', key=lambda x: x.map({'Thứ hai':0, 'Thứ ba':1, 'Thứ tư':2, 'Thứ năm':3, 'Thứ sáu':4, 'Thứ bảy':5, 'Chủ nhật':6}))
    new_column_names = ["Thứ", "Giờ bắt đầu", "Giờ kết thúc", "Giáo viên đảm nhận", "Khóa học"]
    df_sorted.reset_index(drop=True, inplace=True)
    df_sorted.columns = new_column_names
    cursor.execute('DELETE FROM lichday')
    conn.commit()
    for i in range(len(df_sorted["Giáo viên đảm nhận"].values)):
        cursor.execute('INSERT INTO lichday (magv, makhoahoc) VALUES (?, ?)', (int(df_sorted["Giáo viên đảm nhận"].values[i]), int(df_sorted["Khóa học"].values[i]),))
        conn.commit()
    df_all = df_sorted
    return render_template('capnhatlichday.html', current_status=current_status, teacher = teacher, course = course, table=df_sorted.to_html(classes='table table-striped'), mess = mess, mess1 = mess1)

@app.route('/giaovien/xemlichday', methods=['POST', 'GET'])
def xemlichday():
    conn = get_db()
    cursor = conn.cursor()
    user_id = session.get('user_id')
    if user_id != None:
        cursor.execute('SELECT makhoahoc FROM lichday WHERE magv = ?', (user_id,))
        is_register1 = cursor.fetchall()
        is_register = []
        if len(is_register1) == 0:
            mess = "Bạn hiện tại chưa được phân lịch dạy khóa học nào"
            return render_template('xemlichday.html', mess = mess, ischeck = '0')
        else:
            for j in is_register1:
                is_register.append(j['makhoahoc'])
            cursor.execute('SELECT * FROM teachers WHERE teacher_id = ?', (user_id,))
            teacher = cursor.fetchone()
            cursor.execute('SELECT name_of_course FROM Teachable_courses WHERE teacher_id = ?', (user_id,))
            tenkhoahoc = cursor.fetchall()
            thongtinkhoahoc = []
            for i in tenkhoahoc:
                cursor.execute('SELECT * FROM course WHERE band = ?', (i['name_of_course'],))
                infor_course = cursor.fetchall()
                if infor_course != []:
                    days = []
                    havecourse = 1
                    for row in infor_course:
                        id_KH = row['id']
                        cursor.execute('SELECT * FROM course_days WHERE course_id = ?', (id_KH,))
                        day = cursor.fetchall()
                        for d in day:
                            days.append(list(d[1:-1]))
                        thongtinkhoahoc.append(list(row[:]) + [list(days[:])])
            conn.close()
            new_column_names = ["Mã khóa học", "Tên khóa học", "Trình độ", "band điểm","Ngày bắt đầu", "Học phí", "Mô tả", "Ngày kết thúc", "9", "Số giờ dạy 1 buổi", "Lịch cụ thể 1 tuần"]
            df = pd.DataFrame(thongtinkhoahoc, columns=new_column_names)
            df = df.drop('Mô tả', axis=1)
            df = df.drop('Học phí', axis=1)
            df = df.drop('9', axis=1)
            return render_template('xemlichday.html', name_teacher= teacher[1], ischeck = '1',  table=df.to_html(classes='table table-striped'))
    else:
        return redirect(url_for('login'))



from flask import redirect, url_for, jsonify
@app.route('/giaovien/dangkylichday', methods=['POST', 'GET'])
def dangkylichday():
    conn = get_db()
    cursor = conn.cursor()
    user_id = session.get('user_id')

    if request.method == "POST":
        data = request.get_json()
        course_infor = data.get("info")
        cancel1 = data.get("cancel")
        for j in cancel1:
            if j not in course_infor:
                cursor.execute("delete from register_course_teacher where course_id=?", (j,) )
                conn.commit()
        for i in course_infor:
            if i not in cancel1:
                user_id = int(user_id)
                course_id = int(i['course_id'])
                cursor.execute('INSERT INTO register_course_teacher (teacher_id, course_id) VALUES (?, ?)', (user_id, course_id,))
                conn.commit()
        return jsonify({"redirect": url_for('khoahocdangky')})
    if user_id != None:
        cursor.execute('SELECT course_id FROM register_course_teacher WHERE teacher_id = ?', (user_id,))
        is_register1 = cursor.fetchall()
        is_register = []
        for j in is_register1:
            is_register.append(j['course_id'])
        cursor.execute('SELECT * FROM teachers WHERE teacher_id = ?', (user_id,))
        teacher = cursor.fetchone()

        cursor.execute('SELECT status FROM need_schfree ORDER BY stt_id DESC LIMIT 1')
        ischeck = cursor.fetchone()

        cursor.execute('SELECT name_of_course FROM Teachable_courses WHERE teacher_id = ?', (user_id,))
        tenkhoahoc = cursor.fetchall()
        thongtinkhoahoc = []
        havecourse = 0
        for i in tenkhoahoc:
            cursor.execute('SELECT * FROM course WHERE band = ?', (i['name_of_course'],))
            infor_course = cursor.fetchall()
            if len(infor_course) != 0:
                days = []
                havecourse = 1
                for row in infor_course:
                    id_KH = row['id']
                    cursor.execute('SELECT * FROM course_days WHERE course_id = ?', (id_KH,))
                    day = cursor.fetchall()
                    for d in day:
                        days.append(list(d[1:-1]))
                    thongtinkhoahoc.append(list(row[:]) + [list(days[:])])
        conn.close()
        return render_template('dangkylichday.html', name_teacher= teacher[1], user_id = user_id, ischeck = ischeck['status'], tenkhoahoc= thongtinkhoahoc, havecourse = havecourse, is_register = is_register)
    else:
        return redirect(url_for('login'))
    
@app.route('/giaovien/khoahocdangky', methods=['POST', 'GET'])
def khoahocdangky():
    conn = get_db()
    cursor = conn.cursor()
    user_id = session.get('user_id')
    if user_id != None:
        cursor.execute('SELECT course_id FROM register_course_teacher WHERE teacher_id = ?', (user_id,))
        thongtinkhoahoc = []
        is_register1 = cursor.fetchall()
        is_register = []
        course = []
        for j in is_register1:
            is_register.append(j['course_id'])
            cursor.execute('SELECT * FROM course WHERE id = ?', (j['course_id'],))
            is_register1 = cursor.fetchone()
            if is_register1["id"] not in thongtinkhoahoc:
                thongtinkhoahoc.append(is_register1["id"])
                course.append(is_register1)

        conn.close()
        return render_template('khoahocdangky.html',  user_id = user_id, tenkhoahoc= thongtinkhoahoc,courses = course)
    else:
        return redirect(url_for('login'))

from flask_cors import CORS

if __name__ == '__main__':
    
    app.run(debug=True)
    CORS(app)

