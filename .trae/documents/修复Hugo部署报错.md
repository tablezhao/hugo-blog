## 问题分析

### 当前实现
1. 首页模板 `home.html` 调用 `home/profile.html` 组件
2. `profile.html` 调用 `home/featured.html` 组件显示精选文章
3. `featured.html` 直接遍历所有 `featured: true` 的文章，没有分页

### 分页需求
- 精选文章列表需要支持分页
- 每页显示10篇文章
- 使用与博客列表页相同的分页样式

## 修复方案

### 实现步骤
1. 修改 `home.html` 模板，添加分页逻辑
2. 修改 `home/profile.html` 组件，接受分页数据
3. 修改 `home/featured.html` 组件，使用分页数据

### 具体修改

#### 1. 修改 home.html
```html
{{ define "content" }}
  {{ $featured := where .Site.RegularPages "Params.featured" true }}
  {{ $paginator := .Paginate $featured 10 }}
  {{ partial "home/profile.html" (dict "paginator" $paginator "featured" $featured "Page" .) }}
{{ end }}
```

#### 2. 修改 home/profile.html
```html
<div class="home">
    <!-- 原有个人信息部分保持不变 -->
    <div class="info">
        <!-- ... 原有代码 ... -->
    </div>

    <div class="featured">
        {{ partial "home/featured.html" . }}
    </div>
</div>
```

#### 3. 修改 home/featured.html
```html
{{ $paginator := .paginator }}
{{ if gt $paginator.TotalPages 0 }}
  <h2>{{- i18n "featured_posts" -}}</h2>
{{ end }}
<div class="featured-list">
  {{ range $paginator.Pages }}
    <article class="featured-single">
        <h4><a href="{{ .RelPermalink }}">{{ .Params.title }}</a></h4>
        {{ partial "blog/meta.html" . }}
        {{ .Summary }}
    </article>
  {{ end -}}
</div>
{{ if gt $paginator.TotalPages 1 }}
<div class="paginator">
  {{ if $paginator.HasPrev }}
  <a class="prev" href="{{ $paginator.Prev.URL }}">&larr;&nbsp;&nbsp;Pre Page</a>
  {{ end }}
  {{ if $paginator.HasNext }}
  <a class="next" href="{{ $paginator.Next.URL }}">Next Page&nbsp;&nbsp;&rarr;</a>
  {{ end }}
</div>
{{ end }}
```

## 预期结果

- 首页精选文章列表将支持分页
- 每页显示10篇文章
- 底部显示分页导航
- 保持原有设计风格不变

## 修复步骤

1. 编辑 `home.html` 模板，添加分页逻辑
2. 修改 `home/profile.html` 组件，传递分页数据
3. 修改 `home/featured.html` 组件，使用分页数据和分页导航
4. 保存文件并重新生成网站

## 技术说明

- 使用 `where .Site.RegularPages "Params.featured" true` 获取所有精选文章
- 使用 `.Paginate $featured 10` 创建分页，每页10篇
- 使用 `dict` 函数传递多个参数给partial组件
- 使用 `$paginator.Pages` 遍历当前页的文章
- 使用 `$paginator.HasPrev` 和 `$paginator.HasNext` 判断是否有前后页
- 使用 `$paginator.Prev.URL` 和 `$paginator.Next.URL` 获取分页链接