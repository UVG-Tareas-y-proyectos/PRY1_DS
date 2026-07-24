param([string[]]$InputFiles,[string]$OutputDirectory)
$ErrorActionPreference = 'Stop'
[System.IO.Directory]::CreateDirectory($OutputDirectory) | Out-Null
$wordApplication = $null
try {
    $wordApplication = New-Object -ComObject Word.Application
    $wordApplication.Visible = $false
    $wordApplication.DisplayAlerts = 0
    $wordApplication.AutomationSecurity = 3
    foreach ($inputFile in $InputFiles) {
        $document = $null
        try {
            $resolvedInput = [System.IO.Path]::GetFullPath($inputFile)
            $outputPdf = Join-Path $OutputDirectory ([System.IO.Path]::GetFileNameWithoutExtension($resolvedInput) + '.pdf')
            Write-Output ('Abriendo ' + [System.IO.Path]::GetFileName($resolvedInput))
            $document = $wordApplication.Documents.Open($resolvedInput, $false, $true, $false)
            Write-Output ('Exportando ' + [System.IO.Path]::GetFileName($outputPdf))
            $document.Repaginate()
            $document.ExportAsFixedFormat($outputPdf, 17)
            Write-Output $outputPdf
        }
        finally {
            if ($null -ne $document) {
                $document.Close(0)
                [System.Runtime.InteropServices.Marshal]::FinalReleaseComObject($document) | Out-Null
            }
        }
    }
}
finally {
    if ($null -ne $wordApplication) {
        $wordApplication.Quit(0)
        [System.Runtime.InteropServices.Marshal]::FinalReleaseComObject($wordApplication) | Out-Null
    }
}
