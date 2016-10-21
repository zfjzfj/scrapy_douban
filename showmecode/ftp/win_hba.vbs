On Error Resume Next 
strComputer = "." 
Set objWMIService = GetObject("winmgmts:\\" & strComputer & "\root\WMI") 
Set colItems = objWMIService.ExecQuery("Select * from MSFC_FCAdapterHBAAttributes",,48) 
for each objWMIHBA in colItems
	WScript.echo objWMIHBA.ModelDescription
next

Set objWMIService = GetObject("winmgmts:\\" & strComputer & "\root\cimv2") 

WScript.echo "BIOS:"
Set colItems = objWMIService.ExecQuery("Select * from Win32_BIOS",,48)
for each objWMISystem in colItems
	WScript.echo objWMISystem.Manufacturer
	WScript.echo objWMISystem.Description
	WScript.echo objWMISystem.SerialNumber
next

WScript.echo "MotherBoard:"
Set colItems = objWMIService.ExecQuery("Select * from Win32_MotherboardDevice",,48)
for each objWMISystem in colItems
	WScript.echo objWMISystem.Manufacturer
	WScript.echo objWMISystem.DeviceID
	WScript.echo objWMISystem.SystemName
next

WScript.echo "BaseBoard:"
Set colItems = objWMIService.ExecQuery("Select * from Win32_BaseBoard",,48)
for each objWMISystem in colItems
	WScript.echo objWMISystem.Manufacturer
	WScript.echo objWMISystem.Model
	WScript.echo objWMISystem.Description
	WScript.echo objWMISystem.SerialNumber
	WScript.echo objWMISystem.Version
next


