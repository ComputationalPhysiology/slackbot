
filename=journal_club

default:
	pdflatex ${filename}
	bibtex ${filename}
	pdflatex ${filename}
	pdflatex ${filename}

read:
	open ${filename}.pdf &

clean:
	clean-files-latex
