# Set the directory and timeframe variables
$directory = "C:\Users\Username\Documents"
$timeframe = "7"  # Deletes files that are 7 or more days old
$filter = "*.txt"  # Deletes only files with a .txt extension

# Calculate the date threshold based on the timeframe
$dateThreshold = (Get-Date).AddDays(-$timeframe)

# Get a list of files in the directory that match the filter and are older than the threshold date
$filesToDelete = Get-ChildItem -Path $directory -Filter $filter | Where-Object { $_.LastWriteTime -lt $dateThreshold }

# Delete the files
foreach ($file in $filesToDelete) {
    Remove-Item $file.FullName
}
