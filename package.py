name = "tx_stickyController"

version = "0.1.6"

authors = [
    "José María Tejeda",
    "Jeremy Andriambolisoa",
]

description = \
    """
    Sticky Controller is a tool for Maya, specially designed for animators that need create extra controls over a rig that is in an animation shot in a simple way.
    """


requires = [
    "python-3+",
    "maya-2025"
]

uuid = "jmtejeda.stickyController"

build_command = 'python {root}/build.py {install}'

def commands():
    env.PYTHONPATH.append("{root}/python/")
    