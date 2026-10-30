# ===== PROBLEMA =====
# Hindi na-track ng library kung sino ang regular na pumupunta, kung ano libro ang hihiramin,
# kung anong PC ang ginagamit ng mga estudyante, at hindi rin nila alam kung sino ang
# pinaka-active na bumibisita sa library para sa rewards.
#
# ===== SOLUSYON =====
# Library Attendance & Usage System na nagre-record ng pagpasok/paglabas ng estudyante,
# nagtatanong kung gagamit ba ng PC o may hihiramin bang libro, nag-a-assign ng available na PC,
# nagtatala kung sino ang gumagamit ng aling PC, nagbibigay ng points kada bisita,
# at may leaderboard para makita ang pinaka-marami ang punta sa library para sa reward.

import re
from datetime import datetime

import mysql.connector

import libatt_db


def req(msg):
    while True:
        v = input(msg).strip()
        if v == "":
            print("  * Hindi puwede blangko.")
            continue
        return v


def nowtime(label):
    print(f"  [{label}] ENTER kung ngayon na, o ilagay ang HH:MM (24 oras)")
    a = input("    >> ").strip()
    if a == "":
        return datetime.now().strftime("%H:%M")
    if re.match(r"^([01]\d|2[0-3]):([0-5]\d)$", a):
        return a
    print("  * Mali ang format.")
    return nowtime(label)


def card_student(s):
    print("\n" + "="*46)
    print(f"  STUDENT ID : {s['student_id']}")
    print("="*46)
    print(f"  Buong Pangalan : {s['full_name']}")
    print(f"  Baitang/Seksyon: {s['grade_level']} - {s['section']}")
    print(f"  Kabuuang Punta : {s['total_visits']} | Kabuuang Points: {s['total_points']}")
    print("="*46)


def card_visit(v):
    print("\n" + "="*46)
    print(f"  VISIT ID  : {v['visit_id']}")
    print("="*46)
    print(f"  Student ID     : {v['student_id']} | {v['full_name']}")
    print(f"  Baitang/Seksyon: {v['grade_level']} - {v['section']}")
    print(f"  Petsa           : {v['visit_date']}")
    print(f"  Time In         : {v['time_in']}")
    print(f"  Time Out        : {v['time_out'] or '--- NASA LOOB PA ---'}")
    print(f"  Libro           : {v['book_id'] or 'WALA'}")
    print(f"  Gumamit ng PC   : {'OO' if v['using_pc'] else 'HINDI'}")
    if v['using_pc']:
        print(f"  PC na Ginamit   : {v['pc_name']}")
    print(f"  Points nakuha   : {v['points_earned']}")
    print(f"  Status          : {v['status']}")
    print("="*46)


def add_student():
    print("\n--- MAGDAGDAG NG ESTUDYANTE SA MASTERLIST ---")
    sid = req("  Student ID: ").upper()
    try:
        exist = libatt_db.find_student(sid)
    except mysql.connector.Error as e:
        print(f"  [MALI] {e}")
        return
    if exist:
        print("  [PAALALA] Mayroon nang estudyante na may ganitong Student ID.")
        card_student(exist)
        return
    name = req("  Buong Pangalan og apledo: ")
    gl = req("  ano year? (hal. first year): ")
    sec = req("  Seksyon (hal. BSIS A): ")
    try:
        libatt_db.add_student(sid, name, gl, sec)
        print("\n  [TAPOS NA] Naidagdag na ang estudyante sa masterlist.")
    except mysql.connector.Error as e:
        print(f"  [MALI] {e}")


def add_book():
    print("\n--- MAGDAGDAG NG LIBRO ---")
    bid = req("  Book ID / Accession No.: ").upper()
    try:
        exist = libatt_db.find_book(bid)
    except mysql.connector.Error as e:
        print(f"  [MALI] {e}")
        return
    if exist:
        print("  [PAALALA] Mayroon nang libro na may ganitong Book ID.")
        print(f"  Pamagat: {exist['title']} | May-akda: {exist['author']} | Available: {exist['available']}")
        return
    title = req("  Pamagat ng Libro: ")
    author = req("  May-akda: ")
    try:
        libatt_db.add_book(bid, title, author)
        print("\n  [TAPOS NA] Naidagdag na ang libro sa library.")
    except mysql.connector.Error as e:
        print(f"  [MALI] {e}")


