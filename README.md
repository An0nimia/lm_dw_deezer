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
		pip install lm-dw-deezer[RUSTDW]
		```

# Usage
```bash
lm_dw_deezer --help
```


# Inside a docker container
1. Run in a container
	```bash
	docker run -it -v "$(pwd):/Songs" an0nimia/lm_dw_deezer:latest bash
	```
