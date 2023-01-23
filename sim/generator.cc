#include "generator.hh"

MyPrimaryGenerator::MyPrimaryGenerator()
{
    //G4ParticleGun(number of particles per event) (1 run contains several events and each event can contain several particles)
    fParticleGun = new G4ParticleGun(1);
}

MyPrimaryGenerator::~MyPrimaryGenerator()
{
    delete fParticleGun;
}

void MyPrimaryGenerator::GeneratePrimaries(G4Event *anEvent)
{
    //table of particles
    G4ParticleTable *particleTable = G4ParticleTable::GetParticleTable();
    //finding the particle
    G4String particleName="proton";
    G4ParticleDefinition *particle = particleTable->FindParticle("proton");

    //where the particle is created
    G4ThreeVector pos(0.,0.,0.);
    //diretion of particle
    G4ThreeVector mom(0.,0.,1.);


    //use the particle gun to make the particle, defining the properties
    fParticleGun->SetParticlePosition(pos);
    fParticleGun->SetParticleMomentumDirection(mom);
    fParticleGun->SetParticleMomentum(100.*GeV);
    fParticleGun->SetParticleDefinition(particle);

    //Generates
    fParticleGun->GeneratePrimaryVertex(anEvent);
}   
