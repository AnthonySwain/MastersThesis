//Setting up the particle detectors
#include "detector.hh"
#include "G4HCofThisEvent.hh"
#include "G4Step.hh"
#include "G4ThreeVector.hh"
#include "G4SDManager.hh"
#include "G4Track.hh"
#include "G4ios.hh"
#include "G4Run.hh"
#include "G4RunManager.hh"
#include "CSVoutput.hh"

MySensitiveDetector::MySensitiveDetector(G4String name, H5::Group* output) : G4VSensitiveDetector(name), m_writer(*output, "DetectorOutput")
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
    //Every event a new hit collection(HC) has to be created and added to current event collection of hits
//HC has 2 names - the SD Name that created it and the name of collection -UNIQUE PAir
//G4 uses an unique id to identify the collection - use this to register and retriever the collection
} 

G4bool MySensitiveDetector::ProcessHits(G4Step *aStep, G4TouchableHistory */*ROhist*/)
{
    //Looking for charged particles only 
    auto charge = aStep->GetTrack()->GetDefinition()->GetPDGCharge();
    if (charge==0.) return true;


    //G4String particleName = aStep -> GetTrack() -> GetDynamicParticle() -> GetDefinition() -> GetParticleName();
    int PDGnumb = aStep -> GetTrack() -> GetDynamicParticle() -> GetPDGcode();
    auto preStepPoint = aStep->GetPreStepPoint();
    G4ThreeVector PositionPreStep = preStepPoint->GetPosition();

    double momentum = aStep -> GetDeltaEnergy();
    auto time = aStep ->GetTrack()->GetGlobalTime();
    auto event_no = G4RunManager::GetRunManager()->GetCurrentEvent()->GetEventID();
    
    //Volume Information
    auto volume = aStep->GetTrack()->GetVolume();
    auto volume_name = volume->GetName();
    
    //Using a reference number for volume names (In/OutDetector so strings are not saved in H5 file)
    int volume_ref_no;
    if (volume_name == "InDetector1"){
        volume_ref_no = 00;
    };

    if (volume_name == "InDetector2"){
        volume_ref_no = 01;
    };

    if (volume_name == "OutDetector1"){
        volume_ref_no = 10;
    };

    if (volume_name == "OutDetector2"){
        volume_ref_no = 11;
    };
    
    auto volume_copy = volume->GetCopyNo();
   
    if (PDGnumb == 13 or PDGnumb == -13){
        /*
        CSVoutput output;
        output.DetectorOutput(
            event_no,
            PDGnumb,
            PositionPreStep[0],
            PositionPreStep[1],
            PositionPreStep[2],
            time,
            volume_ref_no,
            volume_copy);
        */
        
        using namespace H5CompositesStructures;
        DetectorOutput data;
        
        data = DetectorOutput{
            .event_no = event_no,
            .PDGnumb = PDGnumb,
            .PosX = PositionPreStep[0],
            .PosY = PositionPreStep[1],
            .PosZ = PositionPreStep[2],
            .time = time,
            .volume_ref = volume_ref_no,
            .volume_no = volume_copy,
            .momentum = momentum
            };
        
        m_writer.write(data);
        
        };
    

    return true;
}

