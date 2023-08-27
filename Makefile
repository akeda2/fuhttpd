# fuhttpd Makefile
# 

all: fuhttpd del
# readme

# Create fuhttpd executable
fuhttpd:
	pyinstaller --clean fuhttpd.py -F
	mv dist/fuhttpd .

# Remove files created by pyinstaller
del:
	rm -rf ./dist/ ./build/ ./*.spec ./*.pyc ./*.log fuhttpd.spec dist/

# Clear pyinstall cache and delete file
clean:
	#pyinstaller --clean fuhttpd.py
	rm -rf ./dist/ ./build/ ./*.spec ./*.pyc ./*.log randrn.spec dist/ fuhttpd

PREFIX ?= /usr/local
BINDIR ?= $(PREFIX)/bin

install:
	mkdir -p $(DESTDIR)$(BINDIR)
	install -m755 fuhttpd $(DESTDIR)$(BINDIR)/fuhttpd