def add_pc():
    print("\n--- MAGDAGDAG NG PC UNIT ---")
    pc = req("  PC Name (hal. PC1, PC2, PC3): ").upper()
    try:
        libatt_db.add_pc(pc)
        print(f"\n  [TAPOS NA] Naidagdag na ang {pc} sa listahan ng PC.")
    except mysql.connector.Error as e:
        if "Duplicate" in str(e):
            print("  [PAALALA] Mayroon nang ganitong PC sa system.")
        else:
            print(f"  [MALI] {e}")


def time_in():
    print("\n--- LIBRARY ATTENDANCE (PUMASOK SA LIBRARY) ---")
    sid = req("  Student ID: ").upper()
    try:
        s = libatt_db.find_student(sid)
    except mysql.connector.Error as e:
        print(f"  [MALI] {e}")
        return
    if not s:
        print("  [WALA] Hindi pa naka-register ang estudyante sa masterlist.")
        print("  Paki-add muna sa [7] Magdagdag ng Estudyante sa Masterlist.")
        return
    try:
        openv = libatt_db.get_open_visit(sid)
    except mysql.connector.Error as e:
        print(f"  [MALI] {e}")
        return
    if openv:
        print("  [PAALALA] Nasa loob pa siya ng library. Kailangan muna siyang mag-Library Exit.")
        card_visit(openv)
        return
    card_student(s)
    today = datetime.now().date()
    tin = nowtime("Oras ng Pagpasok")
    book_id = None
    ans_book = input("  May hihiramin ka bang libro? (oo/hindi): ").strip().lower()
    if ans_book in ("oo", "o", "yes", "y"):
        try:
            books = libatt_db.list_books()
        except mysql.connector.Error as e:
            print(f"  [MALI] {e}")
            return
        if not books:
            print("  [WALA] Walang libro sa library.")
        else:
            print("\n--- LISTAHAN NG MGA LIBRO ---")
            for b in books:
                stat = "AVAILABLE" if b['available'] else "HINDI AVAILABLE"
                print(f"  [{b['book_id']}] {b['title']} - {b['author']} | {stat}")
            bid = req("  Book ID na hihiramin: ").upper()
            try:
                b = libatt_db.find_book(bid)
            except mysql.connector.Error as e:
                print(f"  [MALI] {e}")
                return
            if not b:
                print("  [WALA] Hindi matagpuan ang libro.")
            elif not b['available']:
                print("  [PAALALA] Hindi na available ang libro na ito.")
            else:
                book_id = bid
                print(f"  [OK] Napili ang '{b['title']}'")
    using_pc = 0
    pc_name = None
    ans_pc = input("  Gagamit ka ba ng PC? (oo/hindi): ").strip().lower()
    if ans_pc in ("oo", "o", "yes", "y"):
        try:
            av = libatt_db.list_available_pc()
        except mysql.connector.Error as e:
            print(f"  [MALI] {e}")
            return
        if not av:
            print("  [WALA] Walang available na PC sa ngayon.")
        else:
            print("\n--- AVAILABLE NA PC ---")
            for p in av:
                print(f"  {p['pc_name']}")
            pcn = req("  Aling PC ang gagamitin? (hal. PC1): ").upper()
            try:
                ok_assign = libatt_db.assign_pc(pcn)
            except mysql.connector.Error as e:
                print(f"  [MALI] {e}")
                return
            if ok_assign:
                using_pc = 1
                pc_name = pcn
                print(f"  [OK] Na-assign na ang {pc_name}")
            else:
                print("  [PAALALA] Hindi ma-assign ang PC na ito. Maaaring ginagamit na ito o hindi available.")
    points_earned = 1
    if using_pc:
        points_earned = 2
    try:
        if book_id:
            libatt_db.borrow_book(book_id)
        visit_id = libatt_db.time_in_visit(sid, today, tin, book_id, using_pc, pc_name, points_earned)
        if using_pc and pc_name:
            libatt_db.start_pc_usage(visit_id, sid, pc_name, tin)
        libatt_db.update_student_points_visits(sid, points_earned)
        print("\n" + "="*46)
        print(f"  [TAPOS NA] Na-record na ang pagpasok sa Library.")
        print(f"  Points na nakuha sa visit na ito: +{points_earned}")
        if book_id:
            print(f"  Hiniram na Libro: {book_id}")
        if using_pc and pc_name:
            print(f"  PC na Ginamit: {pc_name}")
        print("="*46)
    except mysql.connector.Error as e:
        print(f"  [MALI] {e}")


