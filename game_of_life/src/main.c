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
#include <stdlib.h>
#include <string.h>
#include "data.h"
#include "io.h"
#include "cli.h"

int main (int argc, char *argv[], char **envp) {
	// init config
	config_t config;

	config.board_width = 20;
	config.board_height = 20;
	config.cli = true;
	config.gui = false;
	config.timing = 500;
	config.edge = 1;
	config.rules = 0;
	config.file = "";



	// parsing command line arguments
	for (int i = 1; i < argc; i++) {
//        printf("argv[%i]: %s\n", i, argv[i]);
		if (argv[i][0] == '-') {
			char s = argv[i][1];

			int j = 0;
			int dimlength = 0;
			int dimsep = 0;
			char * c1 = "";
			char * c2 = "";
			switch (s) {
				// use cli as ui
				case 'c':
					config.cli = true;
					break;
				// use gui as ui
				case 'g':
					config.gui = true;
					break;
				// timing in milliseconds
				case 't':
					config.timing = atoi(&argv[i][2]);
					break;
				// path to config file
				case 'f':
					config.file = &argv[i][2];
					break;
				// dimension of the board
				case 'd':
					// read dimension from arguments. To do this we have to do some string mojo
					dimlength = strlen(&argv[i][2]);
					for (j = 0; j < dimlength; j++) {
						if (*(&argv[i][2] + j) == 'x') {
							dimsep = j;
							break;
						}
					}
					c1 = strndup(&argv[i][2], dimsep);
					c2 = strndup((&argv[i][2] + (dimsep + 1)), dimlength);

					if ((atoi(c1) > 2) && (atoi(c2) > 2)) {
						config.board_width = atoi(c1);
						config.board_height = atoi(c2);
					}

					break;
				// edge behaviour
				case 'e':
					config.edge = atoi(&argv[i][2]);
					break;
				// set of rules
				case 'r':
					config.rules = atoi(&argv[i][2]);
					break;
				// display help and exit
				// TODO: add help text
				case 'h':
                    printf("Usage: game_of_life [Options]\n");
                    printf("Options:\n");
                    printf(" -h\tShow this help\n");
                    printf(" -c\tUse cli as ui (Default)\n");
                    printf(" -g\tUse gui (not yet implemented)\n");
                    printf(" -t\tRound timing in milliseconds\n");
                    printf(" -f\tPath to config file for initial pattern: -f\"./game_templates/glider_1.gol\"\n");
                    printf(" -d\tField Dimensions: \"X\"x\"Y\" e.g. 20x30 (not yet implemented)\n");
                    printf(" -e\tEdge behaviour (Not yet implemented)\n");
                    printf(" -r\tSet of Rules to use (Not yet implemented)\n");
					exit(0);
					break;
				default:
                    printf("Please enter valid arguments. Use -h for help!\n");
                    exit(-1);
					break;
			}
		}
        else {
            printf("Please enter valid arguments. Use -h for help!\n");
            exit(-1);
        }

	}
/*
	printf("\n");
	printf("Configs:\n");
	printf("config.board_width: %i\n",config.board_width);
	printf("config.board_height: %i\n",config.board_height);
	printf("config.cli: %i\n",config.cli);
	printf("config.gui: %i\n",config.gui);
	printf("config.timing: %i\n",config.timing);
	printf("config.edge: %i\n",config.edge);;
	printf("config.rules: %i\n",config.rules);
	printf("config.file: %s\n",config.file);
*/
	// init data
	rounddata_t data;

	data.round_count = 0;
	for (int i = 0; i < 20; i++) {
		for (int j = 0; j < 20; j++) {
			data.data[i][j] = 0;
		}
	}

	// load game data from file
	data = loadDataFromFile(config.file);

	// run CLI/GUI
	run_cli(data, config);

	printf("Done!\n");
	return 0;
}
















