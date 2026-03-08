# PowerShell script to deploy with proper encoding
$env:PYTHONIOENCODING = "utf-8"
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
[Console]::InputEncoding = [System.Text.Encoding]::UTF8

cd "D:\Northflank + openv\code_refactor_gym"
openenv push