def time_out():
    print("\n--- LIBRARY EXIT (LUMABAS SA LIBRARY) ---")
    sid = req("  Student ID: ").upper()
    try:
        openv = libatt_db.get_open_visit(sid)
    except mysql.connector.Error as e:
        print(f"  [MALI] {e}")
        return
    if not openv:
        print("  [PAALALA] Wala siyang active na visit sa library o nakalabas na siya.")
        return
    card_visit(openv)
    tout = nowtime("Oras ng Paglabas")
    try:
        libatt_db.time_out_visit(openv['visit_id'], tout)
        if openv.get('using_pc') and openv.get('pc_name'):
            libatt_db.end_pc_usage(openv['visit_id'], tout)
            libatt_db.free_pc(openv['pc_name'])
            print(f"  [OK] Na-free na ang {openv['pc_name']} at available na ulit ito.")
        if openv.get('book_id'):
            libatt_db.return_book(openv['book_id'])
            print(f"  [OK] Na-record na ang pagbalik ng libro ({openv['book_id']}).")
        print("\n  [TAPOS NA] Na-record na ang paglabas sa Library.")
    except mysql.connector.Error as e:
        print(f"  [MALI] {e}")


def inside_now():
    try:
        rows = libatt_db.get_inside_visits()
    except mysql.connector.Error as e:
        print(f"  [MALI] {e}")
        return
    if not rows:
        print("\n  Walang estudyante sa loob ng library sa ngayon.")
        return
    print("\n--- MGA NASA LOOB NG LIBRARY NGAYON ---")
    for r in rows:
        pcinfo = f" | PC:{r['pc_name']}" if r['using_pc'] and r['pc_name'] else ""
        binfo = f" | Libro:{r['book_id']}" if r['book_id'] else ""
        print(f"  [Visit#{r['visit_id']}] [{r['student_id']}] {r['full_name']} | {r['grade_level']}-{r['section']} | Time In:{r['time_in']}{pcinfo}{binfo}")


def leaderboard():
    try:
        rows = libatt_db.get_leaderboard()
    except mysql.connector.Error as e:
        print(f"  [MALI] {e}")
        return
    if not rows:
        print("\n  Wala pang data sa leaderboard.")
        return
    print("\n--- LEADERBOARD - PINAKA-MARAMI ANG PUNTA SA LIBRARY ---")
    rank = 0
    for r in rows:
        rank += 1
        print(f"  #{rank} | [{r['student_id']}] {r['full_name']} | {r['grade_level']}-{r['section']} | Punta:{r['total_visits']} | Points:{r['total_points']}")


def student_history():
    sid = req("  Student ID: ").upper()
    try:
        s = libatt_db.find_student(sid)
    except mysql.connector.Error as e:
        print(f"  [MALI] {e}")
        return
    if not s:
        print("  [WALA] Hindi matagpuan ang estudyante.")
        return
    card_student(s)
    try:
        rows = libatt_db.get_student_history(sid)
    except mysql.connector.Error as e:
        print(f"  [MALI] {e}")
        return
    if not rows:
        print("\n  Wala pang history ng pagbisita sa library.")
        return
    print("\n--- LIBRARY HISTORY NG ESTUDYANTE ---")
    for r in rows:
        tout = r['time_out'] or 'NASA LOOB PA'
        pcinfo = f" | PC:{r['pc_name']}" if r['using_pc'] and r['pc_name'] else ""
        binfo = f" | Libro:{r['book_id']}" if r['book_id'] else ""
        print(f"  {r['visit_date']} | In:{r['time_in']} | Out:{tout} | +{r['points_earned']} pts{pcinfo}{binfo} | {r['status']}")


def pc_status():
    try:
        rows = libatt_db.list_pc_status()
    except mysql.connector.Error as e:
        print(f"  [MALI] {e}")
        return
    if not rows:
        print("\n  Wala pang PC unit na na-add sa system.")
        return
    print("\n--- PC STATUS (AVAILABLE / IN-USE) ---")
    for p in rows:
        print(f"  {p['pc_name']} | {p['status']}")


