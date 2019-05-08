---
title: "AGC033 A問題 参加記録"
date: 2019-05-05T12:19:01+09:00
archives: ["2019/05"]
tags: [競技プログラミング, AtCoder]
---

昨日（2019/05/04）、AtCoderで開催された[AtCoder Grand Contest 033](https://atcoder.jp/contests/agc033)に参加しました。
A問題の復習記事です。
<!--more-->
```
2019/5/4 AtCoder Grand Contest 033
Rank: 565(rated)
Perf: 1705
Rating: 1275(+61, highest!)
```

![レート](/blog/img/AtCoder20190504.png)

結果はA~Fの6問中、A(300), B(600)のみACでした。

問題量が多いため、各問題ごと別に記事を書こうと思います。

---
> ### A - Darker and Darker
>
> ##### 問題文
>
> 縦$H$行、横$W$列の白黒に塗られたマス目が与えられます。
>
> マス目の状態は$A_{11}$から$A\_{HW}$の$HW$個の文字で表されており、  \
> 上から$i$行目、左から$j$列目にあるマスが黒色のとき、$A\_{ij}$は`#`、  \
> 上から$i$行目、左から$j$列目にあるマスが白色のとき、$A\_{ij}$は`.`となっています。  \
>
> すべてのマスが黒色になるまで、以下の操作を繰り返し行います。
>
> - 辺を共有して隣接するマスの中に、黒色のマスが一つ以上存在するような白色のマスすべてが黒色になる。
>
> 何回の操作を行うことになるか求めてください。
>
> ただし、最初に与えられるマス目には少なくとも1つ黒色のマスが存在します。
>
>
> ##### 制約
> - $1 ≦ H,W ≦ 1000$
> - $A\_{ij}$は`#`または`.`。
> - 与えられるマス目には少なくとも1つ黒色のマスが存在する。
>
> <cite>[A - Darker and Darker](https://atcoder.jp/contests/agc033/tasks/agc033_a)</cite>

この問題はシミュレーションが簡単そうですが、気をつけないと実行時間制限に引っかかりそうです。

毎操作ごとにすべてのマスをチェックし、色を更新するというのが、シンプルな再現方法です。

この場合、最悪のパターンは、$H=W=1000$、$A_{11}$のみが黒い場合です。
このとき処理のループ数は、$H*W*2000 \simeq 10^9$となり、1秒間では処理しきれません。
（たいてい、ループ数$10^7$までなら1秒で処理可能と言われています。）

少し考えると、毎度の操作でチェックするマスを減らせることがわかります。
具体的には、**前回の操作で新しく黒になったマスの周囲のみ**チェックすればよいです。

こうすることで、すべてのマスに対し、その周囲のチェックが1度ずつ走ることになります。
ですのでチェックの数は高々$4HW$、つまり$O(HW)$に収まります。
これは1秒以内で十分処理できる計算量です。


{{< prettify lang-cpp >}}
#include &ltalgorithm>
#include &ltcmath>
#include &ltiostream>
#include &ltqueue>
#include &ltstring>
#include &lttuple>
#include &ltvector>

using namespace std;
typedef long long int ll;
typedef vector&ltint> vi;
typedef vector&ltvi> vvi;
typedef pair&ltint, int> v2;

#define INF (1e9)

int H, W;

int main() {
    cin >> H >> W;

    vvi A(H, vi(W, INF));
    string s;
    queue<v2> q;

    for (int i = 0; i < H; i++) {
        cin >> s;
        for (int j = 0; j < W; j++) {
            if (s[j] == '#') {
                A[i][j] = 0;
                q.push(v2(i, j));
            }
        }
    }

    while (!q.empty()) {
        v2 p = q.front();
        q.pop();
        int xx = p.second;
        int yy = p.first;
        if (xx > 0 && A[yy][xx - 1] == INF) {  // L
            A[yy][xx - 1] = A[yy][xx] + 1;
            q.push(v2(yy, xx - 1));
        }
        if (xx < W - 1 && A[yy][xx + 1] == INF) {  // R
            A[yy][xx + 1] = A[yy][xx] + 1;
            q.push(v2(yy, xx + 1));
        }
        if (yy > 0 && A[yy - 1][xx] == INF) {  // U
            A[yy - 1][xx] = A[yy][xx] + 1;
            q.push(v2(yy - 1, xx));
        }
        if (yy < H - 1 && A[yy + 1][xx] == INF) {  // D
            A[yy + 1][xx] = A[yy][xx] + 1;
            q.push(v2(yy + 1, xx));
        }
    }

    int ans = 0;
    for (int i = 0; i < H; i++) {
        for (int j = 0; j < W; j++) {
            ans = max(ans, A[i][j]);
        }
    }

    cout << ans << endl;
    return 0;
}

{{< /prettify >}}
