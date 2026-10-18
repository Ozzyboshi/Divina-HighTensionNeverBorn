# Divina - High Tension Never Born
#
#   make      -> divina (AmigaDOS executable) + divina.adf
#   make run     -> FS-UAE, A500, KS 1.3, 512K chip + 512K slow
#   make run600  -> FS-UAE, A600, KS 2.05, 1MB chip (stock)
#   make clean

VASM      ?= vasmm68k_mot
EXE2ADF   ?= exe2adf
FSUAE     ?= fs-uae
KSDIR     ?= $(HOME)/Documenti/FS-UAE/Kickstarts
KICKSTART ?= $(KSDIR)/Kickstart v1.3 rev 34.5 (1987)(Commodore)(A500-A1000-A2000-CDTV)[!].rom
KICK600   ?= $(KSDIR)/Kickstart v2.05 rev 37.299 (1991)(Commodore)(A600)[!].rom

# -no-opt keeps every instruction exactly as in the original (same timing)
VASMFLAGS = -m68000 -Fhunkexe -kick1hunks -nosym -no-opt -quiet

all: divina divina.adf

divina: divina.asm
	$(VASM) $(VASMFLAGS) -o $@ $<

divina.adf: divina
	$(EXE2ADF) -i $< -a $@ -l DIVINA

run: divina.adf
	$(FSUAE) --amiga_model=A500 \
		--kickstart_file="$(KICKSTART)" \
		--chip_memory=512 --slow_memory=512 --fast_memory=0 \
		--floppy_drive_0="$(abspath divina.adf)" \
		--floppy_drive_speed=0

run600: divina.adf
	$(FSUAE) --amiga_model=A600 \
		--kickstart_file="$(KICK600)" \
		--chip_memory=1024 --slow_memory=0 --fast_memory=0 \
		--floppy_drive_0="$(abspath divina.adf)" \
		--floppy_drive_speed=0

clean:
	rm -f divina divina.adf

.PHONY: all run run600 clean
