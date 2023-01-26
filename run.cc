#include "run.hh"
#include <fstream>

MyRunAction::MyRunAction()
{
 
}


MyRunAction::~MyRunAction()
{}

void MyRunAction::BeginOfRunAction(const G4Run* run)
{
    std::ofstream myFile("datatest2.csv"); 
    myFile <<"particleName" << ", "<<"Track ID"<<", " << "Position (x,y,z) / mm "<< ", " << "kinEnergy / Mev"<<", "<<"time"<<", "<< "\n";
    myFile.close();   
}

void MyRunAction::EndOfRunAction(const G4Run* run)
{


    //myFile.close(); //close file
}