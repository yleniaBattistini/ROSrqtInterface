execute_process(COMMAND "/home/ylenia/catkin_ws/build/rqt_mypkg/catkin_generated/python_distutils_install.sh" RESULT_VARIABLE res)

if(NOT res EQUAL 0)
  message(FATAL_ERROR "execute_process(/home/ylenia/catkin_ws/build/rqt_mypkg/catkin_generated/python_distutils_install.sh) returned error code ")
endif()
