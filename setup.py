from setuptools import setup

# Metadata goes in setup.cfg. These are here for GitHub's dependency graph.
setup(
    name="statesman-discord",
    install_requires=[
        "pyyaml",
        "sentry-sdk==1.13.0",
        "python-dotenv",
        "jsonschema",
        "redis",
    ],
    extras_require={},
)
