#include <stdio.h>
#include <stdlib.h>

//char readFile(char *name);

main(int argc, char *argv[]) {
	int size;
	char *program;
	char *mem;
	char *inp;
	char c, m;
	int n, ptr, lvl, off, len, t;
	FILE *in;

	FILE *fp = fopen(argv[1], "r");
	if (argc > 2) {
		in = fopen(argv[2], "r");
		fseek(in, 0, SEEK_END);
		size = ftell(in);
		rewind(in);
		inp = (char *) malloc (sizeof(char) * (size + 2));
		fread(inp, sizeof(char), size, in);
		*(inp+size+1) = 10;
		fclose(in);
	}
	if (fp == 0) {
		printf("Could not open file %s", argv[1]);
	} else {
		fseek(fp, 0, SEEK_END);
		size = ftell(fp);
		rewind(fp);
		program = (char *) malloc (sizeof(char) * (size+1));
		fread(program, sizeof(char), size, fp);
		fclose(fp);
		mem = (char *) calloc (100, sizeof(char));
		len = 100;
		off = 0;
		ptr = 0;
		while (ptr < size) {
			c = *(program+ptr);
			switch(c) {
				case '+':
					(*mem)++;
					break;
				case '-':
					(*mem)--;
					break;
				case '>':
					mem++;
					off++;
					if (off >= len) {
						len = len + 10;
						mem = (char *) realloc (mem-off, (len+1) * sizeof(char));
						mem = mem + off;
						for (t = 0; t < (len-off); t++) {
							*(mem+t) = 0;
						}
					}
					break;
				case '<':
					mem--;
					off--;
					break;
				case '.':
					printf("%c", *mem);
					break;
				case ',':
					*mem = *inp;
					inp++;
					break;
				case ']':
					if (!*mem) {
						break;
					}
					lvl = 1;
					while (lvl) {
						ptr--;
						if (*(program+ptr) == ']') {
							lvl++;
						} else if (*(program+ptr) == '[') {
							lvl--;
						}
					}
					ptr--;
					break;
				case '[':
					if (*mem) {
						break;
					}
					lvl = 1;
					while (lvl) {
						ptr++;
						if (*(program+ptr) == '[') {
							lvl++;
						} else if (*(program+ptr) == ']') {
							lvl--;
						}
					}
					break;
				default:
					break;
			}
			//printf("%d\t%d\t%d\n", *mem, mem, *(program+ptr));
			ptr++;
		}
	}
}
