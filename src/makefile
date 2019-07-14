# +---------------+
# | Nari Makefile |
# +---------------+

SOURCE = nari.py
CSOURCE = nari.c
OUT = nari
MANPAGE = ../man/ldpl.1

all: $(CSOURCE)
	$(CC) $(CSOURCE) `/usr/bin/python3-config --cflags --ldflags` -v -fPIC -o $(OUT)

$(CSOURCE): $(SOURCE)
	cython -3 --embed $(SOURCE)

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
