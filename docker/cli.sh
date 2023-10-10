TAG="scaleu_cli"
FILENAME="cli.dockerfile"

# Build
docker build -t $TAG -f $FILENAME .

# Get pwd of one directory up
PWD=$(cd ..; pwd)

# Run with bind mount to get access to the local files
docker run --mount type=bind,source=$PWD,target=/app -p 3000:3000 -w /app -it $TAG
