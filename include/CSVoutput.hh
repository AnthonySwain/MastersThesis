//File is now redundant now H5 is setup.
#ifndef CSVOUTPUT_HH 
#define CSVOUTPUT_HH

#include <fstream>

class CSVoutput{
    public:
    void DetectorOutput(int event_no, 
                        int PDGnumb,
                        double x,
                        double y,
                        double z,
                        double time,
                        int volume_ref,
                        int volume_no);

    void InitialMuonOutput(int PDGnumb,
                            double momentum,
                            double theta,
                            double phi,
                            double x,
                            double y,
                            double z);

    void RealityOutput(int event_no,
                        int PDGnumb,
                        int particleID,
                        double x,
                        double y,
                        double z,
                        double energy,
                        double time);
};

#endif