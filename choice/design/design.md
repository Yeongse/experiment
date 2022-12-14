# 対象とする意思決定問題
- 提示される2人の野球選手(野手)のうち, 今シーズンの優勝を目指すならば, どちらと契約したいかという問題を対象とする. 　
- 過去の選択は全く影響を与えず, 純粋に2人の選手だけをみて決めてもらう. 

# 目的
- 属性数の増えすぎに対して, どう選択行動が変化するのか, その現象を確定させる. (効用の差が小さくなっていくのか?, 一貫性がなくなるのか?)
- 研究の最終的な落とし所を検討する(情報の絞り込み支援が良いのではないか？どういう属性を絞るのが良いかについて議論をしたい). 

# 実施する環境
- 属性の数を4, 6, 8, 10の4通りで実施する. 
- 各属性は「打率」, 「本塁打」, 「盗塁数」, 「守備力」, 「打点」, 「四球数」, 「得点圏打率」, 「併殺打数」, 「年間平均離脱数」, 「年齢」の10個を用いる. 
- 各属性は数十程度の水準からランダムで抽出, 各属性については実験前に説明する. 
- AHP法でよく使われる尺度評価のように, 二つの選択肢AとBについて, 
「A(B)の方が極めて優れている(9点)」, 
「A(B)の方が非常に優れている(7点)」, 
「A(B)の方がかなり優れている(5点)」, 
「A(B)の方がやや優れている(3点)」, 
「AとBは同等に優れている(1点)」
の9段階の尺度評価を行わせる. 
- プロファイルは各属性数ごとに6個ずつ抽出し, 15通りの比較を行わせる. 
- 時間制限を設けない. 
- ある属性数に対する選択が終了すると, 5分間の休憩をさせる. 
- 実験終了後にアンケートを実施する. 

# アンケートの内容
- 属性ごとの45通りの一対比較(モデル化のために)
- 各属性数ごとに無視した属性があるか(何か), 設問ごとに変化した場合, それも出す. 
- なんでそれを無視したのか, 自由記述で聞く. 

# 分析手法
- ロジットモデルによるパラメータの推定とエントロピー指標の計算
- 選択結果からの整合比C.R.の計算
- 点数と選択確率の差の相関分析
- 属性数と点数の相関分析

# 観察したい現象
- 全被験者の平均として, 属性数に対してエントロピー指標がU字型になる
- 点数と選択確率の差に正の相関がある
- 属性数が増えすぎると点数が小さくなる or 他の設問から推定される結果と違う回答をすることが増える(整合比が大きくなる)
- 他の属性と類似度が高い属性を無視する or 無視することで選択が簡単になる属性を無視する