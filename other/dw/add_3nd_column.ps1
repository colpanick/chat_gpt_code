# Get all .txt files in the current directory
$files = Get-ChildItem -Filter *.txt

# Iterate through each file and modify it
foreach ($file in $files) {
    # Read the content of the file
    $content = Get-Content $file.FullName

    # Iterate through each line and add a blank column after the second column
    $modifiedContent = $content | ForEach-Object {
        $columns = $_ -split '\|'
        $columns = $columns[0..1] + '' + $columns[2..($columns.Length - 1)]
        $columns -join '|'
    }

    # Save the modified content back to the file
    $modifiedContent | Set-Content $file.FullName
}

Write-Host "Modification complete."
