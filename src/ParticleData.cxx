#include "ParticleData.h"

namespace H5CompositesStructures {
    H5COMPOSITES_DEFINE_STRUCT_DTYPE(InitialParticleData, PDGnumb, momentum, theta, phi, PosX, PosY, PosZ)
    H5COMPOSITES_DEFINE_STRUCT_DTYPE(DetectorOutput, event_no, PDGnumb, PosX, PosY, PosZ, time, volume_ref, volume_no)
    H5COMPOSITES_DEFINE_STRUCT_DTYPE(Reality, Track_ID, event_no, PDGnumb, PosX, PosY, PosZ, time, kinEnergy)

}