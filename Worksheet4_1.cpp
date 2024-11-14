#include <iostream>
#include <vector>
#include <string>
#include <map>
#include <set>
#include <tuple>
#include <cstdlib>
#include <ctime>
#include <algorithm>
#include <cmath>
#include <chrono>
#include <thread>
#include <random>    // For random number generation
#include <iomanip>   // For setting precision

using namespace std;

// Function prototypes
double calculate_empowerment(pair<int, int> start_position, int grid_size, const set<pair<int, int>>& occupied_positions);
pair<int, int> simulate_sequence(pair<int, int> start_position, const vector<string>& sequence, int grid_size, const set<pair<int, int>>& occupied_positions);
pair<int, int> apply_action(pair<int, int> position, const string& action);
pair<pair<int, int>, string> vip_empowerment_policy(pair<int, int> position, int grid_size, const set<pair<int, int>>& occupied_positions);

// Actions mapping
map<string, pair<int, int>> actions = {
    {"north", {-1, 0}},
    {"south", {1, 0}},
    {"west",  {0, -1}},
    {"east",  {0, 1}}
};

// Generate all 3-step action sequences
vector<vector<string>> action_sequences;

// Function to generate all action sequences
void generate_action_sequences() {
    vector<string> action_keys;
    for (const auto& action : actions) {
        action_keys.push_back(action.first);
    }

    for (const auto& a1 : action_keys) {
        for (const auto& a2 : action_keys) {
            for (const auto& a3 : action_keys) {
                action_sequences.push_back({a1, a2, a3});
            }
        }
    }
}

// Agent class definition
class Agent {
public:
    string name;
    pair<int, int> position;
    string behaviour;  // "annoying" or "vip"

    Agent(string name, pair<int, int> position, string behaviour)
        : name(name), position(position), behaviour(behaviour) {}

    string move(int grid_size, const set<pair<int, int>>& occupied_positions) {
        if (behaviour == "annoying") {
            return "";  // Annoying agents do not move
        } else {
            // VIP agent movement
            auto result = vip_empowerment_policy(position, grid_size, occupied_positions);
            pair<int, int> new_position = result.first;
            string action_taken = result.second;

            string move_result = name + " moves " + action_taken + " to " +
                                 to_string(new_position.first + 1) + "x" + to_string(new_position.second + 1);

            // Check if the move is out of bounds
            if (new_position.first < 0 || new_position.first >= grid_size ||
                new_position.second < 0 || new_position.second >= grid_size) {
                move_result = name + " tried to move " + action_taken + " to " +
                              to_string(new_position.first + 1) + "x" + to_string(new_position.second + 1) +
                              " but got hit by a wall";
                new_position = position;  // Stay in the same position
            }
            // Check if the new position is occupied by an annoying agent
            else if (occupied_positions.count(new_position)) {
                move_result = name + " tried to move " + action_taken + " to " +
                              to_string(new_position.first + 1) + "x" + to_string(new_position.second + 1) +
                              " but was blocked by an annoying agent";
                new_position = position;  // Stay in the same position
            }
            // Update position
            position = new_position;
            return move_result;
        }
    }
};

// GridWorld class definition
class GridWorld {
public:
    int size;
    vector<Agent> agents;

    GridWorld(int size, vector<Agent> agents) : size(size), agents(agents) {}

    set<pair<int, int>> get_occupied_positions() {
        set<pair<int, int>> occupied_positions;
        for (const auto& agent : agents) {
            if (agent.behaviour == "annoying") {
                occupied_positions.insert(agent.position);
            }
        }
        return occupied_positions;
    }

    void update_world() {
        auto occupied_positions = get_occupied_positions();
        for (auto& agent : agents) {
            if (agent.behaviour != "annoying") {
                string move_result = agent.move(size, occupied_positions);
                if (!move_result.empty()) {
                    cout << move_result << endl;
                }
                double empowerment = calculate_empowerment(agent.position, size, occupied_positions);
                cout << fixed << setprecision(2);
                cout << "3-step empowerment for " << agent.name << " at "
                     << agent.position.first + 1 << "x" << agent.position.second + 1 << ": "
                     << empowerment << endl;
            }
        }
    }

    void display_grid() {
        vector<vector<string>> grid(size, vector<string>(size, " "));
        for (const auto& agent : agents) {
            int x = agent.position.first;
            int y = agent.position.second;
            grid[x][y] = agent.name;
        }
        cout << "\nGrid State:" << endl;
        for (const auto& row : grid) {
            cout << "[";
            for (size_t i = 0; i < row.size(); ++i) {
                cout << row[i];
                if (i < row.size() - 1) {
                    cout << "|";
                }
            }
            cout << "]" << endl;
        }
    }
};

