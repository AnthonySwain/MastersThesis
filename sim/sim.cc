//Imports
#include <iostream>
#include "G4RunManager.hh"
#include "G4UImanager.hh"
#include "G4VisManager.hh"
#include "G4VisExecutive.hh"
#include "G4UIExecutive.hh"

#include "construction.hh"
#include "physics.hh"
#include "action.hh"

int main(int argc, char** argv)
{
    //Heart of Geant4, takes care of run, event actions, stepping ect... ect...
    G4RunManager *runManager = new G4RunManager();

    //Initialise constructor, physics list,
    runManager->SetUserInitialization(new MyDetectorConstruction());
    runManager->SetUserInitialization(new MyPhysicsList());
    runManager->SetUserInitialization(new MyActionInitialization());
    runManager->Initialize();

    //User interface
    G4UIExecutive *ui = new G4UIExecutive(argc, argv);

    //Visualisation Manager
    G4VisManager *visManager = new G4VisExecutive();
    
    //Initialize
    visManager->Initialize();

    //Unsure, just copy pasted
    G4UImanager *UImanager = G4UImanager::GetUIpointer();

    //Tells geant4 to display
    UImanager->ApplyCommand("/vis/open OGL");
    //Draw the volume
    UImanager->ApplyCommand("/vis/drawVolume");
    //Draw trajectories
    UImanager->ApplyCommand("/vis/scene/add/trajectories smooth");
    //Change the initial position of the display
    UImanager->ApplyCommand("/vis/viewer/set/viewpointVector 1 1 1 ");
    //Update every event
    UImanager->ApplyCommand("/vis/viewer/set/autoRefresh true");
    //Start the session from G4
    UImanager->ApplyCommand("/vis/scence/endOfEventAction accumulate");
    ui->SessionStart();

    return 0;
}