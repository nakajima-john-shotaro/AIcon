# PyTorch_Docker

## 🀇🀏🀐🀘🀙🀡🀀🀁🀂🀃🀆🀅🀄🀄

## セットアップ

### 1. 新たにターミナルを立ち上げて次のコマンドでこのリポジトリをクローン（ダウンロード）してください
```sh
git clone http://git-docker.tasakilab:5050/git/urasaki/PyTorch_Docker.git
```

### 2. 次のコマンドでDockerイメージをビルドしてください（時間がかかります）
```sh
./PyTorch_Docker/docker/build-docker.sh
```

|オプション |パラメータ |説明                      |既定値   |
|-----------|:---------:|--------------------------|:-------:|
|`-h`       |なし       |ヘルプを表示              |なし     |
|`-p`       |VERSION    |PyTorchのバージョン       |1.7.1    |
|`-c`       |VERSION    |CUDAのバージョン          |11.0     |
|`-d`       |VERSION    |cuDNNのバージョン         |8        |
|`-f`       |FLAVOR     |PyTorchのフレーバー       |devel    |

### 3. ビルドに成功したら次のコマンドでDockerコンテナを起動することができます
```sh
./PyTorch_Docker/docker/run-docker.sh
```
**エラーが出た場合はイメージを削除しPyTorchのバージョンを下げてもう一度 2. を実行してみてください**

### 4. 次のコマンドで別のターミナルから起動中のコンテナに入ることができます
```sh
./PyTorch_Docker/docker/exec-docker.sh
```
