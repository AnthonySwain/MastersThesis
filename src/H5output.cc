#include "H5output.hh"

void H5output::DetectorOutput(int event_no, 
                        int PDGnumb,
                        double x,
                        double y,
                        double z,
                        double time,
                        int volume_ref,
                        int volume_no){}
    


void H5output::InitialMuonOutput(int PDGnumb,
                            double momentum,
                            double theta,
                            double phi,
                            double x,
                            double y,
                            double z){
                                
    //Defining and making the data structure
    using namespace H5CompositesStructures;
    InitialParticleData data;

    data = InitialParticleData{
    .PDGnumb = PDGnumb,
    .momentum = momentum,
    .theta = theta,
    .phi = phi,
    .PosX = x,
    .PosY = y,
    .PosZ = z};

    //Create the output file, Allow over-writing
    using namespace H5Composites;
    GroupWrapper fOut = GroupWrapper::createFile("Output.h5", true);
    auto initialWriter = fOut.makeDataSetWriter<InitialParticleData>("InitialMuon");
    initialWriter.setIndex("PDGnumb");
    initialWriter.write(data);
    }

    /*
    Open this in initial sim.cc file 
    create group wrapper, create file,
    In user actions take this file as argument and make writers within write call to do this
    */
void H5output::RealityOutput(int event_no,
                        int PDGnumb,
                        int particleID,
                        double x,
                        double y,
                        double z,
                        double energy,
                        double time){

                        }