def update_record():
    print("\n--- I-UPDATE ANG IMPORMASYON ---")
    print("  [1] I-update ang Impormasyon ng Estudyante")
    print("  [2] I-update ang Impormasyon ng Libro")
    print("  [3] I-update ang Pangalan ng PC Unit")
    print("  [0] Bumalik")
    ch = input("\n  Ano'ng pipiliin mo? : ").strip()
    if ch == "1":
        sid = req("  Student ID na iu-update: ").upper()
        try:
            s = libatt_db.find_student(sid)
        except mysql.connector.Error as e:
            print(f"  [MALI] {e}")
            return
        if not s:
            print("  [WALA] Hindi matagpuan ang estudyante.")
            return
        card_student(s)
        print("  (Pindutin lang ang ENTER kung ayaw mong baguhin ang field)")
        name = input(f"  Bagong Buong Pangalan [{s['full_name']}]: ").strip() or s['full_name']
        gl = input(f"  Bagong Baitang [{s['grade_level']}]: ").strip() or s['grade_level']
        sec = input(f"  Bagong Seksyon [{s['section']}]: ").strip() or s['section']
        try:
            ok = libatt_db.update_student(sid, name, gl, sec)
            if ok:
                print("\n  [TAPOS NA] Na-update na ang impormasyon ng estudyante.")
            else:
                print("  [PAALALA] Walang nabago o hindi matagpuan ang rekord.")
        except mysql.connector.Error as e:
            print(f"  [MALI] {e}")
    elif ch == "2":
        bid = req("  Book ID na iu-update: ").upper()
        try:
            b = libatt_db.find_book(bid)
        except mysql.connector.Error as e:
            print(f"  [MALI] {e}")
            return
        if not b:
            print("  [WALA] Hindi matagpuan ang libro.")
            return
        print("\n" + "="*46)
        print(f"  BOOK ID : {b['book_id']}")
        print("="*46)
        print(f"  Pamagat : {b['title']}")
        print(f"  May-akda: {b['author']}")
        print(f"  Available: {'OO' if b['available'] else 'HINDI'}")
        print("="*46)
        print("  (Pindutin lang ang ENTER kung ayaw mong baguhin ang field)")
        title = input(f"  Bagong Pamagat [{b['title']}]: ").strip() or b['title']
        author = input(f"  Bagong May-akda [{b['author']}]: ").strip() or b['author']
        try:
            ok = libatt_db.update_book(bid, title, author)
            if ok:
                print("\n  [TAPOS NA] Na-update na ang impormasyon ng libro.")
            else:
                print("  [PAALALA] Walang nabago o hindi matagpuan ang rekord.")
        except mysql.connector.Error as e:
            print(f"  [MALI] {e}")
    elif ch == "3":
        try:
            rows = libatt_db.list_pc_status()
        except mysql.connector.Error as e:
            print(f"  [MALI] {e}")
            return
        if not rows:
            print("\n  Wala pang PC unit na na-add sa system.")
            return
        print("\n--- PC STATUS ---")
        for p in rows:
            print(f"  {p['pc_name']} | {p['status']}")
        old = req("  Lumang PC Name na iu-update: ").upper()
        try:
            pc = libatt_db.find_pc(old)
        except mysql.connector.Error as e:
            print(f"  [MALI] {e}")
            return
        if not pc:
            print("  [WALA] Hindi matagpuan ang PC unit.")
            return
        if pc['status'] == 'IN-USE':
            print("  [PAALALA] Hindi pwedeng i-update ang pangalan ng PC na kasalukuyang IN-USE.")
            return
        newn = req("  Bagong PC Name (hal. PC10): ").upper()
        try:
            ok = libatt_db.update_pc_name(old, newn)
            if ok:
                print(f"\n  [TAPOS NA] Na-update na ang pangalan ng PC mula {old} patungong {newn}.")
            else:
                print("  [PAALALA] Walang nabago o hindi matagpuan ang rekord.")
        except mysql.connector.Error as e:
            if "Duplicate" in str(e):
                print("  [MALI] Mayroon nang ganitong PC Name sa system.")
            else:
                print(f"  [MALI] {e}")
    elif ch == "0":
        return
    else:
        print("\n  * Hindi tamang pagpili.")


