#ifndef DETECTOR_HH
#define DETECTOR_HH


#include "G4VSensitiveDetector.hh"
#include "hit.hh"
#include <vector>
#include "ParticleData.h"
#include "GroupWrapper.h"
#include "TypedWriter.h"
#include "run.hh"


//Define hit collection / hit container



class MySensitiveDetector : public G4VSensitiveDetector
{
public:
    MySensitiveDetector(G4String name,  H5::Group* output); //constructor (G4String is the name of the detector)
    ~MySensitiveDetector();

    //methods from base class? 
    void Initialize(G4HCofThisEvent* hitCollection);
    G4bool ProcessHits(G4Step *, G4TouchableHistory *); //called for G4Step in sensitive volume
    //void EndOfEvent(G4HCofThisEvent* hitCollection);

private:
    DetectorHitCollection* fHitsCollection = nullptr;
    /*G4int fNofCells = 0;*/
    G4int fHCID = -1;
    H5Composites::TypedWriter<H5CompositesStructures::DetectorOutput> m_writer;

        
};

#endif