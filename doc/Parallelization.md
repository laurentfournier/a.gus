# **The subprocess option:**
_subprocess_ is **for running other executables** --- it's basically a wrapper around _os.fork()_ and _os.execve()_ with some support for optional plumbing (setting up PIPEs to and from the subprocesses. (Obviously other OS inter-process communications (IPC) mechanisms, such as sockets, SysV shared memory and message queues can be used --- but usually you're using subprocess to run third party binary executables and are going to be stuck with whatever interfaces and IPC channels those support).

Commonly one uses _subprocess_ synchronously --- simply calling some external utility and reading back its output or awaiting its completion (perhaps reading its results from a temporary file, or after its posted them to some database). However one can spawn hundreds of subprocesses and poll them. My own personal favorite utility does exactly that. The **biggest disadvantage** of the _subprocess_ module is that its I/O support is generally blocking. There is a draft [PEP-3145](https://www.python.org/dev/peps/pep-3145/) to fix that in some future version of Python 3.x and an alternative [asyncproc](http://www.lysator.liu.se/~bellman/download/asyncproc.py) (Warning that leads right to the download, not to any sort of documentation nor README). I've also found that it's relatively easy to just import _fcntl_ and manipulate your _Popen_ PIPE file descriptors directly --- though I don't know if this is portable to non-UNIX platforms.

_subprocess_ **has almost no event handling support ... though** you can use the _signal_ module and plain old-school UNIX/Linux signals --- killing your processes softly, as it were.

# **The multiprocessing option:**
_multiprocessing_ is **for running functions within your existing (Python) code** with support for more flexible communications among the family of processes. In particular it's best to build your _multiprocessing_ IPC around the module's _Queue_ objects where possible, but you can also use _Event_ objects and various other features (some of which are, presumably, built around _mmap_ support on platforms where that support is sufficient).

Python's _multiprocessing_ module is intended to provide interfaces and features which are very **similar to** _threading_ while allowing CPython to scale your processing among multiple CPUs/cores despite the GIL. It leverages all the fine-grained SMP locking and coherency effort that was done by developers of your OS kernel.

# **The threading option:**
_threading_ is **for a fairly narrow range of applications which are I/O bound** (don't need to scale across multiple CPU cores) and which benefit from the extremely low latency and switching overhead of thread switching (with shared core memory) vs. process/context switching. On Linux this is almost the empty set (Linux process switch times are extremely close to its thread-switches).

_threading_ suffers from **two major disadvantages in Python**. One, of course, is implementation specific --- mostly affecting CPython. That's the GIL (Global Interpreter Lock). For the most part, most CPython programs will not benefit from the availability of more than two CPUs (cores) and often performance will suffer from the GIL locking contention. The larger issue which is not implementation specific, is that threads share the same memory, signal handlers, file descriptors and certain other OS resources. Thus the programmer must be extremely careful about object locking, exception handling and other aspects of their code which are both subtle and which can kill, stall, or deadlock the entire process (suite of threads).

By comparison the _multiprocessing_ model gives each process its own memory, file descriptors, etc. A crash or unhandled exception in any one of them will only kill that resource and robustly handling the disappearance of a child or sibling process can be considerably easier than debugging, isolating and fixing or working around similar issues in threads.
* (Note: use of _threading_ with major Python systems, such as Numpy, may suffer considerably less from GIL contention then most of your own Python code would. That's because they've been specifically engineered to do so).

# **The twisted option:**
It's also worth noting that [Twisted](http://twistedmatrix.com/) offers yet another alternative which is both **elegant and very challenging to understand**. Basically, at the risk of over simplifying to the point where fans of Twisted may storm my home with pitchforks and torches, Twisted provides and event-driven co-operative multi-tasking within any (single) process.

To understand how this is possible one should read about the features of _select()_ (which can be built around the _select()_ or _poll()_ or similar OS system calls). Basically it's all driven by the ability to make a request of the OS to sleep pending any activity on a list of file descriptors or some timeout. The awakening from each of these calls to _select()_ is an event --- either one involving input available (readable) on some number of sockets or file descriptors, or buffering space becoming available on some other descriptors or sockets (writable), or some exceptional conditions (TCP out-of-band PUSH'd packets, for example), or a TIMEOUT.

Thus the **Twisted** programming model is built around handling these events then looping on the resulting "main" handler, allowing it to dispatch the events to your handlers.

I personally think of the name, Twisted as evocative of the programming model ... since your approach to the problem must be, in some sense, "twisted" inside out. Rather than conceiving of your program as a series of operations on input data and outputs or results, you're writing your program as a service or daemon and defining how it reacts to various events. (In fact the core "main loop" of a Twisted program is (usually? always?) a _reactor()_.

The **major challenges to using Twisted** involve twisting your mind around the event driven model and also eschewing the use of any class libraries or toolkits which are not written to co-operate within the Twisted framework. This is why Twisted supplies its own modules for SSH protocol handling, for curses, and its own subprocess/popen functions, and many other modules and protocol handlers which, at first blush, would seem to duplicate things in the Python standard libraries.

I think it's useful to understand Twisted on a conceptual level even if you never intend to use it. It may give insights into performance, contention, and event handling in your threading, multiprocessing and even subprocess handling as well as any distributed processing you undertake.

# **The distributed option:**
Yet another realm of processing you haven't asked about, but which is worth considering, is that of _**distributed**_ processing. There are many Python tools and frameworks for distributed processing and parallel computation. Personally I think the easiest to use is one which is least often considered to be in that space.

It is almost trivial to build distributed processing around [Redis](http://redis.io/). The entire key store can be used to store work units and results, Redis LISTs can be used as _Queue()_ like object, and the PUB/SUB support can be used for _Event_-like handling. You can hash your keys and use values, replicated across a loose cluster of Redis instances, to store the topology and hash-token mappings to provide consistent hashing and fail-over for scaling beyond the capacity of any single instance for co-ordinating your workers and marshaling data (pickled, JSON, BSON, or YAML) among them.

Of course as you start to build a larger scale and more sophisticated solution around Redis you are re-implementing many of the features that have already been solved using Hadoop, Zookeeper, Cassandra and so on. Those also have modules for Python access to their services.

# **Conclusion**
There you have the gamut of processing alternatives for Python, from single threaded, with simple synchronous calls to sub-processes, pools of polled subprocesses, threaded and multiprocessing, event-driven co-operative multi-tasking, and out to distributed processing.