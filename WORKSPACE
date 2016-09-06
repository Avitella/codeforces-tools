new_http_archive(
    name = "coloredlogs_archive",
    url = "https://pypi.python.org/packages/d2/55/309a63bb40192cc2e7f4da7c12eaf4ca461e5ff970c9c86378747d0996f3/coloredlogs-5.0.tar.gz",
    sha256 = "612354a11acd2e1d603c24fe7be21d736c53a23ad27f244cd9e3fdb4a99661d4",
    build_file = "bazel/coloredlogs.BUILD",
)

bind(
    name = "coloredlogs",
    actual = "@coloredlogs_archive//:coloredlogs",
)
