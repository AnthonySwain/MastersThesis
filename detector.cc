#include "detector.hh"
#include "G4HCofThisEvent.hh"
#include "G4Step.hh"
#include "G4ThreeVector.hh"
#include "G4SDManager.hh"
#include "G4ios.hh"


MySensitiveDetector::MySensitiveDetector(const G4String& name, 
                                         const G4String& hitsCollectionName)
                                        : G4VSensitiveDetector(name), fNofCells(nofCells)
{
    collectionName.insert(hitsCollectionName); //Name of the collection using (prob should look up what a collection is
    
}

MySensitiveDetector::~MySensitiveDetector()
{}

G4bool MySensitiveDetector::ProcessHits(G4Step *aStep, G4TouchableHistory *ROhist)
{
    //energy deposit
    auto edep = aStep ->GetTotalEnergyDeposit();

    //step length
    G4double stepLength = 0.;
    if (aStep->GetTrack()->GetDefinition()->GetPDGCharge() !=0.){
        stepLength = aStep ->GetStepLength();
    }

    //HERE YOU ARE HERE BOI 

    G4TouchableHandle touchable = aStep->GetPreStepPoint()->GetTouchableHandle();
    G4int copyNo = touchable->GetVolume(0)->GetCopyNo(); //Get the volume where the G4 is
    
    
    /*
    //Entering The Detector
    G4StepPoints *preStepPoint = aStep->GetPreStepPoint 
    //Leaves
    G4StepPoints *postStepPoint = aStep->GetPostStepPoint*/ 
}

//Register the hits collection object in the Hits Collections of this event (GHCofThisEvent)
void MySensitiveDetector::Initialize(GHofThisEvent* HCE)
{
    fHitsCollection = new DetectorHitCollection(SensitiveDetectorName, collectionName[0]);
    //GetName() returns SD name, collectionName is a vector, [0] is the first element 

    //Adding this collection to the HCE
    HCID = G4SDManager::GETSDMpointer()->GetCollectionID(collectionName[0]); //To get an ID for collectionname[0]
    HCE->AddHitsCollection(HCID, hitCollection);

    //Create hits
//fNofCells for cells + one more for total sums
for (G4int i=0 i<fNofCells+1; i++) {
    fHitsCollection->insert(new DetectorHit()):
    }
}
//Every event a new hit collection(HC) has to be created and added to current event collection of hits
//HC has 2 names - the SD Name that created it and the name of collection -UNIQUE PAir
//G4 uses an unique id to identify the collection - use this to register and retriever the collection

