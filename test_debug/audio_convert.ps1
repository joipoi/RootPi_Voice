Get-ChildItem "audio_files" -Filter *.wav | ForEach-Object {
    $tmp = "$($_.DirectoryName)\tmp.wav"
    ffmpeg -y -i $_.FullName -ar 16000 -ac 1 -f wav $tmp
    Move-Item -Force $tmp $_.FullName
}

