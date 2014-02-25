set /a count=10

set fofile=test.fo

set outfile=out.pdf

set startdate=%date%_%time%

:loop

AHFCmd.exe -x 4 -d %fofile% -o %outfile%

set /a count-=1

if %count% GTR 0 goto loop

echo "started: "%startdate%" ended: "%date%_%time%
