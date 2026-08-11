
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
        cout << "Please compile the required driver first." << endl;
        return 1;
    }

    if (!exists(inputFile)) {
        cout << "Input file not found: " << inputFile << endl;
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
        cout << "4. Betweenness Centrality\n";
        cout << "5. Connected Components\n";
        cout << "6. Triangle Counting\n";
        cout << "7. Exit\n";
        cout << "====================================\n";
        cout << "Choice: ";

        int choice;

        if (!(cin >> choice)) {
            cout << "Invalid input. Please enter a number.\n";
            cin.clear();
            cin.ignore(10000, '\n');
            continue;
        }

        if (choice == 7) {
            cout << "Exiting wrapper.\n";
            break;
        }

        if (choice < 1 || choice > 7) {
            cout << "Invalid choice. Please select 1-7.\n";
            continue;
        }

        string inputFile;
        cout << "Enter input file: ";
        cin >> inputFile;

        int status = 0;

        switch (choice) {
            case 1:
                status = executeDriver("./bfs_driver", inputFile);
                break;

            case 2:
                status = executeDriver("./dfs_driver", inputFile);
                break;

            case 3:
                status = executeDriver("./sssp_driver", inputFile);
                break;

            case 4:
                status = executeDriver("./bc_driver",
                                       inputFile);
                break;

            case 5:
                status = executeDriver("./connected_components_driver",
                                       inputFile);
                break;

            case 6:
                status = executeDriver("./triangle_counting_driver",
                                       inputFile);
                break;
        }

        if (status != 0) {
            cout << "Execution failed.\n";
        }
    }

    return 0;
}


