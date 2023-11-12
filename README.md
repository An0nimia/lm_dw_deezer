# LM DW Deezer

# Install
1. Only C backend
	```bash
	pip install lm-dw-deezer
	```
1. W Rust backend
	> [!NOTE]
	> If you have already installed RUST you can jump this step
	```bash
	curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
	```
	- Install
		```bash
		pip install lm-dw-deezer[RUST]
		```

# Usage
```bash
lm_deezer_dw --help
```


# Inside a docker container
1. Run in a container
	```bash
	docker run -it --rm -v "$(pwd):/Songs" python:3.12 bash
	```
