//Header file for constructing detectors
//Make sure it's not included serveral times
#ifndef CONSTRUCTION_HH
#define CONSTRUCTION_HH

#include "G4VUserDetectorConstruction.hh"
#include "G4VPhysicalVolume.hh"
#include "G4LogicalVolume.hh"
#include "G4Box.hh"
#include "G4PVPlacement.hh"
#include "G4NistManager.hh"


//Use different units that are pre-implemented in G4
#include "G4SystemOfUnits.hh"

//Class for detectors - inherited from class below from G4
class MyDetectorConstruction : public G4VUserDetectorConstruction
{
public:
    //constructor
    MyDetectorConstruction();
    //destructor
    ~MyDetectorConstruction();

    //Main functino that constructs the whole detector geometry, description of detector should be in this functino
    virtual G4VPhysicalVolume *Construct();
};

#endif