def delete_record():
    print("\n--- TANGGALIN ANG RECORD (MAY KONFIRMASYON) ---")
    print("  [1] Tanggalin ang Estudyante")
    print("  [2] Tanggalin ang Libro")
    print("  [3] Tanggalin ang PC Unit")
    print("  [0] Bumalik")
    ch = input("\n  Ano'ng pipiliin mo? : ").strip()
    if ch == "1":
        sid = req("  Student ID na tatanggalin: ").upper()
        try:
            s = libatt_db.find_student(sid)
        except mysql.connector.Error as e:
            print(f"  [MALI] {e}")
            return
        if not s:
            print("  [WALA] Hindi matagpuan ang estudyante.")
            return
        card_student(s)
        try:
            cnt = libatt_db.count_student_visits(sid)
        except mysql.connector.Error as e:
            print(f"  [MALI] {e}")
            return
        if cnt > 0:
            print(f"  [PAALALA] May {cnt} na library visit record ang estudyante na ito.")
            print("  Hindi maaring tanggalin ang estudyante upang mapanatili ang history ng library.")
            return
        konf = input("  Sigurado ka bang tanggalin ang estudyante na ito? (oo/hindi): ").strip().lower()
        if konf not in ("oo", "o", "yes", "y"):
            print("  Kinansela.")
            return
        try:
            ok = libatt_db.delete_student(sid)
            if ok:
                print("\n  [TINANGGAL] Natanggal na ang estudyante sa masterlist.")
            else:
                print("  [MALI] Hindi nagtagumpay ang pagtanggal.")
        except mysql.connector.Error as e:
            print(f"  [MALI] {e}")
    elif ch == "2":
        bid = req("  Book ID na tatanggalin: ").upper()
        try:
            b = libatt_db.find_book(bid)
        except mysql.connector.Error as e:
            print(f"  [MALI] {e}")
            return
        if not b:
            print("  [WALA] Hindi matagpuan ang libro.")
            return
        print("\n" + "="*46)
        print(f"  BOOK ID : {b['book_id']}")
        print("="*46)
        print(f"  Pamagat : {b['title']}")
        print(f"  May-akda: {b['author']}")
        print("="*46)
        try:
            cnt = libatt_db.count_book_visits(bid)
        except mysql.connector.Error as e:
            print(f"  [MALI] {e}")
            return
        if cnt > 0:
            print(f"  [PAALALA] Nagamit na ang libro na ito sa {cnt} na visit record.")
            print("  Hindi maaring tanggalin ang libro upang mapanatili ang history ng library.")
            return
        konf = input("  Sigurado ka bang tanggalin ang libro na ito? (oo/hindi): ").strip().lower()
        if konf not in ("oo", "o", "yes", "y"):
            print("  Kinansela.")
            return
        try:
            ok = libatt_db.delete_book(bid)
            if ok:
                print("\n  [TINANGGAL] Natanggal na ang libro sa listahan.")
            else:
                print("  [MALI] Hindi nagtagumpay ang pagtanggal.")
        except mysql.connector.Error as e:
            print(f"  [MALI] {e}")
    elif ch == "3":
        try:
            rows = libatt_db.list_pc_status()
        except mysql.connector.Error as e:
            print(f"  [MALI] {e}")
            return
        if not rows:
            print("\n  Wala pang PC unit na na-add sa system.")
            return
        print("\n--- PC STATUS ---")
        for p in rows:
            print(f"  {p['pc_name']} | {p['status']}")
        pc = req("  PC Name na tatanggalin: ").upper()
        try:
            p = libatt_db.find_pc(pc)
        except mysql.connector.Error as e:
            print(f"  [MALI] {e}")
            return
        if not p:
            print("  [WALA] Hindi matagpuan ang PC unit.")
            return
        if p['status'] == 'IN-USE':
            print("  [PAALALA] Hindi pwedeng tanggalin ang PC na kasalukuyang IN-USE.")
            return
        konf = input("  Sigurado ka bang tanggalin ang PC unit na ito? (oo/hindi): ").strip().lower()
        if konf not in ("oo", "o", "yes", "y"):
            print("  Kinansela.")
            return
        try:
            ok = libatt_db.delete_pc(pc)
            if ok:
                print("\n  [TINANGGAL] Natanggal na ang PC unit sa listahan.")
            else:
                print("  [MALI] Hindi nagtagumpay ang pagtanggal.")
        except mysql.connector.Error as e:
            print(f"  [MALI] {e}")
    elif ch == "0":
        return
    else:
        print("\n  * Hindi tamang pagpili.")
