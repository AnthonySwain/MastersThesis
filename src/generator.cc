#include "generator.hh"
#include "G4RunManager.hh"
#include "CSVoutput.hh"
#include "H5output.hh"


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
    EcoMug gen; //initialises Ecomug generator
    gen.SetUseSky(); //plane surface to generate the muons on
    gen.SetSkySize({{1*m,1*m}}); //x and y size of the sky
    gen.SetSkyCenterPosition({{0.,0.,1.4*m}}); //set center of the sky

    // The array storing muon generation position
    std::array<double, 3> muon_position_array;
    
    //Getting position, theta,thi,charge for the generated muon.
    gen.Generate();
    muon_position_array = gen.GetGenerationPosition();
    double muon_p = gen.GetGenerationMomentum();
    auto muon_theta = gen.GetGenerationTheta();
    auto muon_phi = gen.GetGenerationPhi();
    int muon_charge = gen.GetCharge();

    //table of particles
    G4ParticleTable *particleTable = G4ParticleTable::GetParticleTable();
    //finding the particle
    //assigning muon / anti-muon

    G4String particleName;
    G4int PDGnumb;
    if (muon_charge==1){
        particleName="mu-";
        PDGnumb = 13;
        }

    if (muon_charge==-1){
        particleName= "mu+";
        PDGnumb = -13;
        }

    //probably should output seed here 
    //output to H5 data format
    /*
    H5output::InitialMuonOutput(
        PDGnumb,
        muon_p,
        muon_theta,
        muon_phi,
        muon_position_array[0],
        muon_position_array[1],
        muon_position_array[2]
    );*/
    
    //Output to CSV format
    CSVoutput output;
    output.InitialMuonOutput(
        PDGnumb,
        muon_p,
        muon_theta,
        muon_phi,
        muon_position_array[0],
        muon_position_array[1],
        muon_position_array[2]);

    
    G4ParticleDefinition *particle = particleTable->FindParticle(particleName);

    //where the particle is created
    G4ThreeVector pos(muon_position_array[0],muon_position_array[1],muon_position_array[2]);
    
    //diretion of particle
    G4ThreeVector mom(sin(muon_theta)*cos(muon_phi),sin(muon_theta)*sin(muon_phi),cos(muon_theta));

    //use the particle gun to make the particle, defining the properties
    fParticleGun->SetParticlePosition(pos); //initial position
    fParticleGun->SetParticleMomentumDirection(mom); //this is the direction of the particle
    fParticleGun->SetParticleMomentum(muon_p*GeV); //magnitude of momentum
    fParticleGun->SetParticleDefinition(particle); //what the particle is

    //Generates - called at the beginning of an event
    fParticleGun->GeneratePrimaryVertex(anEvent);

}   

