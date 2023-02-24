//Imports
#include <iostream>
#include "G4RunManager.hh"
#include "G4UImanager.hh"
#include "G4VisManager.hh"
#include "G4VisExecutive.hh"
#include "G4UIExecutive.hh"
#include "G4VUserActionInitialization.hh"
#include "generator.hh"
#include "stepping.hh"

#include "ParticleData.h"
#include "../lib/H5Composites/include/H5Composites/GroupWrapper.h"
#include "../lib/H5Composites/include/H5Composites/TypedWriter.h"

#include "construction.hh"
#include "physics.hh"
//#include "action.hh"

int main(int argc, char** argv)
{   

    //Create the output file
    H5Composites::GroupWrapper fOut = H5Composites::GroupWrapper::createFile("OutputTest.h5",true);
    
    //Getting the group from the group wrapper
    //H5::Group group;
    H5::Group group = fOut.group();

    //Then pass the group onto each  function and do what jon has baso given me on a fruit platter...
    // Prepare the details writers
    //H5Composites::TypedWriter<H5CompositesStructures::InitialParticleData> genWriter = fOut.makeDataSetWriter<H5CompositesStructures::InitialParticleData>("InitialMuon");
    //H5Composites::TypedWriter<H5CompositesStructures::DetectorOutput> detectorWriter = fOut.makeDataSetWriter<H5CompositesStructures::DetectorOutput>("DetectorOutput");
    //H5Composites::TypedWriter<H5CompositesStructures::Reality> detailsWriter = fOut.makeDataSetWriter<H5CompositesStructures::Reality>("TruthData");


    //Heart of Geant4, takes care of run, event actions, stepping ect... ect...
    G4RunManager mgr; 
    mgr.SetUserInitialization(new MyDetectorConstruction());
    mgr.SetUserInitialization(new MyPhysicsList());

    MyPrimaryGenerator *generator = new MyPrimaryGenerator();
    mgr.SetUserAction(generator);

    MyRunAction *runAction = new MyRunAction();
    mgr.SetUserAction(runAction);

    MySteppingAction *steppingAction = new MySteppingAction(runAction, group);
    mgr.SetUserAction(steppingAction);

    mgr.Initialize();

    /*
    //Initialise constructor, physics list, ect... - also send the writers to each one
    runManager->SetUserInitialization(new MyDetectorConstruction();
    runManager->SetUserInitialization(new MyPhysicsList());
    runManager->SetUserInitialization(new MyActionInitialization(group));
    
    //Initialise G4 Kernel, performs detector construction, creates the physics processes, calculates cross sections, sets up the run
    runManager->Initialize();
    */
    //User interface
    G4UIExecutive *ui = new G4UIExecutive(argc, argv);

    //Visualisation Manager
    G4VisManager *visManager = new G4VisExecutive();
    
    //Initialize visualisation
    visManager->Initialize();

    //Get the pointer tp the UI manager, set verbosities
    G4UImanager *UImanager = G4UImanager::GetUIpointer();
    
    //Run the macro file
    UImanager->ApplyCommand("/control/execute run.mac");
    ui->SessionStart();

    return 0;
}