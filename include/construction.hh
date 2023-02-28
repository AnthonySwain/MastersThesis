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
#include "detector.hh"
#include "ParticleData.h"
#include "/home/anthony/MastersThesis/lib/H5Composites/include/H5Composites/GroupWrapper.h"
#include "/home/anthony/MastersThesis/lib/H5Composites/include/H5Composites/TypedWriter.h"
//Use different units that are pre-implemented in G4
#include "G4SystemOfUnits.hh"

//Class for detectors - inherited from class below from G4
class MyDetectorConstruction : public G4VUserDetectorConstruction
{
public:
    //constructor
    MyDetectorConstruction(H5::Group* output);
    //destructor
    ~MyDetectorConstruction();

    //Main functino that constructs the whole detector geometry, description of detector should be in this functino
    virtual G4VPhysicalVolume *Construct();

private: 
    G4LogicalVolume *logicDetector; //acccess it outside of construction function
    virtual void ConstructSDandField();//construct sensitive detector (also EM fields)
    H5::Group* group; 

};

#endif