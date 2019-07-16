# +---------------+
# | Nari Makefile |
# +---------------+

# Version info
# CHANGE EVERY TIME YOU MAKE ANY CHANGES TO NARI!
VERSION = 4
FIX = 1

# Other stuff
SOURCE = nari.py
CSOURCE = toCompile.c
OUT = nari
MANPAGE = ../man/ldpl.1
COMPILEDATE="$(shell date +%Y-%m-%d)"
COMPILEHOUR="$(shell date +%H:%M:%S)"

all: $(CSOURCE)
	$(CC) $(CSOURCE) `/usr/bin/python3-config --cflags --ldflags` -v -fPIC -o $(OUT)

$(CSOURCE): $(SOURCE)
	if test -f "$FILE"; then rm toCompile.py; fi
	cp $(SOURCE) toCompile.py
	sed -i "s/@MAYORVERSION/$(VERSION)/g" toCompile.py
	sed -i "s/@COMMITVERSION/$(FIX)/g" toCompile.py
	sed -i "s/@COMPILEDATE/$(COMPILEDATE)/g" toCompile.py
	sed -i "s/@COMPILEHOUR/$(COMPILEHOUR)/g" toCompile.py
	cython -3 --embed toCompile.py

clean:
	rm -f nari.c nari

install: $(OUT) #$(MANPAGE)
	install -d $(DESTDIR)$(PREFIX)/bin/
	install -m 775 nari $(DESTDIR)$(PREFIX)/bin/
	#install -d $(DESTDIR)$(PREFIX)/share/man/man1/
	#install $(MANPAGE) $(DESTDIR)$(PREFIX)/share/man/man1/
ifneq ($(shell uname -s),Darwin)
	mandb
endif

uninstall:
	rm $(DESTDIR)$(PREFIX)/bin/nari
	#rm $(DESTDIR)$(PREFIX)/share/man/man1/nari.1
ifneq ($(shell uname -s),Darwin)
	mandb
endif
