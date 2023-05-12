//Main simulation file - calls upon src and geant4 toolkit. 
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
#include "GroupWrapper.h"
#include "TypedWriter.h"


#include "construction.hh"
#include "physics.hh"
//#include "action.hh"

int main(int argc, char** argv)
{   

    //Create the output file
    H5Composites::GroupWrapper fOut = H5Composites::GroupWrapper::createFile("/home/anthony/MastersThesis/Data/RustedBeam10mm2.h5",true);
    
    //Getting the group from the group wrapper
    H5::Group group = fOut.group();
    G4cout << &group;

    //Heart of Geant4, takes care of run, event actions, stepping ect... ect...
        
    G4RunManager mgr;
    mgr.SetUserInitialization(new MyDetectorConstruction(&group));
    mgr.SetUserInitialization(new MyPhysicsList());

    MyPrimaryGenerator *generator = new MyPrimaryGenerator(group);
    mgr.SetUserAction(generator);

    MyRunAction *runAction = new MyRunAction();
    mgr.SetUserAction(runAction);

    MySteppingAction *steppingAction = new MySteppingAction(runAction, group);
    mgr.SetUserAction(steppingAction);

    mgr.Initialize();

    
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