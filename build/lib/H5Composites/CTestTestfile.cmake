# CMake generated Testfile for 
# Source directory: /home/anthony/MastersThesis/lib/H5Composites
# Build directory: /home/anthony/MastersThesis/build/lib/H5Composites
# 
# This file includes the relevant testing commands required for 
# testing this directory and lists subdirectories to be tested as well.
add_test(dtypes "test_dtypes")
set_tests_properties(dtypes PROPERTIES  _BACKTRACE_TRIPLES "/home/anthony/MastersThesis/lib/H5Composites/CMakeLists.txt;56;add_test;/home/anthony/MastersThesis/lib/H5Composites/CMakeLists.txt;59;define_utest;/home/anthony/MastersThesis/lib/H5Composites/CMakeLists.txt;0;")
add_test(readwrite_primitives "test_readwrite_primitives")
set_tests_properties(readwrite_primitives PROPERTIES  _BACKTRACE_TRIPLES "/home/anthony/MastersThesis/lib/H5Composites/CMakeLists.txt;56;add_test;/home/anthony/MastersThesis/lib/H5Composites/CMakeLists.txt;60;define_utest;/home/anthony/MastersThesis/lib/H5Composites/CMakeLists.txt;0;")
add_test(array "test_array")
set_tests_properties(array PROPERTIES  _BACKTRACE_TRIPLES "/home/anthony/MastersThesis/lib/H5Composites/CMakeLists.txt;56;add_test;/home/anthony/MastersThesis/lib/H5Composites/CMakeLists.txt;61;define_utest;/home/anthony/MastersThesis/lib/H5Composites/CMakeLists.txt;0;")
add_test(tuple "test_tuple")
set_tests_properties(tuple PROPERTIES  _BACKTRACE_TRIPLES "/home/anthony/MastersThesis/lib/H5Composites/CMakeLists.txt;56;add_test;/home/anthony/MastersThesis/lib/H5Composites/CMakeLists.txt;62;define_utest;/home/anthony/MastersThesis/lib/H5Composites/CMakeLists.txt;0;")
