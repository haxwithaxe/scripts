set VBC=\WINDOWS\Microsoft.NET\Framework64\v2.0.50727\vbc.exe
set PLATFORM=/platform:x64
set Refs=/reference:"C:\Program Files\AntennaHouse\AHFormatterV52\XfoDotNet20Ctl52.dll"
set Debug=/debug+ /debug:full

%VBC% %PLATFORM% %Debug% %Refs% /optimize- %*