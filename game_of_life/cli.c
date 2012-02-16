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

#include <stdio.h>
#include <unistd.h>
#include "cli.h"
#include "data.h"
#include "backend.h"



int run_cli(rounddata_t data, config_t config) {

	char done = 1;
	while (done) {
		printf("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n");
		printf("round No.: %i\n", data.round_count);
		print_data(data, config);
		data = calc_next_round(data, config);
		usleep(250000);
	}

	// TODO: check if cli should be exited

	return 0;
}




int print_data(rounddata_t data, config_t config) {

	for (int i = 0; i < 20; i++) {
		for (int j = 0; j < 20; j++) {
			printf("%i", data.data[i][j]);
		}
		printf("\n");
	}
	
	return 0;
}
