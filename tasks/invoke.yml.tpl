buildcfg:
  bazelArgs:
  env:
    TF_CPP_MIN_VLOG_LEVEL: 3
    TF_CPP_MIN_LOG_LEVEL:
    CUDA_VISIBLE_DEVICES:

    PYTHON_BIN_PATH: ${PYTHON_BIN_PATH}
    USE_DEFAULT_PYTHON_LIB_PATH: 1

    CC_OPT_FLAGS: -march=native

    ZEROMQ_PATH: ${ZEROMQ_PATH}

    TF_NEED_JEMALLOC: 1
    TF_NEED_GCP: 0
    TF_NEED_HDFS: 0
    TF_NEED_S3: 0
    TF_NEED_GDR: 0
    TF_ENABLE_XLA: 0
    TF_NEED_OPENCL_SYCL: 0
    TF_NEED_MPI: 0
    TF_NEED_VERBS: 0
    TF_NEED_RPC: 1

    TF_NEED_CUDA: 1
    TF_CUDA_VERSION: 9.1
    CUDA_TOOLKIT_PATH: /opt/cuda
    TF_CUDNN_VERSION: 7
    CUDNN_INSTALL_PATH: /opt/cuda
    TF_CUDA_COMPUTE_CAPABILITIES: 6.1
    TF_CUDA_CLANG: 0
    GCC_HOST_COMPILER_PATH: /usr/bin/gcc-6

    TF_SET_ANDROID_WORKSPACE:
