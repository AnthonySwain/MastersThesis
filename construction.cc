//Importing the headerfile
#include "construction.hh"

#define _USE_MATH_DEFINES
#include <cmath>
#include <G4Tubs.hh>

//Constructor
MyDetectorConstruction::MyDetectorConstruction()
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
    G4Box *solidWorld = new G4Box("solidWorld", 1*m, 1*m, 2*m);

    //insert the material into the volume just made, G4LogicalVolume(solid, material,name)
    G4LogicalVolume *logicWorld = new G4LogicalVolume(solidWorld, worldMat,"logicWorld");

    //Physical Volume, G4PVPlacement(rotation,centre{usingthreevectorclass}, logic volume,name, placed in another volume,boolean opeartions,copy number,check for overlap?)
    //every volume if it touches another volume, it must be completely incorporated by that volume, define using a mother volume
    //this is the mother volume,
    G4VPhysicalVolume *physWorld = new G4PVPlacement(0,G4ThreeVector(0.,0.,0.), logicWorld, "physWorld",0,false,0,true);


    //Making the concrete volume
    G4Material *Concrete = nist->FindOrBuildMaterial("G4_CONCRETE");
    G4MaterialPropertiesTable *mptConcrete = new G4MaterialPropertiesTable();
    G4Box *solidConcrete = new G4Box("solidConcrete", 0.5*m, 0.5*m, 1*m);
    G4LogicalVolume *logicConcrete = new G4LogicalVolume(solidConcrete, Concrete,"logicConcrete");
    G4VPhysicalVolume *physConcrete = new G4PVPlacement(0,G4ThreeVector(0.,0.,0.), logicConcrete, "physConcrete",logicWorld,false,0,true);

    
    //Making the steel volume inside the concrete volume
    //Steel is a mixture of elements so need to comprise it of carbon and iron
    G4Element *C = nist->FindOrBuildElement("C"); //Carbon
    G4Element *Fe = nist->FindOrBuildElement("Fe"); //Iron
    
    //Steel Composition & Properties
    G4Material *Steel = new G4Material("Steel", 7.800*g/cm3,2);
    Steel->AddElement(C, 1*perCent);
    Steel->AddElement(Fe, 99*perCent);
    G4MaterialPropertiesTable *mptSteel = new G4MaterialPropertiesTable();

    //Adding the steel Rod      
    G4Tubs *solidSteel = new G4Tubs("solidSteel",
                                    0., //inner radius
                                    1*cm, //outer radius
                                    50.*cm, // half z distance
                                    0., //start Phi angle
                                    2*M_PI*rad); //End Phi Angle


    G4LogicalVolume *logicSteel = new G4LogicalVolume(solidSteel, Steel,"Steel");
    G4VPhysicalVolume *physSteel = new G4PVPlacement(
                                                0, //no rotation
                                                G4ThreeVector(0.,0.,0.), //its position
                                                logicSteel, //its logical volume
                                                "physSteel", //name
                                                logicConcrete, //mothervolume
                                                false, //no boolean operation
                                                0, //copy number
                                                true); //check for overlaps
                                                
    
    

    return physWorld;


    
}