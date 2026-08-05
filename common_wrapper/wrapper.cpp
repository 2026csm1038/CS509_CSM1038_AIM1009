#include <cstdlib>
#include <fstream>
#include <iostream>
#include <string>

using namespace std;

bool exists(const string &path) {
    ifstream file(path);
    return file.good();
}

int executeDriver(const string &driver, const string &inputFile) {
    if (!exists(driver)) {
        cout << "Driver not found: " << driver << endl;
        return 1;
    }

    if (!exists(inputFile)) {
        cout << "Input file not found." << endl;
        return 1;
    }

    string command = driver + " " + inputFile;
    return system(command.c_str());
}

int main() {
    while (true) {
        cout << "\n========== Common Wrapper ==========\n";
        cout << "1. BFS\n";
        cout << "2. DFS\n";
        cout << "3. SSSP\n";
        cout << "4. Exit\n";
        cout << "Choice: ";

        int choice;
        cin >> choice;

        if (choice == 4)
            break;

        if (choice < 1 || choice > 4) {
            cout << "Invalid choice.\n";
            continue;
        }

        string inputFile;
        cout << "Enter input file: ";
        cin >> inputFile;

        int status = 0;

        if (choice == 1)
            status = executeDriver("./bfs_driver", inputFile);
        else if (choice == 2)
            status = executeDriver("./dfs_driver", inputFile);
        else
            status = executeDriver("./sssp_driver", inputFile);

        if (status != 0)
            cout << "Execution failed.\n";
    }

    return 0;
}
