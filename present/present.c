#include <stdio.h>
#include "present.h"




int main (void) {
	int input = -1;
	int active = 0;

	// Text dynamisch....
	char* text[SLIDE_COUNT];

	INIT_SLIDES();

	while (1) {
		printf("%s", text[active]);

		input = -1;
		while (input == -1) {
			input = getc(stdin);
		}

		// bounds abfragen...
		// Tasten richtig einrichten...
		switch (input) {
			case 97:
				if ((active + 1) < (SLIDE_COUNT)) {
					active = active + 1;
				}
				break;
			case 98:
				if ((active - 1) >= 0) {
					active = active - 1;
				}
				break;
			default:
				break;
		}
	}
	return;
}
