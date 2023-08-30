param(
    [string]$sourceFilePath,
    [string]$destinationFilePath,
    [string]$searchString = "string1",
    [string]$replaceString = "string2"
)

# Read the content of the source file
$fileContent = Get-Content -Path $sourceFilePath -Raw

# Replace instances of the search string with the replace string
$modifiedContent = $fileContent -replace [regex]::Escape($searchString), $replaceString

# Write the modified content to the destination file
$modifiedContent | Set-Content -Path $destinationFilePath

Write-Host "Replacement complete. Modified file saved at: $destinationFilePath"
