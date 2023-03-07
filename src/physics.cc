#include "physics.hh"

MyPhysicsList::MyPhysicsList()
{
    //include the physics that we want to use
    RegisterPhysics ( new G4EmStandardPhysics()); //EM Interactions
    //RegisterPhysics ( new G4OpticalPhysics()); //Optical Photons

};
MyPhysicsList::~MyPhysicsList()
{};