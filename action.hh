#ifndef ACTION_HH
#define ACTION_HH

#include "G4VUserActionInitialization.hh"
#include "generator.hh"
#include "stepping.hh"

class MyActionInitialization : public G4VUserActionInitialization
{
public:
    MyActionInitialization();
    ~MyActionInitialization();

    //runs the particle gun and computes the stepping ect...
    virtual void BuildForMaster() const;
    virtual void Build() const;
};

#endif