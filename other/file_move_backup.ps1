param (
    [Parameter(Mandatory=$true)]
    [ValidateScript({Test-Path $_ -PathType 'Container'})]
    [string]$SourceDirectory,

    [Parameter(Mandatory=$true)]
    [ValidateScript({Test-Path $_ -PathType 'Container'})]
    [string]$BackupDirectory,

    [Parameter(Mandatory=$true)]
    [ValidateScript({Test-Path $_ -PathType 'Container'})]
    [string]$DestinationDirectory
)

# Function to create a backup of a file in the backup directory
function Backup-File {
    param (
        [Parameter(Mandatory=$true)]
        [string]$FilePath,

        [Parameter(Mandatory=$true)]
        [string]$BackupDirectory
    )

    $fileName = Split-Path $FilePath -Leaf
    $backupPath = Join-Path -Path $BackupDirectory -ChildPath $fileName

    # Copy the file to the backup directory
    try {
        Copy-Item -Path $FilePath -Destination $backupPath -ErrorAction Stop
    } catch {
        Write-Error "Failed to create a backup of file '$FilePath'."
        return $false
    }

    return $true
}

# Main script logic
try {
    # Get all non-directory files in the source directory
    $files = Get-ChildItem -Path $SourceDirectory -File

    # Process each file
    foreach ($file in $files) {
        # Backup the file
        if (-not (Backup-File -FilePath $file.FullName -BackupDirectory $BackupDirectory)) {
            continue
        }

        # Move the file to the destination directory
        try {
            Move-Item -Path $file.FullName -Destination $DestinationDirectory -ErrorAction Stop
        } catch {
            Write-Error "Failed to move file '$($file.FullName)' to the destination directory."
        }
    }
} catch {
    Write-Error "An error occurred while processing the files."
}
