#ifndef H5OUTPUT_HH 
#define H5OUTPUT_HH
#include "ParticleData.h"
#include "../lib/H5Composites/include/H5Composites/GroupWrapper.h"
#include "../lib/H5Composites/include/H5Composites/TypedWriter.h"

class H5output{
    public:
    void DetectorOutput(int event_no, 
                        int PDGnumb,
                        double x,
                        double y,
                        double z,
                        double time,
                        int volume_ref,
                        int volume_no);/*{
        //H5CompositesStructures::DetectorOutput data;
                            };*/

    void InitialMuonOutput(int PDGnumb,
                            double momentum,
                            double theta,
                            double phi,
                            double x,
                            double y,
                            double z);/*{
        //H5CompositesStructures::InitialParticleData data;
                            };*/

    void RealityOutput(int event_no,
                        int PDGnumb,
                        int particleID,
                        double x,
                        double y,
                        double z,
                        double energy,
                        double time);/*{
        //H5CompositesStructures::Reality data;
                        };*/
};
#endif