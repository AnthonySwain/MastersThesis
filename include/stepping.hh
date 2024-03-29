//Stepping 
#ifndef STEPPING_HH
#define STEPPING_HH

#include "G4UserSteppingAction.hh"
#include "G4Step.hh"
#include "ParticleData.h"
#include "GroupWrapper.h"
#include "TypedWriter.h"
#include "construction.hh"

#include "run.hh"

class MySteppingAction: public G4UserSteppingAction
{
public:
    MySteppingAction(MyRunAction* runAction, H5::Group &output);
    ~MySteppingAction();

    virtual void UserSteppingAction(const G4Step*);

private: 
    MyRunAction *fRunAction;
    H5Composites::TypedWriter<H5CompositesStructures::Reality> m_writer;
};

#endif