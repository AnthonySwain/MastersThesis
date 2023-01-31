#ifndef HIT_HH
#define HIT_HH

#include "G4VHit.hh"
#include "G4Allocator.hh"
#include "G4THitsCollection.hh"
#include "G4ThreeVector.hh"

class DetectorHit : public G4VHit //base class
{
    public:
        DetectorHit();
        DetectorHit(const DetectorHit&) = default;
        ~DetectorHit();

        //void Print(); //Print hit interface on screen


        //get methods
        //G4double GetEdep() const;
        //G4double GetTrackLength() const;

    private:
    
        //G4double fEdep = 0.; //Energy deposit in the sensitive volume
        //G4double fTrackLength = 0.; //Track length in the sensitive volume
};

typedef G4THitsCollection<DetectorHit> DetectorHitCollection;

#endif