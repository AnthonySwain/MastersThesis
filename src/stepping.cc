//Writing a data output

#include "stepping.hh"
#include <string> 
#include <fstream>
#include "G4CsvNtupleManager.hh"
#include "G4AnalysisManager.hh"
#include "G4Run.hh"
#include "G4RunManager.hh"
#include "G4UnitsTable.hh"
#include "G4SystemOfUnits.hh"
#include <G4UserSteppingAction.hh>
#include <vector>
using namespace std;


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

    G4String particleName = aStep -> GetTrack() -> GetDynamicParticle() -> GetDefinition() -> GetParticleName();
    G4int particleID = aStep -> GetTrack() -> GetTrackID();

    auto prePoint = aStep->GetPreStepPoint();

    auto kinEnergyPreStep = prePoint->GetKineticEnergy();

    auto PositionPreStep = prePoint->GetPosition();


    G4double time = prePoint->GetLocalTime();
    
  //this is horribly inefficient, there must be a better way than this... 
  if (particleName == "mu-")
    {
    std::ofstream myFile("datatest2.csv",std::ios::app); //open file //append to file
    myFile <<particleName << ","
    <<particleID <<"," 
    << PositionPreStep[0] <<"," 
    << PositionPreStep[1] <<"," 
    << PositionPreStep[2] <<"," 
    << kinEnergyPreStep<<"," 
    <<time
    << "\n";
    myFile.close();
    };
    } 
   