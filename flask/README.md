# SAMPLE FLASK APP

A Flask app is not meant to be run from the current directory but rather from the project directory (the directory above it).
This directory partly exists simply because text/code editors sometimes don't play nice over SSH, and it is nice to keep track over GitHub anyways.

`cd $PROJECT_HOME`

`rm -rf __pycache__/`
`rm -rf plaintiff`
`rm -rf defendant`
`rm -rf util`
`rm -rf auth`
`rm main.py`

`mv legal/plaintiff/ .`
`mv legal/defendant/ .`
`mv legal/util/ .`
`mv legal/auth .`
`mv legal/flask/main.py .`
