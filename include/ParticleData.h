//Sets up output data types for the particles 
//Defines H5 structure to be used.
#ifndef PARTICLEDATA_HH
#define PARTICLEDATA_HH
#include "H5Struct.h"

namespace H5CompositesStructures {

    struct InitialParticleData {
        //Particle data on initially created particles

        /// The PDG numb
        int PDGnumb;
        /// The transverse momentum [MeV]
        double momentum;
        // Theta
        double theta;
        //Phi
        double phi;
        //x
        double PosX;
        //y
        double PosY;
        //z
        double PosZ;
        H5COMPOSITES_DECLARE_STRUCT_DTYPE()
    };

    struct DetectorOutput {
        //output data from the detectors
        int event_no;
        int PDGnumb;
        double PosX;
        double PosY;
        double PosZ;
        double time;
        int volume_ref;
        int volume_no;
        double momentum;
        
        H5COMPOSITES_DECLARE_STRUCT_DTYPE()
    };
    
    struct Reality {
        //reality of what happens in the simulation
        int event_no;
        int Track_ID;
        int PDGnumb;
        double PosX;
        double PosY;
        double PosZ;
        double time;
        double kinEnergy;

        H5COMPOSITES_DECLARE_STRUCT_DTYPE()
    };
}
#endif
