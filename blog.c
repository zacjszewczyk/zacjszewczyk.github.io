#include <stdio.h>
#include <string.h>

#define HEADER "\033[95m" // Pink
#define OKBLUE "\033[94m" // Purple
#define OKGREEN "\033[92m" // Green
#define WARNING "\033[93m" // Yellow
#define FAIL "\033[91m" // Red
#define ENDC "\033[0m" // None
#define BOLD "\033[1m" // Blue
#define UNDERLINE "\033[4m" // Underline

int main (int argc, char* argv[]) {
    if (argc == 1) { 
        printf(UNDERLINE"Note"ENDC": You can use '-a' to enter 'Authoring Mode'\n");
    }
    else if (argc == 2) {
        if ((strstr("\"", argv[1]) != NULL) || (strstr("'", argv[1]) != NULL)) {
            printf("Invalid parameter.");
        }
    }
}