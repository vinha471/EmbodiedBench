#!/bin/bash
if [ ! -e /proc/driver/nvidia/version ]; then
    echo "Error: Nvidia driver not found at /proc/driver/nvidia/version; Please ensure you have an Nvidia GPU device and appropriate drivers are installed."
    exit 1;
fi;

if  ! type "docker" 2> /dev/null > /dev/null ; then
    echo "Error: docker not found. Please install docker to complete the build. "
    exit 1
fi;

NVIDIA_VERSION=$(grep -oE '[0-9]{3}\.[0-9]{3}\.[0-9]{2}' /proc/driver/nvidia/version | head -n 1)

# Compare dot versions (e.g. 570.124.06 >= 550.00.00).
version_ge() {
    [ "$(printf '%s\n%s\n' "$1" "$2" | sort -V | head -n 1)" = "$2" ]
}

# Updated CUDA/driver thresholds for CUDA 12.x series.
if version_ge "$NVIDIA_VERSION" "570.00.00"; then
    CUDA_VERSION=12.8.1
elif version_ge "$NVIDIA_VERSION" "560.00.00"; then
    CUDA_VERSION=12.6.3
elif version_ge "$NVIDIA_VERSION" "550.00.00"; then
    CUDA_VERSION=12.4.1
elif version_ge "$NVIDIA_VERSION" "535.00.00"; then
    CUDA_VERSION=12.2.2
elif version_ge "$NVIDIA_VERSION" "525.00.00"; then
    CUDA_VERSION=12.0.1
else
    echo "No valid CUDA version found for nvidia driver $NVIDIA_VERSION"
    exit 1
fi

echo $NVIDIA_VERSION
echo $CUDA_VERSION

if (id -nG | grep -qw "docker") || [ "$USER" == "root" ]; then
    echo "Building Docker container with CUDA Version: $CUDA_VERSION"
    docker build  --build-arg CUDA_VERSION=$CUDA_VERSION  -t embodiedbench:latest .
else
    echo "Error: Unable to run build.sh. Please use sudo to run build.sh or add $USER to the docker group."
    exit 1
fi
