package(default_visibility = ["//visibility:public"])

py_library(
    name = "coloredlogs",
    srcs = [
        "coloredlogs-5.0/coloredlogs/__init__.py",
        "coloredlogs-5.0/coloredlogs/cli.py",
        "coloredlogs-5.0/coloredlogs/converter.py",
        "coloredlogs-5.0/coloredlogs/demo.py",
        "coloredlogs-5.0/coloredlogs/syslog.py",
        "coloredlogs-5.0/coloredlogs/tests.py",
    ],
    imports = [
        "coloredlogs-5.0",
    ],
	deps = [
		"//external:humanfriendly",
	],
    # srcs_version = "PY3",
)
