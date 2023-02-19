//Writing a data output

#include "stepping.hh"
#include "G4CsvNtupleManager.hh"
#include "G4AnalysisManager.hh"
#include "G4Run.hh"
#include "G4RunManager.hh"
#include "G4UnitsTable.hh"
#include "G4SystemOfUnits.hh"
#include <G4UserSteppingAction.hh>
#include "CSVoutput.hh"
#include "H5output.hh"

//Constructor
MySteppingAction::MySteppingAction(MyRunAction *runAction)
{
    fRunAction = runAction; //get access
}

//Destructor
MySteppingAction::~MySteppingAction()
{}

void MySteppingAction::UserSteppingAction(const G4Step *aStep)
{

    //extracting data
    G4double edep = aStep -> GetTotalEnergyDeposit();

    //G4String particleName = aStep -> GetTrack() -> GetDynamicParticle() -> GetDefinition() -> GetParticleName();
    G4int particleID = aStep -> GetTrack() -> GetTrackID();

    int PDGnumb = aStep -> GetTrack() -> GetDynamicParticle() -> GetPDGcode();
    auto prePoint = aStep->GetPreStepPoint();

    auto kinEnergyPreStep = prePoint->GetKineticEnergy();

    auto PositionPreStep = prePoint->GetPosition();
    
    auto event_no = G4RunManager::GetRunManager()->GetCurrentEvent()->GetEventID();

    G4double time = prePoint->GetLocalTime();
    
    if (PDGnumb == 13 or PDGnumb == -13){

        /*
        H5output::RealityOutput(event_no,
            PDGnumb,
            particleID,
            PositionPreStep[0],
            PositionPreStep[1],
            PositionPreStep[2],
            kinEnergyPreStep,
            time);*/
        CSVoutput output;
        output.RealityOutput(event_no,
            PDGnumb,
            particleID,
            PositionPreStep[0],
            PositionPreStep[1],
            PositionPreStep[2],
            kinEnergyPreStep,
            time);
        };
    } 
   