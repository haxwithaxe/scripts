For $subkey In HKEY_LOCAL_MACHINE\System\CurrentControlSet\Services\
	Do
		RegRead(HKEY_LOCAL_MACHINE\System\CurrentControlSet\Services\$subkey, $path)
		