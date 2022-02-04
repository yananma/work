
如果环境报错 ImportError: /lib64/libstdc++.so.6: version `GLIBCXX_3.4.20' not found，就把 python 环境从 3.9 改为 3.7   


安装 GPU 版本的报错  

```python 
(mxcv) [crisis@b64 ~]$ python 
Python 3.7.12 | packaged by conda-forge | (default, Oct 26 2021, 06:08:21) 
[GCC 9.4.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import paddle
>>> paddle.utils.run_check()
Running verify PaddlePaddle program ... 
W0204 18:47:14.452605 269770 device_context.cc:447] Please NOTE: device: 0, GPU Compute Capability: 7.5, Driver API Version: 11.4, Runtime API Version: 10.2
W0204 18:47:14.459616 269770 device_context.cc:465] device: 0, cuDNN Version: 8.3.
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/home/crisis/miniconda3/envs/mxcv/lib/python3.7/site-packages/paddle/utils/install_check.py", line 196, in run_check
    _run_static_single(use_cuda)
  File "/home/crisis/miniconda3/envs/mxcv/lib/python3.7/site-packages/paddle/utils/install_check.py", line 124, in _run_static_single
    exe.run(startup_prog)
  File "/home/crisis/miniconda3/envs/mxcv/lib/python3.7/site-packages/paddle/fluid/executor.py", line 1262, in run
    six.reraise(*sys.exc_info())
  File "/home/crisis/miniconda3/envs/mxcv/lib/python3.7/site-packages/six.py", line 719, in reraise
    raise value
  File "/home/crisis/miniconda3/envs/mxcv/lib/python3.7/site-packages/paddle/fluid/executor.py", line 1260, in run
    return_merged=return_merged)
  File "/home/crisis/miniconda3/envs/mxcv/lib/python3.7/site-packages/paddle/fluid/executor.py", line 1402, in _run_impl
    use_program_cache=use_program_cache)
  File "/home/crisis/miniconda3/envs/mxcv/lib/python3.7/site-packages/paddle/fluid/executor.py", line 1492, in _run_program
    [fetch_var_name])
RuntimeError: (PreconditionNotMet) The third-party dynamic library (libcublas.so) that Paddle depends on is not configured correctly. (error code is libcublas.so: cannot open shared object file: No such file or directory)
  Suggestions:
  1. Check if the third-party dynamic library (e.g. CUDA, CUDNN) is installed correctly and its version is matched with paddlepaddle you installed.
  2. Configure third-party dynamic library environment variables as follows:
  - Linux: set LD_LIBRARY_PATH by `export LD_LIBRARY_PATH=...`
  - Windows: set PATH by `set PATH=XXX; (at /paddle/paddle/fluid/platform/dynload/dynamic_loader.cc:285)
```
