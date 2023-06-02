Function ModifyFilename(ByVal filename)
    Dim parts, firstField

    ' Split the filename into parts based on underscore (_) separator
    parts = Split(filename, "_")

    ' Get the first field
    firstField = parts(0)
    
    ' Check if the first field ends with a number
    If Not IsNumeric(Right(firstField, 1)) Then
        ' Append "1" to the first field
        parts(0) = firstField & "1"
    End If
    
    ' Reconstruct the modified filename
    ModifyFilename = Join(parts, "_")
End Function

' Usage example
Dim filename
filename = "file1_example.txt"
WScript.Echo ModifyFilename(filename) ' Output: file1_example.txt

filename = "file_example.txt"
WScript.Echo ModifyFilename(filename) ' Output: file1_example.txt

filename = "file2_example.txt"
WScript.Echo ModifyFilename(filename) ' Output: file2_example.txt
