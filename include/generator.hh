//Particle gun 
//Generates the muons
#ifndef GENERATOR_HH
#define GENERATOR_HH

#include "G4VUserPrimaryGeneratorAction.hh"
#include "EcoMug.h"
#include "G4ParticleGun.hh"
#include "G4SystemOfUnits.hh"
#include "G4ParticleTable.hh"
#include "run.hh"
#include "G4ParticleDefinition.hh"
#include <cmath>
#include "ParticleData.h"
#include "GroupWrapper.h"
#include "TypedWriter.h"

class MyPrimaryGenerator : public G4VUserPrimaryGeneratorAction
{
public:
    MyPrimaryGenerator(H5::Group &output);
    ~MyPrimaryGenerator();

    //runs the particle gun and computes the stepping ect...
    virtual void GeneratePrimaries(G4Event*);

//define the particle gun
private:
//data members
    G4ParticleGun *fParticleGun; //pointer to G4 serice class
    H5Composites::TypedWriter<H5CompositesStructures::InitialParticleData> m_writer;
};

#endif