// Function to apply an action
pair<int, int> apply_action(pair<int, int> position, const string& action) {
    int dx = actions[action].first;
    int dy = actions[action].second;
    int new_x = position.first + dx;
    int new_y = position.second + dy;
    // Return the intended new position (even if it's invalid)
    return make_pair(new_x, new_y);
}

// Function to simulate a 3-step sequence
pair<int, int> simulate_sequence(pair<int, int> start_position, const vector<string>& sequence, int grid_size, const set<pair<int, int>>& occupied_positions) {
    pair<int, int> position = start_position;
    for (const auto& action : sequence) {
        pair<int, int> proposed_position = apply_action(position, action);
        // Check for walls
        if (proposed_position.first < 0 || proposed_position.first >= grid_size ||
            proposed_position.second < 0 || proposed_position.second >= grid_size) {
            continue;  // Agent stays in the same position
        }
        // Check for annoying agents
        else if (occupied_positions.count(proposed_position)) {
            continue;  // Agent stays in the same position
        } else {
            // Move is successful
            position = proposed_position;
        }
    }
    return position;
}

// Function to calculate empowerment
double calculate_empowerment(pair<int, int> start_position, int grid_size, const set<pair<int, int>>& occupied_positions) {
    set<pair<int, int>> reachable_states;
    for (const auto& sequence : action_sequences) {
        pair<int, int> final_position = simulate_sequence(start_position, sequence, grid_size, occupied_positions);
        reachable_states.insert(final_position);
    }
    if (!reachable_states.empty()) {
        return log2(reachable_states.size());
    } else {
        return 0;
    }
}

// VIP agent's empowerment-driven movement policy
pair<pair<int, int>, string> vip_empowerment_policy(pair<int, int> position, int grid_size, const set<pair<int, int>>& occupied_positions) {
    double max_empowerment = -1;
    vector<pair<pair<int, int>, string>> best_moves;
    // Evaluate all possible moves
    for (const auto& action_pair : actions) {
        string action = action_pair.first;
        pair<int, int> proposed_position = apply_action(position, action);
        pair<int, int> new_position;
        // Check for walls and annoying agents
        if (proposed_position.first < 0 || proposed_position.first >= grid_size ||
            proposed_position.second < 0 || proposed_position.second >= grid_size ||
            occupied_positions.count(proposed_position)) {
            new_position = position;  // Stay in the same position
        } else {
            new_position = proposed_position;  // Move is successful
        }
        // Calculate empowerment from the new position
        double empowerment = calculate_empowerment(new_position, grid_size, occupied_positions);
        if (empowerment > max_empowerment) {
            max_empowerment = empowerment;
            best_moves = { {proposed_position, action} };
        } else if (empowerment == max_empowerment) {
            best_moves.push_back({ proposed_position, action });
        }
    }
    // Randomly select one of the best moves
    static std::default_random_engine rng(static_cast<unsigned int>(time(0)));
    std::uniform_int_distribution<int> dist(0, best_moves.size() - 1);
    auto chosen_move = best_moves[dist(rng)];
    return chosen_move;  // Returns (new_position, action_taken)
}

int main() {
    srand(static_cast<unsigned int>(time(0)));

    // Generate all action sequences
    generate_action_sequences();

    int grid_size = 5;
    set<pair<int, int>> agent_positions;

    // Initialize 5 annoying agents with random positions
    vector<Agent> annoying_agents;
    int annoying_agents_count = 5;
    for (int i = 0; i < annoying_agents_count; ++i) {
        while (true) {
            int x = rand() % grid_size;
            int y = rand() % grid_size;
            pair<int, int> position = make_pair(x, y);
            if (agent_positions.count(position) == 0) {
                agent_positions.insert(position);
                annoying_agents.emplace_back("A", position, "annoying");
                break;
            }
        }
    }

    // Initialize the VIP agent with a random position
    Agent vip_agent("V", {0, 0}, "vip");
    while (true) {
        int x = rand() % grid_size;
        int y = rand() % grid_size;
        pair<int, int> position = make_pair(x, y);
        if (agent_positions.count(position) == 0) {
            agent_positions.insert(position);
            vip_agent.position = position;
            break;
        }
    }

    // Add all agents to the grid world
    vector<Agent> agents = annoying_agents;
    agents.push_back(vip_agent);
    GridWorld world(grid_size, agents);

    // Run the world updates for 50 steps and display the grid state
    for (int step = 0; step < 50000; ++step) {
        cout << "\nStep " << step + 1 << endl;
        world.update_world();
        world.display_grid();
        // Sleep for 250 milliseconds
        
    }

    return 0;
}
