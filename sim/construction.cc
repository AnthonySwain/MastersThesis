//Importing the headerfile
#include "construction.hh"

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

    //This is for a cerenkov detector, making areogel
    //Silica
    //             (name,density,components (silicon and oxygen))
    G4Material *SiO2 = new G4Material("SiO2", 2.201*g/cm3, 2);
    //                                            only one silica
    SiO2->AddElement(nist->FindOrBuildElement("Si"), 1);
    SiO2->AddElement(nist->FindOrBuildElement("O"), 2);

    //Water
    G4Material *H2O = new G4Material("H2O", 1.000*g/cm3, 2);
    H2O->AddElement(nist->FindOrBuildElement("H"), 2);
    H2O->AddElement(nist->FindOrBuildElement("O"), 1);

    //Carbon
    G4Element *C = nist->FindOrBuildElement("C");

    //Aerogel
    G4Material *Aerogel = new G4Material("Aerogel", 0.200*g/cm3,3);
    Aerogel->AddMaterial(SiO2, 62.5*perCent);
    Aerogel->AddMaterial(H2O, 37.4*perCent);
    Aerogel->AddElement(C, 0.1*perCent);

    //Refractive index
    G4double energy[2] = {1.239841939*eV/0.2, 1.239841939*eV/0.9 };
    G4double rindexAerogel[2] = {1.1, 1.1};
    G4double rindexWorld[2] = {1.0, 1.0};

    G4MaterialPropertiesTable *mptAerogel = new G4MaterialPropertiesTable();
    mptAerogel->AddProperty("RINDEX", energy, rindexAerogel, 2);
    //inserting refractive index property just created
    Aerogel->SetMaterialPropertiesTable(mptAerogel);


    //get parameters pre-defined for different materials
    //Pre_defined material Air and defines worldMat as that
    G4Material *worldMat = nist->FindOrBuildMaterial("G4_AIR");

    //Refractive index of air
    G4MaterialPropertiesTable *mptWorld = new G4MaterialPropertiesTable();
    mptWorld->AddProperty("RINDEX", energy, rindexWorld,2);
    worldMat->SetMaterialPropertiesTable(mptWorld);

    //All physics processes must happen in a boundary - a world volume, no geoemtry can be constructed without a world volume
    //Make it a box,  every volume has to contain 3 parts - 
    //solid: defines the size
    //logical - defines the material
    //physical - places the volume in our Geant4 application with rotation, translation ect... creates a volume that can interact with particles
    

    //making the solid one, G4Box(name, halfsize in xyz), this gives a 1m^3 box below
    G4Box *solidWorld = new G4Box("solidWorld", 0.5*m, 0.5*m, 0.5*m);

    //insert the material into the volume just made, G4LogicalVolume(solid, material,name)
    G4LogicalVolume *logicWorld = new G4LogicalVolume(solidWorld, worldMat,"logicWorld");

    //Physical Volume, G4PVPlacement(rotation,centre{usingthreevectorclass}, logic volume,name, placed in another volume,boolean opeartions,copy number,check for overlap?)
    //every volume if it touches another volume, it must be completely incorporated by that volume, define using a mother volume
    //this is the mother volume,
    G4VPhysicalVolume *physWorld = new G4PVPlacement(0,G4ThreeVector(0.,0.,0.), logicWorld, "physWorld",0,false,0,true);


    G4Box *solidRadiator = new G4Box("solidRadiator", 0.4*m, 0.4*m, 0.01*m);
    G4LogicalVolume *logicRadiator = new G4LogicalVolume(solidRadiator, Aerogel, "logicalRadiator");
    G4VPhysicalVolume *physRadiator = new G4PVPlacement(0, G4ThreeVector(0.,0.,0.25*m), logicRadiator, "physRadiator", logicWorld, false, 0, true); 

    return physWorld;


    
}