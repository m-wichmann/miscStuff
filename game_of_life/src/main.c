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
#include "data.h"
#include "io.h"
#include "cli.h"

int main (void) {
	printf("Start!\n");

	// TODO: parse command line arguments
	// CLI or GUI
	// What init data
	// What timing
	// set of rules
	// dimension of the board
	// edge behaviour

	// init data
	rounddata_t data;

	data.round_count = 0;
	for (int i = 0; i < 20; i++) {
		for (int j = 0; j < 20; j++) {
			data.data[i][j] = 0;
		}
	}

	// load game data from file
	data = loadDataFromFile("/home/erebos/Programming/miscScripts/game_of_life/game_templates/glider_1.gol");

	config_t config;
	config.board_width = 20;
	config.board_height = 20;




	// TODO: run CLI/GUI
	run_cli(data, config);

	printf("Done!\n");
	return 0;
}
















