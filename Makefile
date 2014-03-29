.PHONY: test

test:
	./timestat test

all: README.markdown.html

README.markdown.html: README2.markdown
	markdown < README2.markdown > README.markdown.html

README2.markdown: README.markdown
	echo '<link href="https://raw.github.com/jasonm23/markdown-css-themes/gh-pages/markdown6.css" rel="stylesheet"></link>' > README2.markdown
	cat README.markdown >> README2.markdown

clean:
	rm README2.markdown README.markdown.html
