## 问题分析
部署报错的原因是在 `layouts/partials/head.html` 文件的第46行使用了错误的Hugo模板函数 `css.Sass`，而Hugo中没有这个内置函数。

## 修复方案
将第46行的 `css.Sass` 替换为Hugo标准的CSS处理函数 `toCSS`，与同一文件中第27行的正确用法保持一致。

## 修复步骤
1. 编辑 `c:\Users\tonyz\Documents\hugo-blog\layouts\partials\head.html` 文件
2. 将第46行的 `{{ $processedStyle := $style | css.Sass | resources.Minify | resources.Fingerprint }}` 替换为 `{{ $processedStyle := $style | toCSS | minify | fingerprint }}`
3. 保存文件并重新部署

## 预期结果
修复后，Hugo将能够正确解析模板，部署过程不会再出现函数未定义的错误。