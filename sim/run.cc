#include "run.hh"


#include "G4AnalysisManager.hh"
#include "G4Run.hh"
#include "G4RunManager.hh"
#include "G4UnitsTable.hh"
#include "G4SystemOfUnits.hh"


MyRunAction::MyRunAction()
{}

MyRunAction::~MyRunAction()
{}

void MyRunAction::BeginOfRunAction(const G4Run*)
{
    G4AnalysisManager *man = G4AnalysisManager::Instance();

    man->OpenFile("output.csv");

    man->CreateNtuple("Hits","Hits"); //Rows created
    man->CreateNtupleIColumn("fEvent"); //event number
    //Co-ordinates
    man->CreateNtupleIColumn("fX"); 
    man->CreateNtupleIColumn("fY");
    man->CreateNtupleIColumn("fZ");

    man-> FinishNtuple(0); //Tuple Number 0
}

void MyRunAction::EndOfRunAction(const G4Run*)
{
    G4AnalysisManager *man = G4AnalysisManager::Instance();

    man->Write();
    man->CloseFile();
}