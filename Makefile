lc=python3
file=

all: event

f: fighter
fighter:
	$(lc) spoiler_free.py

e: card
event: card
card:
	$(lc) spoiler_free.py event

clean:
	rm -f *~
