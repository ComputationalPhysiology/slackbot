
filename=journal_club

default:
	pdflatex ${filename}
	bibtex mechanics
	bibtex patient_specific
	pdflatex ${filename}
	pdflatex ${filename}

read:
	open ${filename}.pdf &

clean:
	clean-files-latex
