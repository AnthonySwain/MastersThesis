#Setup the project
cmake_minimum_required(VERSION 3.16...3.21)
project(Simulation)

#Find Geant4 package, activating all available UI and Vis drivers by default
find_package(Geant4 REQUIRED ui_all vis_all)

# Setup Geant4 include directories and compile definitions
# Setup include directory for this project
include (${Geant4_USE_FILE})
include_directories(${PROJECT_SOURCE_DIR}/include)
include_directories(${PROJECT_SOURCE_DIR}/src)
include_directories(${PROJECT_SOURCE_DIR}/lib/H5Composites)
include_directories(${PROJECT_SOURCE_DIR}/lib/H5Composites/include/H5Composites)

include_directories(${PROJECT_SOURCE_DIR}/lib/EcoMug-1.3.1)


add_subdirectory(lib/H5Composites)

# Locate sources, headers and macros for this project
file(GLOB sources ${PROJECT_SOURCE_DIR}/src/*.cc)
file(GLOB headers ${PROJECT_SOURCE_DIR}/include/*.hh)
file(GLOB MACRO_FILES  ${PROJECT_SOURCE_DIR}/*.mac)
file(COPY ${MACRO_FILES} DESTINATION ${PROJECT_BINARY_DIR})

#Library of data structures to save in H5
add_library(H5CompositesStructures)
target_sources(H5CompositesStructures
    PRIVATE
    src/ParticleData.cxx
)

target_link_libraries(H5CompositesStructures
    PUBLIC
    H5Composites)

# Add the executable, and link it to the Geant4 libraries, H5Composites and H5CompositesStructures
add_executable(sim sim.cc ${sources} ${headers})
target_link_libraries(sim 
    ${Geant4_LIBRARIES} 
    H5Composites
    H5CompositesStructures)

add_custom_target(Simulation DEPENDS sim)



