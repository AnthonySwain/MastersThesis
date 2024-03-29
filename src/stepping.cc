//Stepping - used for data output along steps

#include "stepping.hh"
#include "G4CsvNtupleManager.hh"
#include "G4AnalysisManager.hh"
#include "G4Run.hh"
#include "G4RunManager.hh"
#include "G4UnitsTable.hh"
#include "G4SystemOfUnits.hh"
#include <G4UserSteppingAction.hh>
#include "CSVoutput.hh"
#include "ParticleData.h"

//Constructor{
MySteppingAction::MySteppingAction(MyRunAction *runAction, H5::Group &output) : m_writer(output, "StepData")
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
        CSVoutput output;
        output.RealityOutput(event_no,
            PDGnumb,
            particleID,
            PositionPreStep[0],
            PositionPreStep[1],
            PositionPreStep[2],
            kinEnergyPreStep,
            time);
        */
        
        using namespace H5CompositesStructures;
        Reality data;
        
        data = Reality{
            .event_no = event_no,
            .Track_ID = particleID,
            .PDGnumb = PDGnumb,
            .PosX = PositionPreStep[0],
            .PosY = PositionPreStep[1],
            .PosZ = PositionPreStep[2],
            .time = time,
            .kinEnergy = kinEnergyPreStep
            };
        
        m_writer.write(data);
        
        };
    } 
   