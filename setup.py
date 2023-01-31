from setuptools import setup

# Metadata goes in setup.cfg. These are here for GitHub's dependency graph.
setup(
    name="statesman-discord",
    install_requires=[
        "discord.py",
        "flask<3.0",
        "flask-dotenv",
        "flask-executor",
        "flask-inputs",
        "flask-limiter[redis]",
        "flask-redis",
        "flask-script",
        "flask-session",
        "jsonschema",
        "kubernetes",
        "pika",
        "pynacl",
        "python-dotenv",
        "pyyaml",
        "redis",
        "requests",
        "sentry-sdk[flask]",
        "uwsgi",
    ],
    extras_require={},
)
