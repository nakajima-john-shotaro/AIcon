# AIcon / frontend

[初めてのハッカソン~オンライン開発合宿vol.2~](https://talent.supporterz.jp/events/4dd93ba8-1fde-477a-8706-2d17f46c1c4d/)」で使用したプログラムのリポジトリです



## Overview

入力した文章からそれに合うようなアイコン用の画像をDeep Learningを使って生成するシステム

画像生成には[Deep Daze](https://github.com/lucidrains/deep-daze)を使用しています



## やることリスト

### フロントエンド

- [x] 入力文章の翻訳
- [x] バックエンドとの通信
- [x] 見た目を整える
- [] 細かなバグの修正
- ~~[] クラウドからの画像取得~~



### バックエンド

- ~~[ ] DALL-Eの学習~~
- ~~[ ] DALL-Eの検証~~
- [x] Big Sleepの動作確認
- [x] Deep Dazeの動作確認
- ~~[ ] クラウドへの画像保存~~
- [x] フロントエンドとの通信



## したいことリスト

### フロントエンド

- TwitterとかのAPIを使ってアイコンの変更



### バックエンド

- 



## Citations
```bibtex
@misc{unpublished2021clip,
    title  = {CLIP: Connecting Text and Images},
    author = {Alec Radford, Ilya Sutskever, Jong Wook Kim, Gretchen Krueger, Sandhini Agarwal},
    year   = {2021}
}
```

```bibtex
@misc{brock2019large,
    title   = {Large Scale GAN Training for High Fidelity Natural Image Synthesis}, 
    author  = {Andrew Brock and Jeff Donahue and Karen Simonyan},
    year    = {2019},
    eprint  = {1809.11096},
    archivePrefix = {arXiv},
    primaryClass = {cs.LG}
}
```

```bibtex
@misc{sitzmann2020implicit,
    title   = {Implicit Neural Representations with Periodic Activation Functions},
    author  = {Vincent Sitzmann and Julien N. P. Martel and Alexander W. Bergman and David B. Lindell and Gordon Wetzstein},
    year    = {2020},
    eprint  = {2006.09661},
    archivePrefix = {arXiv},
    primaryClass = {cs.CV}
}
```

```bibtex
@misc{ramesh2021zeroshot,
    title   = {Zero-Shot Text-to-Image Generation}, 
    author  = {Aditya Ramesh and Mikhail Pavlov and Gabriel Goh and Scott Gray and Chelsea Voss and Alec Radford and Mark Chen and Ilya Sutskever},
    year    = {2021},
    eprint  = {2102.12092},
    archivePrefix = {arXiv},
    primaryClass = {cs.CV}
}
```


```bibtex
@misc{kitaev2020reformer,
    title   = {Reformer: The Efficient Transformer},
    author  = {Nikita Kitaev and Łukasz Kaiser and Anselm Levskaya},
    year    = {2020},
    eprint  = {2001.04451},
    archivePrefix = {arXiv},
    primaryClass = {cs.LG}
}
```

```bibtex
@misc{esser2021taming,
    title   = {Taming Transformers for High-Resolution Image Synthesis},
    author  = {Patrick Esser and Robin Rombach and Björn Ommer},
    year    = {2021},
    eprint  = {2012.09841},
    archivePrefix = {arXiv},
    primaryClass = {cs.CV}
}
```



## DALL-E・Big Sleep・Deep Dazeの使用方法 (デバッグ用)

1. [PyTorch_Docker](http://git-docker.tasakilab:5050/urasaki/PyTorch_Docker)で環境を構築

2. PyTorch_Dockerのshared_dirへ移動

3. このリポジトリをクローン

   ```bash
   git clone http://git-docker.tasakilab:5050/git/Hackathon_202104/GeneCon.git
   ```

4. 実装中