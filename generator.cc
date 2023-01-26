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
    G4String particleName="mu-";
    G4ParticleDefinition *particle = particleTable->FindParticle(particleName);

    //where the particle is created
    G4ThreeVector pos(0.5,0.5,2);
    //diretion of particle
    G4ThreeVector mom(0.,0.01,1.);


    //use the particle gun to make the particle, defining the properties
    fParticleGun->SetParticlePosition(pos); //initial position
    fParticleGun->SetParticleMomentumDirection(mom); //this is the direction of the particle
    fParticleGun->SetParticleMomentum(3.*GeV); //magnitude of momentum
    fParticleGun->SetParticleDefinition(particle); //what the particle is

    //Generates - called at the beginning of an event
    fParticleGun->GeneratePrimaryVertex(anEvent);
}   
