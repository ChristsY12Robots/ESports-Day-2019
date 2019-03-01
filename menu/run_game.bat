IF %3% == 1 ( rem dubug mode. 
	powershell.exe -NoExit -Command "cd C:/Python35/Scripts/; 	pip install pygame; 	cd %1; 	py -3.5 %2"
) ELSE ( rem release mode.
	SETCONSOLE /minimize
	powershell.exe -WindowStyle Hidden -Command "cd C:/Python35/Scripts/; 	pip install pygame; 	cd %1; 	py -3.5 %2"
)

 
