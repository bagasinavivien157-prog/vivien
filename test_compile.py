import py_compile

py_compile.compile('libatt_db.py', doraise=True)
py_compile.compile('libatt_ops.py', doraise=True)
py_compile.compile('main_libatt.py', doraise=True)
print('OK')
