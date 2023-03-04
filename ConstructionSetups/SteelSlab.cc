//Importing the headerfile
#include "construction.hh"
#include "G4SDManager.hh"
#define _USE_MATH_DEFINES
#include <cmath>
#include <G4Tubs.hh>
#include "G4VisAttributes.hh"
#include <G4Colour.hh>
#include "G4RotationMatrix.hh"
#include "G4ThreeVector.hh"
#include "G4PhysicalConstants.hh"
#include "G4SystemOfUnits.hh"
#include "ParticleData.h"
#include "/home/anthony/MastersThesis/lib/H5Composites/include/H5Composites/GroupWrapper.h"
#include "/home/anthony/MastersThesis/lib/H5Composites/include/H5Composites/TypedWriter.h"


//Constructor
MyDetectorConstruction::MyDetectorConstruction(H5::Group* output) : group{output}
{}

//Destructor
MyDetectorConstruction::~MyDetectorConstruction()
{}

G4VPhysicalVolume *MyDetectorConstruction::Construct()
{
    //Define material, using from pre-defined in G4
    G4NistManager *nist = G4NistManager::Instance();

    //get parameters pre-defined for different materials
    //Pre_defined material Air and defines worldMat as that
    G4Material *worldMat = nist->FindOrBuildMaterial("G4_AIR");

    //Refractive index of air
    G4MaterialPropertiesTable *mptWorld = new G4MaterialPropertiesTable();
    
    //All physics processes must happen in a boundary - a world volume, no geoemtry can be constructed without a world volume
    //Make it a box,  every volume has to contain 3 parts - 
    //solid: defines the size
    //logical - defines the material
    //physical - places the volume in our Geant4 application with rotation, translation ect... creates a volume that can interact with particles
    

    //making the solid one, G4Box(name, halfsize in xyz), this gives a 1m^3 box below
    G4Box *solidWorld = new G4Box("solidWorld", 2*m, 2*m, 2*m);

    //insert the material into the volume just made, G4LogicalVolume(solid, material,name)
    G4LogicalVolume *logicWorld = new G4LogicalVolume(solidWorld, worldMat,"logicWorld");

    //Physical Volume, G4PVPlacement(rotation,centre{usingthreevectorclass}, logic volume,name, placed in another volume,boolean opeartions,copy number,check for overlap?)
    //every volume if it touches another volume, it must be completely incorporated by that volume, define using a mother volume
    //this is the mother volume,
    G4VPhysicalVolume *physWorld = new G4PVPlacement(0,G4ThreeVector(0.,0.,0.), logicWorld, "physWorld",0,false,0,true);

   
    //Making the steel volume inside the concrete volume
    //Steel is a mixture of elements so need to comprise it of carbon and iron
    G4Element *C = nist->FindOrBuildElement("C"); //Carbon
    G4Element *Fe = nist->FindOrBuildElement("Fe"); //Iron
    
    //Steel Composition & Properties
    G4Material *Steel = new G4Material("Steel", 7.800*g/cm3,2);
    Steel->AddElement(C, 1*perCent);
    Steel->AddElement(Fe, 99*perCent);
    G4MaterialPropertiesTable *mptSteel = new G4MaterialPropertiesTable();

    G4Box *solidSteel = new G4Box("solidSteel", 1.0*m, 0.5*m, 7.5*cm)

    //Adding the steel plate    
    G4LogicalVolume *logicSteel = new G4LogicalVolume(solidSteel, Steel,"Steel");
    G4VPhysicalVolume *physSteel = new G4PVPlacement(0,G4ThreeVector(0.,0.,0.), logicSteel, "physSteel",logicWorld,false,0,true);

    //Physical Properties of the detector
    G4Element *Si = nist->FindOrBuildElement("Si"); //Silicon
    G4Material *Detector = new G4Material("Detector", 2.329*g/cm3,1);
    Detector->AddElement(Si,100*perCent);
    G4MaterialPropertiesTable *mptDetector = new G4MaterialPropertiesTable();
    
    //Adding The Detectors either side of the concrete 

    G4Box *solidDetector = new G4Box("solidDetector", 0.75*m, 0.6*m, 0.0005*m);
    G4LogicalVolume *logicDetector = new G4LogicalVolume(solidDetector, Detector, "logicDetector");

    
    //Creating layers of particle detectors either side of the sample
    for(G4int i = 0; i<2; i++)
    {
    //Detectors on one side
        G4VPhysicalVolume *physDetector00 = new G4PVPlacement(
                                                            0, //no rotation
                                                            G4ThreeVector(0.,0., 0.525*m + i*0.005*m),  //position
                                                            logicDetector, //Logical volume
                                                            "InDetector1",  //name
                                                            logicWorld,  //mother volume
                                                            false,  //no boolean operation
                                                            i,  //copy number
                                                            true  //check for overlaps
                                                            );
    
    //Detectors on the other side
        G4VPhysicalVolume *physDetector10 = new G4PVPlacement(
                                                            0, //no rotation
                                                            G4ThreeVector(0.,0.,-0.525*m - i*0.005*m),  //position
                                                            logicDetector, //Logical volume
                                                            "OutDetector1",  //name
                                                            logicWorld,  //mother volume
                                                            false,  //no boolean operation
                                                            i,  //copy number
                                                            true  //check for overlaps
                                                            );

        G4VPhysicalVolume *physDetector11 = new G4PVPlacement(
                                                            0, //no rotation
                                                            G4ThreeVector(0.,0.,-0.725*m - i*0.005*m),  //position
                                                            logicDetector, //Logical volume
                                                            "OutDetector2",  //name
                                                            logicWorld,  //mother volume
                                                            false,  //no boolean operation
                                                            i,  //copy number
                                                            true  //check for overlaps
                                                            );
        
        G4VPhysicalVolume *physDetector01 = new G4PVPlacement(
                                                            0, //no rotation
                                                            G4ThreeVector(0.,0.,0.725*m + i*0.005*m),  //position
                                                            logicDetector, //Logical volume
                                                            "InDetector2",  //name
                                                            logicWorld,  //mother volume
                                                            false,  //no boolean operation
                                                            i,  //copy number
                                                            true  //check for overlaps
                                                            );
    };
    //Setting Visualisation Properties

    //make air (world volume) invisible
    logicWorld->SetVisAttributes (G4VisAttributes::GetInvisible()); 

    //make the detectors red
    auto DetectorVisAtt = new G4VisAttributes(G4Colour(1.0,0,0)); 
    DetectorVisAtt->SetVisibility(true);
    logicDetector->SetVisAttributes(DetectorVisAtt);
    
    return physWorld;
}

//Adding sensitive detector construction
void MyDetectorConstruction::ConstructSDandField()
{
    G4cout << group;
    auto simpleSD = new MySensitiveDetector("simpleSD", group);
    G4SDManager::GetSDMpointer()->AddNewDetector(simpleSD);
    
    //Assigning the detectors to be sensit
    SetSensitiveDetector("logicDetector", simpleSD);
}