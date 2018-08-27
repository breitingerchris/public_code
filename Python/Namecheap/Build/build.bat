python ../serial/serial.py
set content=
for /f "delims=" %%i in ('type data.txt') do set content=%%i
python ../Obf/pyobfuscate.py ../namecheap.py > %content%.py
pyinstaller -F -c --icon=icon.ico -n "Namecheap" %content%.py
del %content%.py
python ../serial/serial.py
set content=
for /f "delims=" %%i in ('type data.txt') do set content=%%i
python ../Obf/pyobfuscate.py ../regcheck.py > %content%.py
pyinstaller -F -c --icon=icon.ico -n "Reg Check" %content%.py
del %content%.py
move E:\Python\Namecheap\Build\dist\namecheap.exe E:\Python\Namecheap\Dist\Namecheap.exe
move "E:\Python\Namecheap\Build\dist\Reg Check.exe" "E:\Python\Namecheap\Dist\Reg Check.exe"
python ../serial/serial.py
move data.txt E:\Python\Namecheap\Dist\data.txt
