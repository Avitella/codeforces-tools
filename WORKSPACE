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

new_http_archive(
    name = "humanfriendly_archive",
    url = "https://pypi.python.org/packages/05/43/47c39f284391051c503322b86d2ffbe1e7314a3156cf5649aa7af03c85fb/humanfriendly-1.44.7.tar.gz",
    sha256 = "fcee758612edc6fead9b8fd1d5a473eab2c3a84cf8766f3ce70862ccd35e8a64"
    build_file = "bazel/humanfriendly.BUILD",
)

bind(
    name = "humanfriendly",
    actual = "@humanfriendly_archive//:humanfriendly",
)
