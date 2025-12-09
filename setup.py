from setuptools import setup, find_packages

setup(
    name="vlm-probe",
    version="0.4.0",
    description="Probing fine-grained perception in vision-language models.",
    author="Xu Mingrui",
    license="MIT",
    packages=find_packages(exclude=["tests*", "scripts*"]),
    python_requires=">=3.10",
    install_requires=[
        "torch>=2.1",
        "transformers>=4.40",
        "accelerate>=0.25",
        "pillow>=10.0",
        "pyyaml>=6.0",
        "tqdm",
    ],
)
