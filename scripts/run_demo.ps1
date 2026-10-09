Write-Host "AI Dependency Upgrade Agent"
Write-Host ""

Write-Host "Scanning dependencies..."
python -m app.cli scan sample_project

Write-Host ""
Write-Host "Running tests..."
python -m app.cli test sample_project

Write-Host ""
Write-Host "Running complete analysis..."
python -m app.cli analyze sample_project

Write-Host ""
Write-Host "Demo completed."