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



MySteppingAction::MySteppingAction(MyRunAction *runAction)
{
    fRunAction = runAction; //get access
}

MySteppingAction::~MySteppingAction()
{}

void MySteppingAction::UserSteppingAction(const G4Step *aStep)
{

    G4double edep = aStep -> GetTotalEnergyDeposit();

    G4String particleName = aStep -> GetTrack() -> GetDynamicParticle() -> GetDefinition() -> GetParticleName();
    
  

    G4StepPoint* prePoint = aStep->GetPreStepPoint();
    G4StepPoint* postPoint = aStep->GetPostStepPoint();

    G4double kinEnergyPreStep = prePoint->GetKineticEnergy();
    G4double kinEnergyPostStep = postPoint->GetKineticEnergy();

    G4ThreeVector PositionPreStep = prePoint->GetPosition();
    G4ThreeVector PositionPostStep = postPoint->GetPosition();

    G4double time = prePoint->GetLocalTime();
    
//this is horrible inefficient, there must be a better way than this... 
  if (particleName == "proton")
    {
    std::ofstream myFile("datatest2.csv",std::ios::app); //open file //append to file
    myFile <<particleName << ", " << PositionPreStep <<", " << kinEnergyPreStep<<", " <<time<<", " << "\n";
    myFile.close();
    };
    } 
   