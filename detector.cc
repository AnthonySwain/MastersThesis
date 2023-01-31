#include "detector.hh"
#include "G4HCofThisEvent.hh"
#include "G4Step.hh"
#include "G4ThreeVector.hh"
#include "G4SDManager.hh"
#include "G4Track.hh"
#include "G4ios.hh"


MySensitiveDetector::MySensitiveDetector(G4String name): G4VSensitiveDetector(name)
{
    collectionName.insert("simpleSDColl"); //Name of the collection using
}

MySensitiveDetector::~MySensitiveDetector()
{}



//Register the hits collection object in the Hits Collections of this event (GHCofThisEvent)
void MySensitiveDetector::Initialize(G4HCofThisEvent* HCE)
{
    fHitsCollection = new DetectorHitCollection(SensitiveDetectorName, collectionName[0]);
    //GetName() returns SD name, collectionName is a vector, [0] is the first element 

    //Adding this collection to the HCE
    if (fHCID<0){
        fHCID = G4SDManager::GetSDMpointer()->GetCollectionID(fHitsCollection); //To get an ID for collectionname[0]
    }
    HCE->AddHitsCollection(fHCID, fHitsCollection);
}

//Every event a new hit collection(HC) has to be created and added to current event collection of hits
//HC has 2 names - the SD Name that created it and the name of collection -UNIQUE PAir
//G4 uses an unique id to identify the collection - use this to register and retriever the collection

G4bool MySensitiveDetector::ProcessHits(G4Step *aStep, G4TouchableHistory *ROhist)
{
    auto charge = aStep->GetTrack()->GetDefinition()->GetPDGCharge();
    if (charge==0.) return true;
    //i legit have no idea why these 2 lines of code above are used but they are
    //(from example B5 in geant4)


    G4String particleName = aStep -> GetTrack() -> GetDynamicParticle() -> GetDefinition() -> GetParticleName();
    auto preStepPoint = aStep->GetPreStepPoint();
    G4ThreeVector PositionPreStep = preStepPoint->GetPosition();

    auto time = aStep ->GetTrack()->GetGlobalTime();

    //Volume Information
    auto volume = aStep->GetTrack()->GetVolume();
    auto volume_name = volume->GetName();
    auto volume_copy = volume->GetCopyNo();

    if (particleName == "mu-"){
        std::ofstream myFile("DetectorHits.csv",std::ios::app); //open file //append to file
        myFile << particleName << ", "
        << PositionPreStep << ", "
        << time << ", " 
        << volume_name << ", " 
        << volume_copy << "," 
        << "\n";
        myFile.close();
    };
    return true;
}

