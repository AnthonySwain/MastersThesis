//Code that gets run every event
#include "run.hh"
#include <fstream>

MyRunAction::MyRunAction()
{}

MyRunAction::~MyRunAction()
{}

void MyRunAction::BeginOfRunAction(const G4Run* run)
{   
    //Comments are from when CSV was being used as output.


    //Runs at the start of each run
    /*
    //Setting up the header of the datafiles
    std::ofstream myFile("datatest2.csv"); 
    myFile << "event_no" << ","
    <<"PDGnumb" << ","
    <<"Track ID"<<"," 
    << "PosX" << ","
    << "PosY" << ","
    << "PosZ" << ","
    << "kinEnergy / Mev"<<","
    <<"time"
    << "\n";
    myFile.close();

    //Hits on Detector
    std::ofstream myFile2("DetectorHits.csv");
    myFile2 << "event_no" << ","
    << "PDGnumb" << ","
    << "PosX" << ","
    << "PosY" << ","
    << "PosZ" << ","
    << "time" << "," 
    << "volume_name" << "," 
    << "volume_copy" 
    << "\n";
    myFile2.close();

    //Muon distribution
    std::ofstream myFile3("Initial_Muon_Dist.csv");
    myFile3 << "PDGnumb" << ","
    << "PosX" << ","
    << "PosY" << ","
    << "PosZ" << ","
    << "Momentum[GeV]" << ","
    << "theta" << ","
    << "phi" 
    << "\n";
    myFile3.close();
    */
}

void MyRunAction::EndOfRunAction(const G4Run* run)
{}