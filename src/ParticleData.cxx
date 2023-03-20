#include "ParticleData.h"

namespace H5CompositesStructures {
    H5COMPOSITES_DEFINE_STRUCT_DTYPE(InitialParticleData, PDGnumb, momentum, theta, phi, PosX, PosY, PosZ)
    H5COMPOSITES_DEFINE_STRUCT_DTYPE(DetectorOutput, event_no, PDGnumb, PosX, PosY, PosZ, time, volume_ref, volume_no, momentum)
    H5COMPOSITES_DEFINE_STRUCT_DTYPE(Reality, event_no, Track_ID, PDGnumb, PosX, PosY, PosZ, time, kinEnergy)

}