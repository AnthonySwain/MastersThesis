#include "CSVoutput.hh"

void CSVoutput::DetectorOutput(int event_no, 
                        int PDGnumb,
                        double x,
                        double y,
                        double z,
                        double time,
                        int volume_ref,
                        int volume_no){

    std::ofstream myFile("../data/DetectorHits.csv",std::ios::app); //open file //append to file
    myFile << event_no << "," 
    << PDGnumb << ","
    << x << ","
    << y << ","
    << z << ","
    << time << "," 
    << volume_ref << "," 
    << volume_no 
    << "\n";
    myFile.close();

};

void CSVoutput::InitialMuonOutput(int PDGnumb,
                            double momentum,
                            double theta,
                            double phi,
                            double x,
                            double y,
                            double z){
    
    std::ofstream myFile2("../data/Initial_Muon_Dist.csv",std::ios::app); //open file //append to file
    myFile2 << PDGnumb << ","
    << x << ","
    << y << ","
    << z << ","
    << momentum << ","
    << theta << ","
    << phi
    << "\n";
    myFile2.close();
}

void CSVoutput::RealityOutput(int event_no,
                        int PDGnumb,
                        int particleID,
                        double x,
                        double y,
                        double z,
                        double energy,
                        double time){
    std::ofstream myFile("../data/Reality.csv",std::ios::app); //open file //append to file
    myFile << event_no << ","
    << PDGnumb << ","
    << particleID <<"," 
    << x <<"," 
    << y <<"," 
    << z <<"," 
    << energy<<"," 
    <<time
    << "\n";
    myFile.close();

    }