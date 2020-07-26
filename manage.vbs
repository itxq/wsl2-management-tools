bat = Left(WScript.ScriptFullName, InStrRev(WScript.ScriptFullName, "\")) & ".wsl2_management_tools\manage.bat"
arg = ""

If WScript.Arguments.Count > 1 Then
    arg = WScript.Arguments(1)
End If

CreateObject("WScript.Shell").Run """" & bat & """ """ & arg & """", 0, False
