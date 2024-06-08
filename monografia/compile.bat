@echo off
pdflatex monografia
bibtex monografia
pdflatex monografia
pdflatex monografia

:: Deletar arquivos auxiliares nas pastas e subpastas
for /r %%x in (*.aux *.bbl *.blg *.brf *.dvi *.idx *.lof *.log *.lot *.nlo *.toc) do del /f /q "%%x"

echo Compilation and cleanup completed.
echo Pressione Enter para abrir o PDF no Chrome.
pause >nul

:: Abrir o PDF no Google Chrome
start chrome %cd%\monografia.pdf
cls