#####
#game_of_life
#
#Copyright 2012, erebos42 (https://github.com/erebos42/miscScripts)
#
#This is free software; you can redistribute it and/or modify it
#under the terms of the GNU Lesser General Public License as
#published by the Free Software Foundation; either version 2.1 of
#the License, or (at your option) any later version.
#
#This software is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
#Lesser General Public License for more details.
#
#You should have received a copy of the GNU Lesser General Public
#License along with this software; if not, write to the Free
#Software Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA
#02110-1301 USA, or see the FSF site: http://www.fsf.org.
#####

TARGET	= game_of_life

CC		= gcc
RM		= rm -f

CFLAGS	= -Wall -std=gnu99 -O2
LDFLAGS = 

SRC		= ./src/main.c ./src/io.c ./src/data.c ./src/cli.c ./src/backend.c 
OBJ		= $(SRC:.c=.o)

all: $(TARGET) cleanup

$(TARGET): $(OBJ)
	@echo "# Linking $(TARGET)"
	$(CC) $(CFLAGS) $(OBJ) -o $(TARGET)

%.o: %.c
	@echo "# Compiling $< to $@"
	$(CC) $(CFLAGS) $< -c -o $@

cleanup:
	@echo "# Cleaning up object files"
	$(RM) $(OBJ)	

clean:
	$(RM) $(TARGET)
	$(RM) $(OBJ)















