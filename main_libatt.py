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
#
# CRUD: Create, Read, Update, Delete na may confirmation. Exit na nagsasara ng koneksyon.

import libatt_db
import libatt_ops


def menu():
    print("\n" + "="*56)
    print("   LIBRARY ATTENDANCE & USAGE SYSTEM")
    print("="*56)
    print("  [1] Library Attendance (Pumasok sa Library) - CREATE")
    print("  [2] Library Exit (Lumabas sa Library) - UPDATE")
    print("  [3] Tingnan ang Mga Nasa Library Ngayon - READ")
    print("  [4] Leaderboard - Pinaka-Marami ang Punta sa Library - READ")
    print("  [5] Library History ng Estudyante - READ")
    print("  [6] PC Status (Available / In-Use) - READ")
    print("  [7] Magdagdag ng Estudyante sa Masterlist - CREATE")
    print("  [8] Magdagdag ng Libro - CREATE")
    print("  [9] Magdagdag ng PC Unit - CREATE")
    print("  [10] I-update ang Impormasyon (Estudyante/Libro/PC) - UPDATE")
    print("  [11] Tanggalin ang Record (May Konfirmasyon) - DELETE")
    print("  [0] Lumabas - EXIT")
    print("="*56)


def main():
    ok, msg = libatt_db.test_connection()
    print(f"\n  {msg}")
    if not ok:
        print("  Paki-import muna ang 'schema_libatt.sql' sa XAMPP/MySQL.")
        return
    while True:
        menu()
        ch = input("\n  Ano'ng aksyon ang gagawin? : ").strip()
        if ch == "1":
            libatt_ops.time_in()
        elif ch == "2":
            libatt_ops.time_out()
        elif ch == "3":
            libatt_ops.inside_now()
        elif ch == "4":
            libatt_ops.leaderboard()
        elif ch == "5":
            libatt_ops.student_history()
        elif ch == "6":
            libatt_ops.pc_status()
        elif ch == "7":
            libatt_ops.add_student()
        elif ch == "8":
            libatt_ops.add_book()
        elif ch == "9":
            libatt_ops.add_pc()
        elif ch == "10":
            libatt_ops.update_record()
        elif ch == "11":
            libatt_ops.delete_record()
        elif ch == "0":
            print("\n  Isinasara ang koneksyon sa database...")
            print("  Program terminated successfully.")
            print("  Sige, paalam!")
            break
        else:
            print("\n  * Hindi tamang pagpili.")


if __name__ == "__main__":
    main()
