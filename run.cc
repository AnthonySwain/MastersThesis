#include "run.hh"
#include <fstream>

MyRunAction::MyRunAction()
{
 
}


MyRunAction::~MyRunAction()
{}

void MyRunAction::BeginOfRunAction(const G4Run* run)
{   
    //Setting up the header of the datafiles
    std::ofstream myFile("datatest2.csv"); 
    myFile <<"particleName" << ", "<<"Track ID"<<", " << "Position (x,y,z) / mm "<< ", " << "kinEnergy / Mev"<<", "<<"time"<<", "<< "\n";
    myFile.close();

    std::ofstream myFile2("DetectorHits.csv",std::ios::app); //open file //append to file
        myFile2 << "particleName" << ", "
        << "Position" << ", "
        << "time" << ", " 
        << "volume_name" << ", " 
        << "volume_copy" << "," 
        << "\n";
        myFile2.close();
}

void MyRunAction::EndOfRunAction(const G4Run* run)
{


    //myFile.close(); //close file
}