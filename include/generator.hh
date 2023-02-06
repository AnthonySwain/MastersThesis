//Particle gun
#ifndef GENERATOR_HH
#define GENERATOR_HH

#include "G4VUserPrimaryGeneratorAction.hh"

#include "G4ParticleGun.hh"
#include "G4SystemOfUnits.hh"
#include "G4ParticleTable.hh"
#include "G4ParticleDefinition.hh"

class MyPrimaryGenerator : public G4VUserPrimaryGeneratorAction
{
public:
    MyPrimaryGenerator();
    ~MyPrimaryGenerator();

    //runs the particle gun and computes the stepping ect...
    virtual void GeneratePrimaries(G4Event*);

//define the particle gun
private:
//data members
    G4ParticleGun *fParticleGun; //pointer to G4 serice class
};

#endif