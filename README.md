# sam
tools for [SAM](https://github.com/facebookresearch/segment-anything)

## Download checkpoints
follow https://github.com/facebookresearch/segment-anything, download file and place in ./weights

## Build docker image
```
docker build --progress plain --network=host -f Dockerfile -t sam:test .
```


