// filename: punjab_flood_relief.cpp
// Compile with: g++ -std=c++17 punjab_flood_relief.cpp -o relief

#include <iostream>
#include <vector>
#include <string>
using namespace std;

class Sector {
protected:
    string name;
    vector<string> facilities;
public:
    // Constructor: initialize sector name and facilities
    Sector(const string& sectorName, const vector<string>& facs)
        : name(sectorName), facilities(facs)
    {
        cout << "=== Initializing sector: " << name << " ===\n";
        cout << "Services provided:\n";
        for (size_t i = 0; i < facilities.size(); ++i) {
            cout << "  " << (i+1) << ". " << facilities[i] << "\n";
        }
        cout << endl;
    }

    // Print a short status (can be extended)
    void status() const {
        cout << "[Status] " << name << " operational. (" << facilities.size() << " services)\n";
    }

    // Destructor: announce cleanup for this sector
    virtual ~Sector() {
        cout << "+++ Shutting down sector: " << name << " (cleanup & handover) +++\n";
    }
};

// Specialized sectors (demonstrates inheritance, optional)
class RescueSector : public Sector {
public:
    RescueSector() : Sector("Rescue & Evacuation",
        {"Helicopter & boat evacuations", "NDRF/SDRF coordination", "Temporary triage and rescue centers"}) {}
    ~RescueSector() override {}
};

class ShelterSector : public Sector {
public:
    ShelterSector() : Sector("Shelter & Relief Camps",
        {"Temporary tents & community halls", "Food & drinking water distribution", "Sanitation and temporary toilets"}) {}
    ~ShelterSector() override {}
};

class MedicalSector : public Sector {
public:
    MedicalSector() : Sector("Medical Aid",
        {"Mobile medical teams", "Essential medicines & first aid", "Disease surveillance & vaccination drives"}) {}
    ~MedicalSector() override {}
};

class FinanceSector : public Sector {
public:
    FinanceSector() : Sector("Financial Assistance",
        {"Ex-gratia payments for casualties", "Farm/household compensation", "State & central relief fund disbursement"}) {}
    ~FinanceSector() override {}
};

class AgricultureSector : public Sector {
public:
    AgricultureSector() : Sector("Agriculture Support",
        {"Free seeds distribution", "Fodder for livestock", "Special girdawari (damage assessment) and compensation"}) {}
    ~AgricultureSector() override {}
};

// GovernmentRelief demonstrates dynamic creation and deletion
class GovernmentRelief {
private:
    vector<Sector*> activeSectors;
public:
    GovernmentRelief() {
        cout << "### Government Relief Program: START ###\n\n";
    }

    // Activate a sector (allocates dynamically to show destructors later)
    void activateSector(Sector* s) {
        activeSectors.push_back(s);
    }

    void showAllStatus() const {
        cout << "\n--- Current sectors status ---\n";
        for (const Sector* s : activeSectors) {
            s->status();
        }
        cout << "------------------------------\n\n";
    }

    // Clean up: delete all sectors (this triggers destructors)
    void shutdownAll() {
        cout << "\n### Shutting down all sectors and handing over to local administration ###\n";
        for (Sector* s : activeSectors) {
            delete s; // each delete calls the destructor
        }
        activeSectors.clear();
    }

    ~GovernmentRelief() {
        // Ensure cleanup if not already called
        if (!activeSectors.empty()) {
            shutdownAll();
        }
        cout << "\n### Government Relief Program: END ###\n";
    }
};

int main() {
    GovernmentRelief reliefProgram;

    // Activate sectors (constructor messages will display)
    reliefProgram.activateSector(new RescueSector());
    reliefProgram.activateSector(new ShelterSector());
    reliefProgram.activateSector(new MedicalSector());
    reliefProgram.activateSector(new FinanceSector());
    reliefProgram.activateSector(new AgricultureSector());

    // Show current status
    reliefProgram.showAllStatus();

    // Simulate some operations...
