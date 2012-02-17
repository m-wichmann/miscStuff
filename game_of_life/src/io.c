/*
game_of_life

Copyright 2012, erebos42 (https://github.com/erebos42/miscScripts)

This is free software; you can redistribute it and/or modify it
under the terms of the GNU Lesser General Public License as
published by the Free Software Foundation; either version 2.1 of
the License, or (at your option) any later version.

This software is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public
License along with this software; if not, write to the Free
Software Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA
02110-1301 USA, or see the FSF site: http://www.fsf.org.
*/

#include "io.h"
#include <stdio.h>
#include <stdlib.h>

rounddata_t loadDataFromFile(char * filepath) {

	rounddata_t ret;
	ret.round_count = 0;
	for (int i = 0; i < 20; i++) {
		for (int j = 0; j < 20; j++) {
			ret.data[i][j] = 0;
		}
	}

	FILE *fp;

	if((fp = fopen(filepath, "r")) == NULL) {
		printf("Cannot open file.\n");
		exit(1);
	}


	int temp = 42;
	int i = 0;
	int j = 0;
	while ((temp = fgetc(fp)) != EOF) {
		temp = temp - 48;
		if ((temp == 0) || (temp == 1)) {
			ret.data[i][j] = temp;
			j++;
		}
		if (temp == -38) { // end of line
			j = 0;
			i++;
		}
	}

	fclose(fp);

	return ret;
}















