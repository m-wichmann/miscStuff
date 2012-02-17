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

#include "backend.h"
#include "data.h"

rounddata_t calc_next_round(rounddata_t data, config_t config) {
	
	// init next round data
	rounddata_t new_data = data;
	

	// increment round count
	new_data.round_count++;

	for (int i = 0; i < 20; i++) {
		for (int j = 0; j < 20; j++) {
//			char cell_focus = data.data[i][j];
			char cell_1 = data.data[(i-1)%20][(j-1)%20];
			char cell_2 = data.data[(i-1)%20][(j)%20];
			char cell_3 = data.data[(i-1)%20][(j+1)%20];
			char cell_4 = data.data[(i)%20][(j-1)%20];
			char cell_5 = data.data[(i)%20][(j+1)%20];
			char cell_6 = data.data[(i+1)%20][(j-1)%20];
			char cell_7 = data.data[(i+1)%20][(j)%20];
			char cell_8 = data.data[(i+1)%20][(j+1)%20];
			char cell_sum = cell_1 + cell_2 + cell_3 + cell_4 + cell_5 + cell_6 + cell_7 + cell_8;
			switch (cell_sum) {
				case 0:
					new_data.data[i][j] = 0;
					break;
				case 1:
					new_data.data[i][j] = 0;
					break;
				case 2:
					new_data.data[i][j] = data.data[i][j];
					break;
				case 3:
					new_data.data[i][j] = 1;
					break;
				default:
					new_data.data[i][j] = 0;
					break;
			}
		}
	}

	return new_data;
}
