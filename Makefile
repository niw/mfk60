.DEFAULT_GOAL := panelize

DIODE := D{} CUSTOM 6.25 0 270 BACK

.PHONY: apply_layout
apply_layout: mfk60_keyboard-layout.json
	sh bin/kbplacer.sh \
	--board mfk60.kicad_pcb \
	--layout "$<" \
	--diode "${DIODE}"

.PHONY: panelize
panelize: mfk60_panelized.kicad_pcb mfk60_top_plate_panelized.kicad_pcb mfk60_middle_plate_panelized.kicad_pcb mfk60_bottom_plate_panelized.kicad_pcb

.PHONY: clean
clean:
	$(RM) mfk60*_panelized.kicad_*

mfk60_panelized.kicad_pcb: mfk60.kicad_pcb mfk60_kikit.json
	bin/kikit.sh panelize -p mfk60_kikit.json mfk60.kicad_pcb "$@"
	bin/python.sh bin/update_text_position.py -b "$@"

mfk60_top_plate_panelized.kicad_pcb: mfk60_top_plate.kicad_pcb mfk60_kikit.json
	bin/kikit.sh panelize -p mfk60_kikit.json mfk60_top_plate.kicad_pcb "$@"
	bin/python.sh bin/update_text_position.py -b "$@"

mfk60_middle_plate_panelized.kicad_pcb: mfk60_middle_plate.kicad_pcb mfk60_kikit.json
	bin/kikit.sh panelize -p mfk60_kikit.json mfk60_middle_plate.kicad_pcb "$@"
	bin/python.sh bin/update_text_position.py -b "$@"

mfk60_bottom_plate_panelized.kicad_pcb: mfk60_bottom_plate.kicad_pcb mfk60_kikit.json
	bin/kikit.sh panelize -p mfk60_kikit.json mfk60_bottom_plate.kicad_pcb "$@"
	bin/python.sh bin/update_text_position.py -b "$@"
